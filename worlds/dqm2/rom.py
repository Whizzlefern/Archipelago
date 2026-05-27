import os
from pkgutil import get_data
from typing import TYPE_CHECKING, Sequence

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .encounters_data import tara_encounters_data, cobi_encounters_data, unrandomized_encounters
from .locations import lookup_location_to_id, location_data
from .monster_data import core_monster_data

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

    randomize_encounters(world, patch, game_version, valid_monster_ids)

    slot_name = str.encode(world.multiworld.player_name[world.player])
    write_bytes(patch,0x3FFFF0, slot_name)

    patch.write_file("token_data.bin", patch.get_token_binary())
    out_file_name = world.multiworld.get_out_file_name_base(world.player)
    patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))


def get_full_addr(bank, addr) -> int:
    return ((bank - 0x1) * 0x4000) + addr

def write_bytes(patch, address: int, data: Sequence[int] | int):
    patch.write_token(APTokenTypes.WRITE, address, data)

def randomize_encounters(world: "DQM2World", patch, game_version, valid_ids) -> None:
    encounters_data = cobi_encounters_data if game_version == "cobi" else tara_encounters_data

    for encounter in encounters_data:
        if encounter in unrandomized_encounters:
            continue
        elif encounter in [0x10, 0x11]:
            # Don't randomize ArmyAnt, MadGopher, for now
            continue
        elif encounter == 0x1a:
            # Make boss water type to avoid getting locked
            water_ids = list(range(0x13c, 0x15c))
            monster = world.random.choice(water_ids).to_bytes(2, "little")
        else:
            monster = world.random.choice(valid_ids).to_bytes(2, "little")            
        
        current_byte = encounters_data[encounter]["rom_addr"]
        write_bytes(patch, current_byte, monster)

        # current_byte += 0x2

# Canal Boss Monster Sprite
# 69/7c37:
#     ??
#     ??
#
# # Den of Canal Boss? xd
# 69/7b69
# 69/7d48
# 69/7d84
# 69/7d90
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