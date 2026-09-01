import os, copy
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

    allowed_monsters = world.options.allowed_monsters.value
    valid_monster_ids = get_valid_monster_ids(allowed_monsters)

    current_core_options = {
        "Better Join Rate": world.options.better_join_rate,
        "Randomize Level Up Skills": world.options.randomize_level_skills,
        "Randomize EXP Growth": world.options.randomize_exp_growth,
        "Randomize Stat Growths": world.options.randomize_stat_growths
    }

    current_encounter_options = {
        "Encounters Data": pbe.cobi_encounters_data if game_version == "cobi" else pbe.tara_encounters_data,
        "Valid IDs": valid_monster_ids,
        "Randomize Encounters": world.options.randomize_encounters,
        "Randomize Encounter Skills": world.options.randomize_encounter_skills,
        "Randomize Encounter Stats": world.options.randomize_encounter_stats,
        "EXP Multiplier": world.options.exp_multiplier
    }

    if world.options.randomize_breeding_results:
        randomize_breeding_results(world, patch, valid_monster_ids)

    core_randomized = (current_core_options["Better Join Rate"] | current_core_options["Randomize Level Up Skills"] |
            current_core_options["Randomize EXP Growth"] | current_core_options["Randomize Stat Growths"])
    if core_randomized:
        randomize_core_monsters(world, patch, current_core_options)

    encounters_randomized = (current_encounter_options["Randomize Encounters"] | current_encounter_options["Randomize Encounter Skills"] | current_encounter_options["Randomize Encounter Stats"] | current_encounter_options["EXP Multiplier"] > 100)
    if encounters_randomized:
        randomize_encounters(world, patch, current_encounter_options)

    slot_name = str.encode(world.multiworld.player_name[world.player])
    write_bytes(patch, 0x3FFFF0, slot_name)

    patch.write_file("token_data.bin", patch.get_token_binary())
    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))


def get_full_addr(bank, addr) -> int:
    return ((bank - 0x1) * 0x4000) + addr if bank > 0x00 else addr


