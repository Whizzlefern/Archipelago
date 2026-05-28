from BaseClasses import Location
from .names import location_names as ln, region_names as rn


class DQM2Location(Location):
    game = "Dragon Quest Monsters 2"


class LocationData:
    def __init__(self, region, rom_addr=None, ram_addr=None):
        self.region = region
        self.rom_addr = rom_addr
        self.ram_addr = ram_addr
        self.address = None


class RomLoc:
    def __init__(self, bank, addr):
        self.bank = bank
        self.addr = addr


class Flag:
    def __init__(self, flag):
        self.flag = flag
        self.byte = 0xCBD7 + int(flag / 8)
        self.bit = flag % 8
        self.bit_mask = 1 << self.bit


location_data = {
    # ==== GreatLog === #
    # Farm
    # TODO: In Game Modification 
    #    ln.farm_dad_gift: LocationData(rn.greatlog, RomLoc(0x13, 0x5E29), Flag(0x100)),
    #    ln.farm_mom_gift Flag(0x1A7)
    ln.stable_vase_1: LocationData(rn.stable, RomLoc(0x13, 0x7AD1), Flag(0x13C)),
    ln.stable_vase_2: LocationData(rn.stable, RomLoc(0x13, 0x7AE2), Flag(0x13D)),
        
    # Arena
    ln.arena_vase: LocationData(rn.arena, RomLoc(0x13, 0x6D47), Flag(0x10C)),
    
    # Residential
    ln.old_man_house_vase: LocationData(rn.residential, RomLoc(0x13, 0x6FD2), Flag(0x114)),
    # TODO: In Game Modification 
    # ln.slime_trade_gift??? Flag(0x12E)
    ln.housing_vase: LocationData(rn.residential, RomLoc(0x13, 0x7A23), Flag(0x130)),
    
    # Shops
    # TODO: In Game Modification 
    #    ln.rare_key_shelf: LocationData(rn.shops, 0, Flag(0x11E)),
    ln.key_shop_vase: LocationData(rn.shops, RomLoc(0x13, 0x7A04), Flag(0x132)),
    
    # Castle
    # TODO: In Game Modification 
    #    ln.kameha_battle_1: LocationData(rn.castle, RomLoc(0x85, 0x49A3), Flag(0x3A)),
    #    ln.kameha_battle_2: LocationData(rn.castle, RomLoc(0x85, 0x48F6), Flag(0x3C)),
    #    ln.castle_king_gift: LocationData(rn.castle, RomLoc(0x73, 0x5998), Flag(0x117)),
    ln.kameha_chest_1: LocationData(rn.greatlog_castle, RomLoc(0x13, 0x76C3), Flag(0x11B)),
    ln.kameha_chest_2: LocationData(rn.greatlog_castle, RomLoc(0x13, 0x76D4), Flag(0x11C)),
    
    # Treetop
    ln.treetop_vase: LocationData(rn.treetop, RomLoc(0x13, 0x73EB), Flag(0x126)),
    ln.treetop_chest_1: LocationData(rn.treetop, RomLoc(0x13, 0x7DE1), Flag(0x13E)),
    ln.treetop_chest_2: LocationData(rn.treetop, RomLoc(0x13, 0x7DF3), Flag(0x13F)),
    
    # ==== Oasis World === #
    # Kalka
    ln.kalka_vase: LocationData(rn.kalka, RomLoc(0x04, 0x6244), Flag(0x46)),
    
    # Asiya
    ln.asiya_vase: LocationData(rn.asiya, RomLoc(0x04, 0x644B), Flag(0x47)),
    ln.asiya_prisoner: LocationData(rn.asiya, RomLoc(0x73, 0x6EAB), Flag(0x57)),
    
    # Canal
    ln.canal_nw_vase_1: LocationData(rn.canal, RomLoc(0x04, 0x6651), Flag(0x4B)),
    ln.canal_nw_vase_2: LocationData(rn.canal, RomLoc(0x04, 0x6662), Flag(0x4C)),
    ln.canal_ne_vase_1: LocationData(rn.canal, RomLoc(0x04, 0x6673), Flag(0x4D)),
    ln.canal_ne_vase_2: LocationData(rn.canal, RomLoc(0x04, 0x6684), Flag(0x4E)),
    ln.canal_chest_above_boss: LocationData(rn.canal, RomLoc(0x04, 0x6695), Flag(0x4F)),
    ln.canal_chest_east_boss: LocationData(rn.canal, RomLoc(0x04, 0x66A6), Flag(0x50)),
    ln.canal_sw_chest_1: LocationData(rn.canal, RomLoc(0x04, 0x66B7), Flag(0x51)),
    ln.canal_sw_chest_2: LocationData(rn.canal, RomLoc(0x04, 0x66C8), Flag(0x52)),
    ln.canal_boss_defeated: LocationData(rn.canal, 0, Flag(0x53)),
    ln.canal_entrance_vase: LocationData(rn.canal, RomLoc(0x04, 0x67E1), Flag(0x5B)),
    
    # Mirage Lake
    ln.mirage_lake_boss_defeated: LocationData(rn.mirage_lake, 0, Flag(0x5A)),
    
    # ==== Pirate World ==== #
    # ln.ocean_boss_defeated: LocationData(rn.pirate_world, 0, Flag(0xF4)),
    
    # Yold
    ln.yold_barrel: LocationData(rn.yold, RomLoc(0x04, 0x5A5A), Flag(0x62)),
    
    # Polona
    # TODO: Disabled for now since it prevents picking up items from the world map if I mess with this ???
    # ln.polona_dance: LocationData(rn.polona, RomLoc(0x73, 0x6BEE), Flag(0x6E)),
    
    # Mermaid World
    ln.mermaid_queen: LocationData(rn.mermaid, RomLoc(0x04, 0x5EA5), Flag(0x5E)),
    
    # Ritz
    ln.ritz_barrel: LocationData(rn.ritz, RomLoc(0x04, 0x5C32), Flag(0x63)),
    
    # Cape Cave
    ln.cape_boss_defeated: LocationData(rn.cape_cave, 0, Flag(0x66)),
    ln.cape_nw_chest: LocationData(rn.cape_cave, RomLoc(0x04, 0x5D75), Flag(0x67)),
    ln.cape_n_chest: LocationData(rn.cape_cave, RomLoc(0x04, 0x5D86), Flag(0x68)),
    ln.cape_ne_chest_1: LocationData(rn.cape_cave, RomLoc(0x04, 0x5D97), Flag(0x69)),
    ln.cape_ne_chest_2: LocationData(rn.cape_cave, RomLoc(0x04, 0x5DA8), Flag(0x6A)),
    ln.cape_ne_chest_3: LocationData(rn.cape_cave, RomLoc(0x04, 0x5DB9), Flag(0x6B)),
    ln.cape_mid_chest: LocationData(rn.cape_cave, RomLoc(0x04, 0x5DCA), Flag(0x6C)),
    
    # Ghost Ship
    ln.ghost_ship_boss_defeated: LocationData(rn.ghost_ship, 0, Flag(0x75)),
    ln.ghost_ship_capt_quarters_chest: LocationData(rn.ghost_ship, RomLoc(0x04, 0x5F02), Flag(0x76)),
    ln.ghost_ship_1f_vase_1: LocationData(rn.ghost_ship, RomLoc(0x04, 0x6015), Flag(0xE7)),
    ln.ghost_ship_1f_vase_2: LocationData(rn.ghost_ship, RomLoc(0x04, 0x6026), Flag(0xE8)),
    ln.ghost_ship_1f_mid_barrel: LocationData(rn.ghost_ship, RomLoc(0x04, 0x604F), Flag(0xE9)),
    ln.ghost_ship_1f_ne_barrel: LocationData(rn.ghost_ship, RomLoc(0x04, 0x6060), Flag(0xEA)),
    ln.ghost_ship_2f_hidden_chest_1: LocationData(rn.ghost_ship, RomLoc(0x04, 0x6071), Flag(0xEB)),
    ln.ghost_ship_2f_hidden_chest_2: LocationData(rn.ghost_ship, RomLoc(0x04, 0x6082), Flag(0xEC)),
    ln.ghost_ship_2f_hidden_chest_3: LocationData(rn.ghost_ship, RomLoc(0x04, 0x6093), Flag(0xED)),
    ln.ghost_ship_2f_center_chest: LocationData(rn.ghost_ship, RomLoc(0x04, 0x60A4), Flag(0xEE)),
    ln.ghost_ship_deck_w_barrel: LocationData(rn.ghost_ship, RomLoc(0x04, 0x60B5), Flag(0xEF)),
    ln.ghost_ship_deck_e_barrel: LocationData(rn.ghost_ship, RomLoc(0x04, 0x60C6), Flag(0xF0)),
    ln.ghost_ship_1f_s_vase: LocationData(rn.ghost_ship, RomLoc(0x04, 0x6037), Flag(0xF2)),
   
    # Lighthouse
    ln.lighthouse_chest: LocationData(rn.lighthouse, RomLoc(0x04, 0x5F2A), Flag(0x79)),
    
    # Volcano
    ln.volcano_har_mirror: LocationData(rn.volcano, 0, Flag(0x5F)),
    ln.volcano_b2f_chest_1: LocationData(rn.volcano, RomLoc(0x04, 0x5F97), Flag(0xE0)),
    ln.volcano_b2f_chest_2: LocationData(rn.volcano, RomLoc(0x04, 0x5FA8), Flag(0xE1)),
    ln.volcano_b2f_s_chest_1: LocationData(rn.volcano, RomLoc(0x04, 0x5FB9), Flag(0xE2)),
    ln.volcano_b2f_s_chest_2: LocationData(rn.volcano, RomLoc(0x04, 0x5FCA), Flag(0xE3)),
    ln.volcano_b2f_s_chest_3: LocationData(rn.volcano, RomLoc(0x04, 0x5FDB), Flag(0xE4)),
    ln.volcano_b3f_lava_chest_1: LocationData(rn.volcano, RomLoc(0x04, 0x5FF3), Flag(0xE5)),
    ln.volcano_b3f_lava_chest_2: LocationData(rn.volcano, RomLoc(0x04, 0x6004), Flag(0xE6)),
    
    # ==== Ice World ==== #
    # Norden
    ln.norden_boss_defeated: LocationData(rn.norden, 0, Flag(0x94)),
    ln.norden_vase: LocationData(rn.norden, RomLoc(0x13, 0x4C85), Flag(0x1E6)),

    # Spirit's Spring
    # TODO: In Game Modification 
    #ln.spirit_spring_chest: LocationData(rn.spirit_spring, RomLoc(0x13, 0x5883), Flag(0x80)),
    #ln.spirit_spring_boss_defeated (0x1E4)
    #ln.spirit_spring_sky_shield    (0x1E5)
    
    # Gold Mine
    ln.gold_mine_chest: LocationData(rn.gold_mine, RomLoc(0x13, 0x5071), Flag(0x84)),
    ln.gold_mine_boss_defeated: LocationData(rn.gold_mine, 0, Flag(0x86)),
    
    # Weston
    ln.weston_barrel: LocationData(rn.weston, RomLoc(0x13, 0x52AD), Flag(0x1E7)),
    
    # Westania Castle
    ln.westania_castle_boss_defeated: LocationData(rn.westania_castle, 0, Flag(0x9D)),
    
    # Southern Forest
    # TODO: In Game Modification 
    #ln.southern_forest_soul: LocationData(rn.southern_forest, RomLoc(0x0F, 0x70D8), Flag(0x9B)),
    
    # Estria
    ln.estria_boss_defeated: LocationData(rn.estria, 0, Flag(0x1E2)),
    
    # Eastern Mountains
    # TODO: In Game Modification
    #ln.eastern_mountain_sleep_herb: LocationData(rn.eastern_mountain, RomLoc(0x13, 0x583D), Flag(0x9F)),
    #ln.eastern_mountain_chest (0x1E0)
    
    # Lake Tower
    ln.lake_tower_1f_right_chest: LocationData(rn.lake_tower, RomLoc(0x13, 0x58B1), Flag(0x1E9)),
    ln.lake_tower_1f_left_chest: LocationData(rn.lake_tower, RomLoc(0x13, 0x58C2), Flag(0x1EA)),
    ln.lake_tower_2f_left_chest: LocationData(rn.lake_tower, RomLoc(0x13, 0x58D3), Flag(0x1EB)),
    ln.lake_tower_2f_right_chest: LocationData(rn.lake_tower, RomLoc(0x13, 0x58E4), Flag(0x1EC)),
    ln.lake_tower_4f_left_chest: LocationData(rn.lake_tower, RomLoc(0x13, 0x58F5), Flag(0x1ED)),
    ln.lake_tower_4f_right_chest: LocationData(rn.lake_tower, RomLoc(0x13, 0x5906), Flag(0x1EE)),
    ln.lake_tower_5f_left_chest: LocationData(rn.lake_tower, RomLoc(0x13, 0x5817), Flag(0x1EF)),
    ln.lake_tower_5f_right_chest: LocationData(rn.lake_tower, RomLoc(0x13, 0x5928), Flag(0x1F0)),
    
    # ==== Sky World ==== #
    # Fhunt
    # TODO: In Game Modification
    #ln.fhunt_gravestone: LocationData(rn.fhunt, RomLoc(0x13, 0x4351), Flag(0xA7)),
    
    # Sage Tower
    ln.sage_tower_1f_chest: LocationData(rn.sage_tower, RomLoc(0x13, 0x4301), Flag(0xA1)),
    ln.sage_tower_4f_chest_1: LocationData(rn.sage_tower, RomLoc(0x13, 0x4319), Flag(0xA2)),
    # TODO: In Game Modification
    #ln.sage_tower_4f_chest_2: LocationData(rn.sage_tower, 0, Flag(0xA3)),
    
    # Mad Condor's Nest
    ln.nest_boss_defeated: LocationData(rn.nest, 0, Flag(0xA8)),
    ln.nest_chest: LocationData(rn.nest, RomLoc(0x13, 0x44D0), Flag(0xAA)),
    
    # Small Cave
    ln.small_cave_e_chest: LocationData(rn.small_cave, RomLoc(0x13, 0x4718), Flag(0xAB)),
    ln.small_cave_w_chest: LocationData(rn.small_cave, RomLoc(0x13, 0x4729), Flag(0xAC)),
    ln.small_cave_boss_defeated: LocationData(rn.small_cave, 0, Flag(0xAE)),
    
    # Wind Tower
    ln.wind_tower_chest: LocationData(rn.wind_tower, RomLoc(0x13, 0x4750), Flag(0xAF)),
    
    # Graveyard
    ln.graveyard_boss_defeated: LocationData(rn.graveyard, 0, Flag(0xB4)),    
    ln.graveyard_chest: LocationData(rn.graveyard, RomLoc(0x13, 0x47D7), Flag(0xB5)),
    
    # Hitano Castle
    ln.hitano_castle_vase: LocationData(rn.hitano_castle, RomLoc(0x13, 0x486A), Flag(0x200)),
    
    # Demon Castle
    ln.demon_castle_1f_chest: LocationData(rn.demon_castle, RomLoc(0x13, 0x48A5), Flag(0xBC)),
    ln.demon_castle_b1f_chest: LocationData(rn.demon_castle, RomLoc(0x13, 0x48B6), Flag(0xBD)),
    ln.demon_castle_b2f_chest: LocationData(rn.demon_castle, RomLoc(0x13, 0x48CE), Flag(0xBE)),
    ln.demon_castle_b4f_chest: LocationData(rn.demon_castle, RomLoc(0x13, 0x48DF), Flag(0xBF)),
    ln.demon_castle_boss_defeated: LocationData(rn.demon_castle, 0, Flag(0xC1)),
    # TODO: In Game Modification
    #ln.demon_castle_boss_gift: LocationData(rn.demon_castle, RomLoc(0x0F, 0x547E, Flag(0xC2)),
    
    # ==== Limbo World ==== #
    ln.darck_manor_boss_defeated: LocationData(rn.darck_manor, 0, Flag(0xD1)),
    
    # ==== Elf World ==== #
    # West Forest
    ln.west_forest_boss_defeated: LocationData(rn.west_forest, 0, Flag(0x14B)),
    
    # Elven Village
    ln.elven_village_nw_vase_1: LocationData(rn.elven_village, RomLoc(0x04, 0x6F25), Flag(0x153)),
    ln.elven_village_nw_vase_2: LocationData(rn.elven_village, RomLoc(0x04, 0x6F36), Flag(0x154)),
    ln.elven_village_ne_vase: LocationData(rn.elven_village, RomLoc(0x04, 0x6F47), Flag(0x155)),
    
    # East Forest
    ln.east_forest_boss_defeated: LocationData(rn.east_forest, 0, Flag(0x151)),
    ln.east_forest_entrance_chest: LocationData(rn.east_forest, RomLoc(0x04, 0x6F66), Flag(0x156)),
    ln.east_forest_back_w_chest: LocationData(rn.east_forest, RomLoc(0x04, 0x6F77), Flag(0x157)),
    ln.east_forest_back_e_chest: LocationData(rn.east_forest, RomLoc(0x04, 0x6F88), Flag(0x158)),
    
    # ==== Lonely World ==== #
    # Kiral's House
    ln.kiral_house_vase: LocationData(rn.kiral_house, RomLoc(0x04, 0x70A7), Flag(0x15B)),
    # TODO: In Game Modification
    #ln.kiral_house_gift: LocationData(rn.kiral_house, RomLoc(0x04, 0x7011), Flag(0x165)),
    
    # Kiral's Basement
    ln.kiral_basement_barrel: LocationData(rn.kiral_basement, RomLoc(0x04, 0x70D4), Flag(0x15C)),
    # TODO: In Game Modification
    #ln.kiral_basement_main_barrel: LocationData(rn.kiral_basement, RomLoc(0x04, 0x7188), Flag(0x164)),
    
    # ==== Travel World ==== # 
    # Miagen# TODO: In Game Modification
    #ln.miagen_old_lady_gift: LocationData(rn.miagen, RomLoc(0x04, 0x72F7), Flag(0x1BF)),
    ln.miagen_nw_vase: LocationData(rn.miagen, RomLoc(0x04, 0x7673), Flag(0x1C8)),
    ln.miagen_se_vase: LocationData(rn.miagen, RomLoc(0x04, 0x7684), Flag(0x1C9)),
    
    # Traveler's Hut
    ln.traveler_hut_vase: LocationData(rn.traveler_hut, RomLoc(0x04, 0x76AA), Flag(0x1CA)),
    
    # Dark Tower
    # TODO: In Game Modification
    #ln.dark_tower_entrance_chest: LocationData(rn.dark_tower, RomLoc(0x04, 0x7647), Flag(0x1BC)),
    ln.dark_tower_boss_defeated: LocationData(rn.dark_tower, 0, Flag(0x1C3)),
    ln.dark_tower_1f_chest: LocationData(rn.dark_tower, RomLoc(0x04, 0x76C2), Flag(0x1CB)),
    ln.dark_tower_3f_chest: LocationData(rn.dark_tower, RomLoc(0x04, 0x76E9), Flag(0x1CC)),
    ln.dark_tower_5f_chest: LocationData(rn.dark_tower, RomLoc(0x04, 0x76FA), Flag(0x1CD)),
    ln.dark_tower_7f_chest: LocationData(rn.dark_tower, RomLoc(0x04, 0x770B), Flag(0x1CE)),
    
    # ==== Brawn World ==== #
    ln.brawn_tower_2f_chest_1: LocationData(rn.brawn_tower, RomLoc(0x04, 0x776A), Flag(0x1D5)),
    ln.brawn_tower_2f_chest_2: LocationData(rn.brawn_tower, RomLoc(0x04, 0x777B), Flag(0x1D6)),
    ln.brawn_tower_2f_chest_3: LocationData(rn.brawn_tower, RomLoc(0x04, 0x778C), Flag(0x1D8)),
    ln.brawn_tower_3f_chest_1: LocationData(rn.brawn_tower, RomLoc(0x04, 0x779D), Flag(0x1DA)),
    ln.brawn_tower_3f_chest_2: LocationData(rn.brawn_tower, RomLoc(0x04, 0x77AE), Flag(0x1DB)),
    ln.brawn_tower_3f_chest_3: LocationData(rn.brawn_tower, RomLoc(0x04, 0x77BF), Flag(0x1DC)),
    ln.brawn_tower_4f_chest_1: LocationData(rn.brawn_tower, RomLoc(0x04, 0x77D0), Flag(0x1DE)),
    ln.brawn_tower_4f_chest_2: LocationData(rn.brawn_tower, RomLoc(0x04, 0x77E1), Flag(0x1DF)),
    ln.brawn_tower_4f_chest_3: LocationData(rn.brawn_tower, RomLoc(0x04, 0x77F2), Flag(0x169)),
    ln.brawn_tower_5f_chest_1: LocationData(rn.brawn_tower, RomLoc(0x04, 0x7803), Flag(0x16B)),
    ln.brawn_tower_5f_chest_2: LocationData(rn.brawn_tower, RomLoc(0x04, 0x7814), Flag(0x16C)),
    ln.brawn_tower_5f_chest_3: LocationData(rn.brawn_tower, RomLoc(0x04, 0x7825), Flag(0x16D)),
    ln.brawn_tower_6f_chest_1: LocationData(rn.brawn_tower, RomLoc(0x04, 0x7836), Flag(0x16F)),
    ln.brawn_tower_6f_chest_2: LocationData(rn.brawn_tower, RomLoc(0x04, 0x7847), Flag(0x170)),
    ln.brawn_tower_6f_chest_3: LocationData(rn.brawn_tower, RomLoc(0x04, 0x7858), Flag(0x171)),
    ln.brawn_tower_6f_chest_4: LocationData(rn.brawn_tower, RomLoc(0x04, 0x7869), Flag(0x172)),
    
    # ==== Baffle World ==== #
    ln.baffle_tower_2f_chest_1: LocationData(rn.baffle_tower, RomLoc(0x04, 0x78C8), Flag(0x174)),
    ln.baffle_tower_2f_chest_2: LocationData(rn.baffle_tower, RomLoc(0x04, 0x78D9), Flag(0x175)),
    ln.baffle_tower_2f_chest_3: LocationData(rn.baffle_tower, RomLoc(0x04, 0x78EA), Flag(0x176)),
    ln.baffle_tower_3f_chest_1: LocationData(rn.baffle_tower, RomLoc(0x04, 0x78FB), Flag(0x179)),
    ln.baffle_tower_3f_chest_2: LocationData(rn.baffle_tower, RomLoc(0x04, 0x790C), Flag(0x17A)),
    ln.baffle_tower_3f_chest_3: LocationData(rn.baffle_tower, RomLoc(0x04, 0x791D), Flag(0x17B)),
    ln.baffle_tower_4f_chest_1: LocationData(rn.baffle_tower, RomLoc(0x04, 0x792E), Flag(0x17D)),
    ln.baffle_tower_4f_chest_2: LocationData(rn.baffle_tower, RomLoc(0x04, 0x793F), Flag(0x17E)),
    ln.baffle_tower_4f_chest_3: LocationData(rn.baffle_tower, RomLoc(0x04, 0x7950), Flag(0x17F)),
    ln.baffle_tower_5f_chest_1: LocationData(rn.baffle_tower, RomLoc(0x04, 0x7961), Flag(0xD6)),
    ln.baffle_tower_5f_chest_2: LocationData(rn.baffle_tower, RomLoc(0x04, 0x7972), Flag(0xD7)),
    ln.baffle_tower_5f_chest_3: LocationData(rn.baffle_tower, RomLoc(0x04, 0x7983), Flag(0xD8)),
    ln.baffle_tower_6f_chest_1: LocationData(rn.baffle_tower, RomLoc(0x04, 0x7994), Flag(0xDA)),
    ln.baffle_tower_6f_chest_2: LocationData(rn.baffle_tower, RomLoc(0x04, 0x79A5), Flag(0xDB)),
    ln.baffle_tower_6f_chest_3: LocationData(rn.baffle_tower, RomLoc(0x04, 0x79B6), Flag(0xDC)),
    ln.baffle_tower_6f_chest_4: LocationData(rn.baffle_tower, RomLoc(0x04, 0x79C7), Flag(0xDD)),
    
    # ==== Baffle World ==== #
    ln.soul_tower_2f_chest_1: LocationData(rn.soul_tower, RomLoc(0x04, 0x7A1F), Flag(0xF5)),
    ln.soul_tower_2f_chest_2: LocationData(rn.soul_tower, RomLoc(0x04, 0x7A30), Flag(0xF6)),
    ln.soul_tower_2f_chest_3: LocationData(rn.soul_tower, RomLoc(0x04, 0x7A41), Flag(0xF7)),
    ln.soul_tower_3f_chest_1: LocationData(rn.soul_tower, RomLoc(0x04, 0x7A52), Flag(0xF9)),
    ln.soul_tower_3f_chest_2: LocationData(rn.soul_tower, RomLoc(0x04, 0x7A63), Flag(0xFA)),
    ln.soul_tower_3f_chest_3: LocationData(rn.soul_tower, RomLoc(0x04, 0x7A74), Flag(0xFB)),
    ln.soul_tower_4f_chest_1: LocationData(rn.soul_tower, RomLoc(0x04, 0x7A85), Flag(0xFD)),
    ln.soul_tower_4f_chest_2: LocationData(rn.soul_tower, RomLoc(0x04, 0x7A96), Flag(0xFE)),
    ln.soul_tower_4f_chest_3: LocationData(rn.soul_tower, RomLoc(0x04, 0x7AA7), Flag(0xFF)),
    ln.soul_tower_5f_chest_1: LocationData(rn.soul_tower, RomLoc(0x04, 0x7AB8), Flag(0x1F3)),
    ln.soul_tower_5f_chest_2: LocationData(rn.soul_tower, RomLoc(0x04, 0x7AC9), Flag(0x1F4)),
    ln.soul_tower_5f_chest_3: LocationData(rn.soul_tower, RomLoc(0x04, 0x7ADA), Flag(0x1F5)),
    ln.soul_tower_6f_chest_1: LocationData(rn.soul_tower, RomLoc(0x04, 0x7AEB), Flag(0x1F7)),
    ln.soul_tower_6f_chest_2: LocationData(rn.soul_tower, RomLoc(0x04, 0x7AFC), Flag(0x1F8)),
    ln.soul_tower_6f_chest_3: LocationData(rn.soul_tower, RomLoc(0x04, 0x7B0D), Flag(0x1F9)),
    ln.soul_tower_6f_chest_4: LocationData(rn.soul_tower, RomLoc(0x04, 0x7B1E), Flag(0x1FA))
}

i = 1
for loc_name, loc_data in location_data.items():
    if loc_data.rom_addr is not None:
        loc_data.address = i
        i += 1

lookup_location_to_id = {loc_name: loc_data.address for loc_name, loc_data in location_data.items()}
