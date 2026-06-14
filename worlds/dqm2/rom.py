import os
from pkgutil import get_data
from typing import TYPE_CHECKING, Sequence

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .data import encounters_data as pbe, monster_data as cd
from .locations import location_data

if TYPE_CHECKING:
    from .world import DQM2World

DQM2_COBI_HASH = "f71ac6ac4bb335f59bfd2b594d47ab49"
DQM2_TARA_HASH = "8e79dcdee0e15ef069b3f376a0fee37d"


class TaraProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Dragon Quest Monsters 2"
    hash = DQM2_TARA_HASH
    patch_file_ending = ".apdqm2t"
    result_file_ending = ".gbc"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        from .world import DQM2World
        with open(DQM2World.settings.tara_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


class CobiProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Dragon Quest Monsters 2"
    hash = DQM2_COBI_HASH
    patch_file_ending = ".apdqm2c"
    result_file_ending = ".gbc"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        from .world import DQM2World
        with open(DQM2World.settings.cobi_rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


def patch_rom(world: "DQM2World", output_directory: str) -> None:
    game_version = world.options.game_version.current_key

    patch_type = CobiProcedurePatch if game_version == "cobi" else TaraProcedurePatch
    patch = patch_type(player=world.player, player_name=world.player_name)
    patch.write_file("base_patch.bsdiff4",
                     get_data(__name__, f"{game_version}basepatch.bsdiff4"))


    if world.options.character == 0:
        write_bytes(patch, get_full_addr(0x07, 0x68C2), bytes([0x01]))
    else:
        write_bytes(patch, get_full_addr(0x07, 0x68C2), bytes([0x00]))

    for location in world.multiworld.get_locations(world.player):
        if location.item.code is None:
            continue

        loc_data = location_data[location.name]
        if location.item and location.item.player == world.player:
            if loc_data.rom_addr:
                rom_address = get_full_addr(loc_data.rom_addr.bank, loc_data.rom_addr.addr)
                item_id = location.item.code.to_bytes(1, "little")
                write_bytes(patch, rom_address, item_id)
            else:
                continue
        else:
            if loc_data.rom_addr:
                rom_address = get_full_addr(loc_data.rom_addr.bank, loc_data.rom_addr.addr)
                item_id = bytes([0x2F])
                write_bytes(patch, rom_address, item_id)
            else:
                continue

    valid_monster_ids = []
    for monster in cd.core_monster_data.keys():
        valid_monster_ids.append(cd.core_monster_data[monster]["id"])

    encounters_data = pbe.cobi_encounters_data if game_version == "cobi" else pbe.tara_encounters_data
    four_skills = world.options.four_skills
    exp_multiplier = world.options.exp_multiplier

    current_encounter_options = {
        "Encounters Data": encounters_data,
        "Valid IDs": valid_monster_ids,
        "Four Skills": four_skills,
        "EXP Multiplier": exp_multiplier
    }

    randomize_core_monsters(world, patch)
    randomize_encounters(world, patch, current_encounter_options)
    # randomize_bosses(world, patch, current_encounter_options)
    # randomize_arena()
    # randomize_gifts()
    # randomize_mates()

    slot_name = str.encode(world.multiworld.player_name[world.player])
    write_bytes(patch,0x3FFFF0, slot_name)

    patch.write_file("token_data.bin", patch.get_token_binary())
    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))


def get_full_addr(bank, addr) -> int:
    return ((bank - 0x1) * 0x4000) + addr

def write_bytes(patch, address: int, data: Sequence[int] | int):
    patch.write_token(APTokenTypes.WRITE, address, data)

def randomize_core_monsters(world: "DQM2World", patch):
    for monster, values in cd.core_monster_data.items():
        current_byte = cd.core_monster_data[monster]["rom_addr"]
        current_monster = bytearray()

        for value in values:
            current_value = bytearray()

            if value in ["rom_addr", "id"]:
                continue

            elif value == "join" and world.options.better_join_rate:
                better_join = list(range(0x00, 0x04))
                current_value = world.random.choice(better_join).to_bytes()

            elif value == "skills":
                if world.options.randomize_level_skills:
                    current_value = bytes(world.random.sample(cd.base_skills, 3))
                else:
                    for skill in cd.core_monster_data[monster][value]:
                        current_value.extend(skill.to_bytes(1))

            elif value == "resistances":
                for resist in cd.core_monster_data[monster][value]:
                    current_value.extend(resist.to_bytes(1))

            elif value == "base_exp":
                current_value = cd.core_monster_data[monster][value].to_bytes(2, "little")

            else:
                current_value = cd.core_monster_data[monster][value].to_bytes(1)

            current_monster.extend(current_value)

        current_monster = bytes(current_monster)
        write_bytes(patch, current_byte, current_monster)


def randomize_encounters(world: "DQM2World", patch, options) -> None:
    skip_randomize = pbe.unrandomized_encounters + pbe.boss_recruits + [0x10, 0x11]

    for encounter in pbe.all_recruitable_locations:
        if encounter in skip_randomize:
            continue

        current_byte = options["Encounters Data"][encounter]["rom_addr"]
        current_encounter = create_encounter(world, encounter, options)

        write_bytes(patch, current_byte, current_encounter)


