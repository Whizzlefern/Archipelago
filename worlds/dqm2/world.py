import os
from typing import ClassVar

import settings
from BaseClasses import Item, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld
from Utils import visualize_regions

from .items import DQM2Item, item_table, lookup_name_to_id, filler_items, item_name_groups
from .locations import location_data, lookup_location_to_id
from .names import item_names, location_names, region_names
from .options import DQM2Options
from .regions import create_regions, connect_regions, create_events
from .rom import patch_rom, CobiProcedurePatch, TaraProcedurePatch
from .rules import set_all_rules


class DQM2Settings(settings.Group):
    class CobiRomFile(settings.UserFilePath):
        """File name of  the Dragon Quest Monsters 2 ROMs"""
        description = "Dragon Quest Monsters 2 - Cobi's Journey ROM File"
        copy_to = "Dragon Warrior Monsters 2 - Cobi's Journey (USA) (SGB Enhanced) (GB Compatible).gbc"
        md5s = [CobiProcedurePatch.hash]

    class TaraRomFile(settings.UserFilePath):
        description = "Dragon Quest Monsters 2 - Tara's Adventure ROM File"
        copy_to = "Dragon Warrior Monsters 2 - Tara's Adventure (USA) (SGB Enhanced) (GB Compatible).gbc"
        md5s = [TaraProcedurePatch.hash]

    cobi_rom_file: CobiRomFile = CobiRomFile(CobiRomFile.copy_to)
    tara_rom_file: TaraRomFile = TaraRomFile(TaraRomFile.copy_to)


class DQM2WebWorld(WebWorld):
    theme = "grassFlowers"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Dragon Quest Monsters 2 randomizer connected to an Archipelago Multiworld",
            "English",
            "setup_en.md",
            "setup/en",
            ["Whizzlefern"]
        )
    ]


class DQM2World(World):
    """
    Your island home is sinking into the ocean, and you're the one to save it!
    You'll need to find, train and breed an army of the coolest, weirdest and
    cutest Dragon Warrior monsters to ever live inside your Game Boy!
    """
    game = "Dragon Quest Monsters 2"
    authors = ["Whizzlefern"]
    settings_key = "dqm2_options"
    settings: ClassVar[DQM2Settings]
    options_dataclass = DQM2Options
    options: DQM2Options
    item_name_to_id = lookup_name_to_id
    location_name_to_id = lookup_location_to_id
    
    item_name_groups: item_name_groups

    web = DQM2WebWorld()
    origin_region_name = region_names.greatlog
    topology_present = False

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)
        create_events(self)

        itempool = []

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        # FOR NOW
        unrandomized_items = [item_names.greatlog_key, item_names.oasis_key, item_names.pirate_key, item_names.ice_key,
                              item_names.sky_key, item_names.limbo_key, item_names.elf_key, item_names.lonely_key,
                              item_names.travel_key, item_names.brawn_key, item_names.baffle_key, item_names.soul_key,
                              item_names.magic_key, item_names.wiz_stone, item_names.pretty_ring]

        for item in item_table.keys():
            if item in unrandomized_items:
                continue
            itempool += [self.create_item(item)]

        while len(itempool) < total_locations:
            itempool += [self.create_item(self.get_filler_item_name())]

        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        set_all_rules(self)

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        created_item = DQM2Item(name, data.classification, data.code, self.player)

        return created_item

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(filler_items)

    # def pre_fill(self) -> None:
    #     visualize_regions(self.get_region(region_names.greatlog), "dqm2_map.puml")

    def generate_output(self, output_directory: str) -> None:
        patch_rom(self, output_directory)
