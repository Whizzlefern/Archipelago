from typing import NamedTuple, Dict

from BaseClasses import Item, ItemClassification as IC
from .names import item_names

class DQM2Item(Item):
    game = "Dragon Quest Monsters 2"

class ItemData:
    def __init__(self, code, groups=None, classification=None):
      self.code = None if code is None else code
      self.groups = groups
      self.classification = IC.filler if classification is None else classification

item_table = {
    item_names.herb: ItemData(0x01, ["Medicine"]),
    item_names.love_water: ItemData(0x02, ["Medicine"]),
    item_names.world_dew: ItemData(0x03, ["Medicine"]),
    item_names.potion: ItemData(0x04, ["Medicine"]),
    item_names.elf_water: ItemData(0x05, ["Medicine"]),
    item_names.antidote: ItemData(0x06, ["Medicine"]),
    item_names.moon_herb: ItemData(0x07, ["Medicine"]),
    item_names.laurel: ItemData(0x08, ["Medicine"]),
    item_names.awake_sand: ItemData(0x09, ["Medicine"]),
    item_names.sky_bell: ItemData(0x0A, ["Medicine"]),
    item_names.sage_rock: ItemData(0x0B, ["Medicine"]),
    item_names.world_leaf: ItemData(0x0C, ["Medicine"]),
    item_names.atk_seed: ItemData(0x0D, ["Stat Seeds"]),
    item_names.def_seed: ItemData(0x0E, ["Stat Seeds"]),
    item_names.agl_seed: ItemData(0x0F, ["Stat Seeds"]),
    item_names.int_seed: ItemData(0x10, ["Stat Seeds"]),
    item_names.life_acorn: ItemData(0x11, ["Stat Seeds"]),
    item_names.mystic_nut: ItemData(0x12, ["Stat Seeds"]),
    item_names.quest_book: ItemData(0x13, ["Books"]),
    item_names.horror_book: ItemData(0x14, ["Books"]),
    item_names.be_nice_book: ItemData(0x15, ["Books"]),
    item_names.cheater_book: ItemData(0x16, ["Books"]),
    item_names.smart_book: ItemData(0x17, ["Books"]),
    item_names.comedy_book: ItemData(0x18, ["Books"]),
    item_names.beef_jerky: ItemData(0x19, ["Meat"]),
    item_names.pork_chop: ItemData(0x1A, ["Meat"]),
    item_names.rib: ItemData(0x1B, ["Meat"]),
    item_names.sirloin: ItemData(0x1C, ["Meat"], IC.useful),
    item_names.bad_meat: ItemData(0x1D, ["Meat"]),
    item_names.meteorb: ItemData(0x1E, ["Meat"], IC.useful),
    item_names.beast_tail: ItemData(0x1F, ["Battle Items"]),
    item_names.repellent: ItemData(0x20, ["Battle Items"]),
    item_names.shiny_harp: ItemData(0x21, ["Battle Items"]),
    item_names.mist_staff: ItemData(0x22, ["Staves"]),
    item_names.friend_staff: ItemData(0x23, ["Staves"]),
    item_names.wind_staff: ItemData(0x24, ["Staves"]),
    item_names.bolt_staff: ItemData(0x25, ["Staves"]),
    item_names.snow_staff: ItemData(0x26, ["Staves"]),
    item_names.fire_staff: ItemData(0x27, ["Staves"]),
    item_names.warp_staff: ItemData(0x28, ["Staves", "Travel Items"]),
    item_names.warp_wing: ItemData(0x29, ["Travel Items"]),
    item_names.exit_bell: ItemData(0x2A, ["Travel Items"]),
    item_names.bookmark: ItemData(0x2B, ["Travel Items"]),
    item_names.tiny_medal: ItemData(0x2C, ["Travel Items"], IC.progression_deprioritized_skip_balancing),
    item_names.gold_pass: ItemData(0x2D, ["Travel Items", "Unique"], IC.useful),
    item_names.log_twig: ItemData(0x2E, ["Travel Items"]),
    # 0x2F unused
    item_names.water_call: ItemData(0x30, ["Unique", "Key Items"], IC.progression),
    item_names.moon_rock: ItemData(0x31, ["Unique", "Key Items"], IC.progression),
    item_names.crest: ItemData(0x32, ["Unique", "Key Items"], IC.progression),
    item_names.yuna_soul: ItemData(0x33, ["Unique", "Key Items"], IC.progression),
    item_names.sleep_herb: ItemData(0x34, ["Unique", "Key Items"], IC.progression),
    item_names.change_staff : ItemData(0x35, ["Unique", "Key Items"], IC.progression),
    item_names.tidal_bell: ItemData(0x36, ["Unique", "Key Items"], IC.progression | IC.useful),
    item_names.har_mirror: ItemData(0x37, ["Unique", "Key Items"], IC.progression | IC.useful),
    item_names.sky_shield: ItemData(0x38, ["Unique", "Key Items"], IC.progression | IC.useful),
    item_names.heaven_helmet: ItemData(0x39, ["Unique", "Key Items"], IC.progression),
    item_names.heaven_armor: ItemData(0x3A, ["Unique", "Key Items"], IC.progression),
    item_names.heaven_sword: ItemData(0x3B, ["Unique", "Key Items"], IC.progression),
    item_names.wiz_stone: ItemData(0x3C, ["Unique", "Key Items"], IC.progression),
    item_names.pretty_ring: ItemData(0x3D, ["Unique", "Key Items"], IC.progression),
    # 0x3E-0x3F unused
    # Raw Stat Boosts
    item_names.vit_belt: ItemData(0x40, ["Equipment"]),
    item_names.draco_belt: ItemData(0x41, ["Equipment"]),
    item_names.magic_belt: ItemData(0x42, ["Equipment"]),
    item_names.odd_belt: ItemData(0x43, ["Equipment"]),
    item_names.stone_fang: ItemData(0x44, ["Equipment"]),
    item_names.steel_fang: ItemData(0x45, ["Equipment"]),
    item_names.merm_scale: ItemData(0x46, ["Equipment"]),
    item_names.drak_scale: ItemData(0x47, ["Equipment"]),
    item_names.agl_ring: ItemData(0x48, ["Equipment"]),
    item_names.starry_ring: ItemData(0x49, ["Equipment"]),
    item_names.smart_hat: ItemData(0x4A, ["Equipment"]),
    item_names.wise_hat: ItemData(0x4B, ["Equipment"]),
    # Resistance Boosts
    item_names.magic_cape: ItemData(0x4C, ["Equipment"]),
    item_names.draco_cape: ItemData(0x4D, ["Equipment"]),
    item_names.silver_cape: ItemData(0x4E, ["Equipment"]),
    item_names.gold_cape: ItemData(0x4F, ["Equipment"]),
    item_names.plat_cape: ItemData(0x50, ["Equipment"]),
    item_names.orca_cape: ItemData(0x51, ["Equipment"]),
    item_names.brave_cape: ItemData(0x52, ["Equipment"]),
    item_names.d_scale: ItemData(0x53, ["Equipment"]),
    # 0x54-0x59 are unused
    # Stat Growth Boosts
    item_names.life_ring: ItemData(0x5A, ["Equipment"]),
    item_names.divine_ring: ItemData(0x5B, ["Equipment"]),
    item_names.war_ring: ItemData(0x5C, ["Equipment"]),
    item_names.mage_ring: ItemData(0x5D, ["Equipment"]),
    item_names.fight_ring: ItemData(0x5E, ["Equipment"]),
    item_names.sailor_ring: ItemData(0x5F, ["Equipment"]),
    item_names.thief_ring: ItemData(0x60, ["Equipment"]),
    item_names.cleric_ring: ItemData(0x61, ["Equipment"]),
    # Keys use custom IDs
    item_names.greatlog_key: ItemData(0x81, ["Unique", "World Keys"], IC.progression),
    item_names.oasis_key: ItemData(0x82, ["Unique", "World Keys"], IC.progression),
    item_names.pirate_key: ItemData(0x83, ["Unique", "World Keys"], IC.progression),
    item_names.ice_key: ItemData(0x84, ["Unique", "World Keys"], IC.progression),
    item_names.sky_key: ItemData(0x85, ["Unique", "World Keys"], IC.progression),
    item_names.limbo_key: ItemData(0x86, ["Unique", "World Keys"], IC.progression),
    item_names.elf_key: ItemData(0x87, ["Unique", "World Keys"], IC.progression),
    item_names.lonely_key: ItemData(0x88, ["Unique", "World Keys"], IC.progression),
    item_names.travel_key: ItemData(0x89, ["Unique", "World Keys"], IC.progression),
    item_names.brawn_key: ItemData(0x8A, ["Unique", "World Keys"], IC.progression),
    item_names.baffle_key: ItemData(0x8B, ["Unique", "World Keys"], IC.progression),
    item_names.soul_key: ItemData(0x8C, ["Unique", "World Keys"], IC.progression),
    item_names.magic_key: ItemData(0x8D, ["Unique", "Travel Items"], IC.useful)
}

filler_items = [item_name for item_name, data in item_table.items() if "Unique" not in data.groups]

item_name_groups: dict[str, set[str]] = {
  "Medicine": {},
  "Stat Seeds": {},
  "Books": {},
  "Meat": {},
  "Battle Items": {},
  "Staves": {},
  "Travel Items": {},
  "Key Items": {},
  "Equipment": {},
  "World Keys": {}
}

for group_name in item_name_groups.keys():
  group = set()
  for item_name, data in item_table.items():
    if group_name in data.groups:
      group.add(item_name)
  
  item_name_groups.update({group_name: group})


lookup_name_to_id: Dict[str, int] = {item_name: data.code for item_name, data in item_table.items()}
lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}