def create_encounter(world: "DQM2World", encounter, options) -> bytes:
    created_encounter = bytearray()
    encounter_id = world.random.choice(options["Valid IDs"]).to_bytes(2, "little")
    exp_multiplier = options["EXP Multiplier"]
    scaling = f"{options["Encounters Data"][encounter]["world"]} - {options["Encounters Data"][encounter]["area"]}"
    vanilla_world = options["Encounters Data"][encounter]["world"]

    # Monster ID
    created_encounter.extend(encounter_id)

    # Skills
    if options["Four Skills"]:
        sample_size = 4
    else:
        sample_size = world.random.choice(pbe.encounter_ranges[scaling]["num_skills"])

    created_skills = create_skills(world, encounter, sample_size, vanilla_world)
    created_encounter.extend(created_skills)

    # Stats
    created_stats = create_stats(world, scaling, exp_multiplier)
    created_encounter.extend(created_stats)

    return bytes(created_encounter)


def create_skills(world, encounter, sample_size, vanilla_world) -> bytearray:
    created_skills = bytearray()
    valid_skills = cd.always_available

    # Determine which skills should be available
    if encounter in pbe.all_recruitable_locations:
        if vanilla_world == "Oasis":
            valid_skills += cd.tier1
        elif vanilla_world == "Pirate":
            valid_skills += cd.tier2
        elif vanilla_world == "Ice":
            valid_skills += cd.tier3
        elif vanilla_world == "Sky":
            valid_skills += cd.tier4
        else:
            valid_skills += cd.tier5

        if vanilla_world in ["Elf", "Lonely", "Traveler"]:
            valid_skills += cd.extra

        valid_skills += cd.banned_on_boss

    skills = world.random.sample(valid_skills, sample_size)

    while len(skills) < 4:
        skills.append(0xFF)

    for skill in skills:
        created_skills.extend(skill.to_bytes(1, "little"))

    return created_skills


def create_stats(world, scaling, exp_multiplier) -> bytearray:
    created_stats = bytearray()
    for attribute in pbe.encounter_attributes:
        value = world.random.choice(pbe.encounter_ranges[scaling][attribute])
        b = pbe.encounter_attributes[attribute]
        if attribute == "exp" and exp_multiplier > 100:
            value = int(min(value * (exp_multiplier / 100), 0xFFFF))
        created_stats.extend(value.to_bytes(b, "little"))
    return created_stats

# def randomize_bosses(world: "DQM2World", encounter, options) -> None:
#     for

        # for encounter in encounters_data:
    #
    #     if encounter in skip_randomize:
    #         continue
    #     elif encounter in [0x10, 0x11]:
    #         # Don't randomize ArmyAnt, MadGopher, for now
    #         continue
    #     elif encounter == 0x1a:
    #         # Make boss water type to avoid getting locked
    #         water_ids = list(range(0x13c, 0x15c))
    #         monster = world.random.choice(water_ids).to_bytes(2, "little")
    #     else:
    #         monster = world.random.choice(valid_ids).to_bytes(2, "little")
    #
    #     if encounter in boss_joins:
    #         if encounter == 0x07:
    #             write_bytes(patch, encounters_data[0x08]["rom_addr"], monster)
    #         elif encounter == 0x1a:
    #             write_bytes(patch, encounters_data[0x1b]["rom_addr"], monster)
    #             write_bytes(patch, get_full_addr(0x69, 0x6077), monster)
    #         elif encounter == 0x182:
    #             write_bytes(patch, encounters_data[0x183]["rom_addr"], monster)
    #             for address in  [0x7c37, 0x7b69, 0x7d48, 0x7d84, 0x7d8f, 0x7d9b, 0x7da6]:
    #                 full_addr = get_full_addr(0x69, address)
    #                 write_bytes(patch, full_addr, monster)
    #         elif encounter == 0x190:
    #             write_bytes(patch, encounters_data[0x1af]["rom_addr"], monster)
    #             write_bytes(patch, get_full_addr(0x69, 0x5e2e), monster)
    #
    #         elif encounter == 0x1ab:
    #             write_bytes(patch, encounters_data[0x1ac]["rom_addr"], monster)
    #
    #     current_byte = encounters_data[encounter]["rom_addr"]
    #     write_bytes(patch, current_byte, monster)
    #
    #     if world.options.better_join_rate:
    #         if encounter in recruitable_locations:
    #             current_byte += 0x08
    #             better_join = list(range(0x01, 0x04))
    #             join = world.random.choice(better_join).to_bytes(1)
    #             write_bytes(patch, current_byte, join)

# Canal Boss Monster Sprite
# 69/7c37:
#     ??
#     ??
#
# # Den of Canal Boss? xd
# 69/7b69
# 69/7d48
# 69/7d84
# 69/7d8F
# 69/7d9b
# 69/7da6

# Pirate Boss Sprite
# 69/63a9:
#     ??
#     ??
#
# # Ocean Boss Sprite
# 69/5e2e:
#     ??
#     ??
#
# # Cape Boss Sprite
# 69/6077:
#     ??
#     ??