def get_bank_addr(addr) -> list:
    return [(addr // 0x4000), ((addr % 0x4000) + 0x4000)]


def write_bytes(patch, address: int, data: Sequence[int] | int):
    patch.write_token(APTokenTypes.WRITE, address, data)


def get_valid_monster_ids(allowed_monsters) -> list:
    valid_ids = []

    if len(allowed_monsters) == 0:
        for monster in cd.core_monster_data.keys():
            valid_ids.append(cd.core_monster_data[monster]["id"])
    else:
        allowed_from_family = []
        allowed_from_species = []

        for value in allowed_monsters:
            if value in ["Slime (Family)", "Dragon (Family)", "Beast", "Bird", "Plant", "Bug", "Devil", "Zombie",
                         "Material", "Water", "???"]:
                if value in ["Slime (Family)", "Dragon (Family)"]:
                    value = value.split(" ")[0]
                for monster in cd.species_data[value]["monsters"]:
                    allowed_from_family.append(monster)
            else:
                if value in ["Slime (Species)", "Dragon (Species)"]:
                    value = value.split(" ")[0]
                allowed_from_species.append(value)

        for monster in list(set(allowed_from_family + allowed_from_species)):
            valid_ids.append(cd.core_monster_data[monster]["id"])

    return valid_ids


def randomize_core_monsters(world: "DQM2World", patch, options) -> None:
    population = list(range(0, 32))
    weights = [0.1] + ([1] * 31)
    growths = ["hp_growth", "mp_growth", "atk_growth", "def_growth", "agi_growth", "int_growth"]

    for monster, values in cd.core_monster_data.items():
        current_byte = cd.core_monster_data[monster]["rom_addr"]
        current_monster = bytearray()

        for value in values:
            current_value = bytearray()

            if value in ["rom_addr", "id"]:
                continue

            elif value == "join" and options["Better Join Rate"]:
                better_join = list(range(0x01, 0x04))
                current_value = bytes([world.random.choice(better_join)])

            elif value == "exp_growth" and options["Randomize EXP Growth"]:
                if options["Randomize EXP Growth"].current_key == "fast":
                    growth_options = list(range(0x00, 0x08))
                else:
                    growth_options = population
                current_value = bytes([world.random.choice(growth_options)])

            elif value == "skills":
                if options["Randomize Level Up Skills"]:
                    current_value = bytes(world.random.sample(cd.base_skills, 3))
                else:
                    for skill in cd.core_monster_data[monster][value]:
                        current_value.extend(bytes([skill]))

            elif value in growths and options["Randomize Stat Growths"]:
                current_value = bytes(world.random.choices(population=population, weights=weights, k=1))

            elif value == "resistances":
                for resist in cd.core_monster_data[monster][value]:
                    current_value.extend(bytes([resist]))

            elif value == "base_exp":
                current_value = cd.core_monster_data[monster][value].to_bytes(2, "little")

            else:
                current_value = bytes([cd.core_monster_data[monster][value]])

            current_monster.extend(current_value)

        current_monster = bytes(current_monster)
        write_bytes(patch, current_byte, current_monster)


def randomize_breeding_results(world: "DQM2World", patch, valid_ids) -> None:
    byte_pairs = {0x3b116: 0x3b34e, 0x3ba51: 0x3bb83, 0x3bdd5: 0x3be83, 0x3be9b: 0x3bf75}
    spacers = [0x3beb1, 0x3bec9, 0x3bee1, 0x3bef9, 0x3bf11, 0x3bf29, 0x3bf41, 0x3bf59, 0x3bf71]

    for start, end in byte_pairs.items():
        current_byte = copy.deepcopy(start)
        while current_byte < end:
            if current_byte in spacers:
                current_byte += 0x2
            result = world.random.choice(valid_ids).to_bytes(2, "little")
            write_bytes(patch, current_byte, result)

            current_byte += 0x2


def randomize_encounters(world: "DQM2World", patch, options) -> None:
    skip_randomize = (pbe.all_unused +
                      pbe.boss_recruits +  # Randomized with bosses
                      [0x10, 0x11] +  # Skip ArmyAnt and MadGopher, for now
                      pbe.medal_man_gifts +  # Requires script edit
                      pbe.breeding_pairs +  # Requires script edit
                      pbe.egg_gifts +  # Requires script edit
                      pbe.summons)  # Requires unique case

    all_encounters = options["Encounters Data"]
    valid_ids = options["Valid IDs"]
    random_monsters = options["Randomize Encounters"]
    random_skills = options["Randomize Encounter Skills"]
    random_stats = options["Randomize Encounter Stats"]
    exp_multiplier = options["EXP Multiplier"]

    ### PROGRESS CHECKING ###
    ### All 684 Encounters include
    ### [o] all_recruitable       - random encounters
    ### [o] all_boss              - boss fights in key worlds
    ### [o] all_arena             - boss fights in the arena
    ### [o] all_wandering_masters - wandering masters
    ### [o] all_npc_bosses        - boss fights against non arena NPCs
    ### [o] all_misc              - see below
    ###   [o] starting_monster
    ###   [x] summons
    ###   [ ] mimic_encounters
    ###   [x] medal_man_gifts
    ###   [x] breeding_pairs
    ###   [x] egg_gifts
    ###   [x] boss_recruits
    ### [x] all_unused            - promotional, unused, and debug

    ### o = Skills need to be look at

    overworld_bosses = [0x1a, 0x1c, 0x182, 0x190, 0x32, 0x44, 0x199, 0x64, 0x1A6, 0x1AB]

    for encounter in all_encounters:
        if encounter in skip_randomize:
            continue

        current_byte = all_encounters[encounter]["rom_addr"]
        current_encounter = create_encounter(world, encounter, all_encounters, valid_ids, random_monsters, random_skills, random_stats, exp_multiplier)
        if encounter in pbe.boss_joins:
            create_boss_recruit(world, patch, encounter, current_encounter, options["Encounters Data"])
        if encounter in overworld_bosses:
            mon_id = current_encounter[0:2]
            edit_overworld_boss(patch, encounter, mon_id)
        #
        #
        #
        #
        write_bytes(patch, current_byte, current_encounter)


def create_encounter(world: "DQM2World", encounter, all_encounters, valid_ids, random_monsters, random_skills, random_stats, exp_multiplier) -> bytes:
    created_encounter = bytearray()

    current_encounter = all_encounters[encounter]

    encounter_info = {
        "World": current_encounter["world"],
        "Area": current_encounter["area"],
        "Type": current_encounter["type"]
    }

    if encounter_info["Type"] == "Recruitable" or encounter_info["Area"] == "Tower":
        scaling = f"{encounter_info['World']} - {encounter_info['Area']}"
    elif encounter_info["World"] == "Arena" or encounter_info["Type"].startswith("Wandering"):
        scaling = f"{encounter_info['Type']}"
    else:
        scaling = ""

    # Monster ID
    if random_monsters:
        mon_id = get_mon_id(world, encounter, valid_ids)
    else:
        mon_id = current_encounter["id"].to_bytes(2, "little")

    created_encounter.extend(mon_id)

    # Skills
    created_skills = bytearray()
    if random_skills:
        if random_skills == 2:
            sample_size = 4
        else:
            if scaling != "":
                sample_size = world.random.choice(pbe.encounter_ranges[scaling]["num_skills"])
            else:
                sample_size = world.random.choice([0, 1, 2, 3, 4])
        created_skills = create_skills(world, encounter, sample_size, encounter_info)
    else:
        for skill in ["skill_1", "skill_2", "skill_3", "skill_4"]:
            created_skills.extend(bytes([current_encounter[skill]]))

    created_encounter.extend(created_skills)

    # Stats
    created_stats = bytearray()
    if random_stats:
        # Give slash a little boost
        if encounter == 0x1:
            scaling = "Oasis - Overworld"
        created_stats = create_stats(world, current_encounter, scaling, exp_multiplier)
    else:
        for value in ["exp", "join", "level", "hp", "mp", "atk", "def", "agi", "int", "charge", "defense", "motivation", "mixed"]:
            if value == "exp" and exp_multiplier > 100:
                current_value = min(int(current_encounter[value] * (exp_multiplier / 100)), 0xFFFF)
            else:
                current_value = current_encounter[value]
            if value in ["join", "level", "charge", "defense", "motivation", "mixed"]:
                current_value = bytes([current_value])
            else:
                current_value = current_value.to_bytes(2, "little")
            created_stats.extend(current_value)

    created_encounter.extend(created_stats)

    return bytes(created_encounter)


def get_mon_id(world: "DQM2World", encounter, valid_ids) -> bytes:
    # TODO: Temporarily limit Cape Cave boss to water type to prevent soft locks
    if encounter == 0x1a:
        valid_ids = list(range(0x13c, 0x15c))
    return world.random.choice(valid_ids).to_bytes(2, "little")


def create_skills(world: "DQM2World", encounter, sample_size, encounter_info) -> bytearray:
    created_skills = bytearray()
    valid_skills = []
    valid_skills += cd.always_available
    vanilla_world = encounter_info["World"]
    vanilla_area = encounter_info["Area"]
    enc_type = encounter_info["Type"]

    if vanilla_world == "Oasis" or enc_type in ["Kiddie Class", "Wandering Masters - Tier 1", "Starting Monster"]:
        valid_skills += cd.tier1
    elif vanilla_world == "Pirate" or enc_type in ["C Class", "Wandering Masters - Tier 2"]:
        valid_skills += cd.tier2
    elif vanilla_world == "Ice" or enc_type in ["B Class", "C Free", "Wandering Masters - Tier 3"]:
        valid_skills += cd.tier3
    elif vanilla_world == "Sky" or enc_type in ["A Class", "B Free", "Wandering Masters - Tier 4"]:
        valid_skills += cd.tier4
    else:
        valid_skills += cd.tier5

    if vanilla_world in ["Elf", "Lonely", "Traveler"]:
        valid_skills += cd.extra

    if enc_type == "Recruitable":
        valid_skills += cd.banned_on_boss

    skills = world.random.sample(valid_skills, sample_size)

    # Ensure dance move on Cape Boss
    if encounter == 0x1a:
        dance_moves = [0x76, 0x78, 0x7a, 0x7c, 0x7d]
        dance_check: bool = False
        for dance in dance_moves:
            if dance in skills:
                dance_check = True

        if not dance_check:
            if len(skills) > 0:
                del skills[-1]
            skills.append(world.random.choice(dance_moves))

    while len(skills) < 4:
        skills.append(0xFF)

    for skill in skills:
        created_skills.extend(bytes([skill]))
    return created_skills


def create_stats(world: "DQM2World", encounter, scaling, exp_multiplier) -> bytearray:
    created_stats = bytearray()

    if scaling != "":
        for attribute in pbe.encounter_attributes:
            value = world.random.choice(pbe.encounter_ranges[scaling][attribute])
            b = pbe.encounter_attributes[attribute]

            # Max is 65535 for EXP, 999 otherwise
            if attribute == "exp":
                value = min(int(value * (exp_multiplier / 100)), 0xFFFF)
            else:
                value = min(value, 0x3e7)

            # Min is 0 for listed attributes, 1 otherwise
            if attribute in ["exp", "join", "mp", "charge", "defense", "motivation", "mixed"]:
                value = max(value, 0x0)
            else:
                value = max(value, 0x1)

            created_stats.extend(value.to_bytes(b, "little"))
    else:
        boss_scaling = [0.80, 0.85, 0.90, 0.95, 1, 1.05, 1.10, 1.15, 1.20]
        for attribute in encounter:
            if attribute in ["rom_addr", "id", "skill_1", "skill_2", "skill_3", "skill_4", "world", "area", "type"]:
                continue

            b = pbe.encounter_attributes[attribute]
            if attribute in ["exp", "hp", "mp", "atk", "def", "agi", "int"]:
                value = int(encounter[attribute] * world.random.choice(boss_scaling))
            else:
                value = encounter[attribute]

            # Max is 65535 for EXP, 999 otherwise
            if attribute == "exp":
                value = min(int(value * (exp_multiplier / 100)), 0xFFFF)
            else:
                value = min(value, 0x3e7)

            # Min is 0 for listed attributes, 1 otherwise
            if attribute in ["exp", "join", "mp", "charge", "defense", "motivation", "mixed"]:
                value = max(value, 0x0)
            else:
                value = max(value, 0x1)

            created_stats.extend(value.to_bytes(b, "little"))

    return created_stats


def create_boss_recruit(world: "DQM2World", patch, encounter, current_encounter, all_encounters) -> None:
    current_recruit = bytearray(current_encounter)
    recruit_hp = int.from_bytes(current_encounter[10:12], "little")
    boss_scaling = [0.80, 0.85, 0.90, 0.95, 1, 1.05, 1.10, 1.15, 1.20]

    if encounter in [0x7, 0x1A, 0x182, 0x1AB]:
        recruit_hp = int((recruit_hp / 4) * world.random.choice(boss_scaling))
    else:
        recruit_hp = int((recruit_hp / 10) * world.random.choice(boss_scaling))

    recruit_hp = recruit_hp.to_bytes(2, "little")
    current_recruit[10] = recruit_hp[0]
    current_recruit[11] = recruit_hp[1]

    if encounter == 0x190:
        current_byte = all_encounters[0x1AF]["rom_addr"]
    else:
        ptr = encounter + 0x1
        current_byte = all_encounters[ptr]["rom_addr"]

    current_recruit = bytes(current_recruit)
    write_bytes(patch, current_byte, current_recruit)


def edit_overworld_boss(patch, encounter, mon_id) -> None:
    if encounter == 0x1a:
        # Cape Cave
        write_bytes(patch, get_full_addr(0x69, 0x6077), mon_id)
    elif encounter == 0x1c:
        # Ghost Ship
        write_bytes(patch, get_full_addr(0x69, 0x63a9), mon_id)
    elif encounter == 0x182:
        # Canal
        for address in [0x7c37, 0x7b69, 0x7d48, 0x7d84, 0x7d8f, 0x7d9b, 0x7da6]:
            full_addr = get_full_addr(0x69, address)
            write_bytes(patch, full_addr, mon_id)
    elif encounter == 0x190:
        # Pirate Ocean
        write_bytes(patch, get_full_addr(0x69, 0x5e2e), mon_id)
    elif encounter == 0x32:
        # Gold Mine
        write_bytes(patch, get_full_addr(0x69, 0x56cd), mon_id)
        write_bytes(patch, get_full_addr(0x69, 0x56ef), mon_id)
    elif encounter == 0x44:
        # Estria Castle
        write_bytes(patch, get_full_addr(0x69, 0x5d1b), mon_id)
    elif encounter == 0x199:
        # Norden Castle
        write_bytes(patch, get_full_addr(0x69, 0x5331), mon_id)
        write_bytes(patch, get_full_addr(0x69, 0x5353), mon_id)
    elif encounter == 0x64:
        # Graveyard
        write_bytes(patch, get_full_addr(0x69, 0x4fd8), mon_id)
    elif encounter == 0x1A6:
        # Small Cave
        write_bytes(patch, get_full_addr(0x69, 0x4e4d), mon_id)
    elif encounter == 0x1AB:
        # Nest
        for address in [0x4acb, 0x4c24]:
            full_addr = get_full_addr(0x69, address)
            write_bytes(patch, full_addr, mon_id)
