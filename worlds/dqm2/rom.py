import os
from pkgutil import get_data
from typing import TYPE_CHECKING, Sequence

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .encounters_data import tara_encounters_data, cobi_encounters_data, unrandomized_encounters, recruitable_locations, \
    boss_joins, boss_recruits, oasis_overworld_encounters
from .locations import lookup_location_to_id, location_data
from .monster_data import core_monster_data, base_skills

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

    for monster in core_monster_data.keys():
        valid_monster_ids.append(core_monster_data[monster]["id"])

    randomize_core_monsters(world, patch)


    encounters_data = cobi_encounters_data if game_version == "cobi" else tara_encounters_data
    randomize_encounters(world, patch, encounters_data, valid_monster_ids)
    # randomize_bosses()
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
    for monster, values in core_monster_data.items():
        current_byte = core_monster_data[monster]["rom_addr"]
        current_monster = bytearray()

        for value in values:
            current_value = bytearray()

            if value in ["rom_addr", "id"]:
                continue

            elif value == "join" and world.options.better_join_rate:
                better_join = list(range(0x00, 0x04))
                current_value = world.random.choice(better_join).to_bytes()

            elif value == "skills":
                if world.options.randomize_skills:
                    current_value = bytes(world.random.sample(base_skills, 3))
                else:
                    for skill in core_monster_data[monster][value]:
                        current_value.extend(skill.to_bytes(1))

            elif value == "resistances":
                for resist in core_monster_data[monster][value]:
                    current_value.extend(resist.to_bytes(1))

            elif value == "base_exp":
                current_value = core_monster_data[monster][value].to_bytes(2, "little")

            else:
                current_value = core_monster_data[monster][value].to_bytes(1)

            current_monster.extend(current_value)

        current_monster = bytes(current_monster)
        write_bytes(patch, current_byte, current_monster)




def randomize_encounters(world: "DQM2World", patch, encounters_data, valid_ids) -> None:
    skip_randomize = unrandomized_encounters + boss_recruits + [0x10, 0x11]

    for encounter in recruitable_locations:
        if encounter in skip_randomize:
            continue

        current_byte = encounters_data[encounter]["rom_addr"]
        current_monster = bytearray()

        current_monster.extend(world.random.choice(valid_ids).to_bytes(2, "little"))
        current_monster = bytes(current_monster)

        write_bytes(patch, current_byte, current_monster)




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