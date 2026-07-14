from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from rule_builder.rules import CanReachLocation, Has, HasAll, HasAny, HasFromList, Rule

from .names import entrance_names, item_names, location_names

if TYPE_CHECKING:
    from .world import DQM2World

HAS_WATER_CALL = Has(item_names.water_call)
#HAS_MOON_ROCK = Has(item_names.moon_rock)
HAS_CREST = Has(item_names.crest)
HAS_YUNA_SOUL = Has(item_names.yuna_soul)
HAS_SLEEP_HERB = Has(item_names.sleep_herb)
HAS_CHANGE_STAFF = Has(item_names.change_staff)
HAS_TIDAL_BELL = Has(item_names.tidal_bell)
HAS_HAR_MIRROR = Has(item_names.har_mirror)
HAS_SKY_SHIELD = Has(item_names.sky_shield)
HAS_HEAVEN_GEAR = Has(item_names.heaven_helmet) & Has(item_names.heaven_armor) & Has(item_names.heaven_sword)
HAS_WIZ_STONE = Has(item_names.wiz_stone)
HAS_PRETTY_RING = Has(item_names.pretty_ring)

HAS_OASIS_KEY = Has(item_names.oasis_key)
HAS_PIRATE_KEY = Has(item_names.pirate_key)
HAS_ICE_KEY = Has(item_names.ice_key)
HAS_SKY_KEY = Has(item_names.sky_key)
HAS_LIMBO_KEY = Has(item_names.limbo_key)
HAS_ELF_KEY = Has(item_names.elf_key)
HAS_LONELY_KEY = Has(item_names.lonely_key)
HAS_TRAVEL_KEY = Has(item_names.travel_key)
HAS_BRAWN_KEY = Has(item_names.brawn_key)
HAS_BAFFLE_KEY = Has(item_names.baffle_key)
HAS_SOUL_KEY = Has(item_names.soul_key)

def get_worlds_completed(state: CollectionState, world: DQM2World) -> int:
    return state.count_from_list(("Oasis World Complete",
                           "Pirate World Complete",
                           "Ice World Complete"), world.player)

def set_all_rules(world: DQM2World) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: DQM2World) -> None:
    # GreatLog
    world.set_rule(world.get_entrance(entrance_names.greatlog_to_arena), Has("Oasis World Complete"))
    world.set_rule(world.get_entrance(entrance_names.greatlog_to_residential), Has("Oasis World Complete"))
    world.set_rule(world.get_entrance(entrance_names.greatlog_to_shops), Has("Oasis World Complete"))
    world.set_rule(world.get_entrance(entrance_names.greatlog_to_stable), Has("Ice World Complete"))
    world.set_rule(world.get_entrance(entrance_names.greatlog_to_treetop), Has("Ice World Complete"))
    world.set_rule(world.get_entrance(entrance_names.greatlog_to_castle), Has("Sky World Complete"))

    # Desert World
    world.set_rule(world.get_entrance(entrance_names.oasis_to_mirage), HAS_WATER_CALL)

    # Pirate World
    world.set_rule(world.get_entrance(entrance_names.pirate_to_ghost_ship), HAS_TIDAL_BELL)
    
    can_enter_volcano = HasAll(item_names.moon_rock, item_names.tidal_bell)
    world.set_rule(world.get_entrance(entrance_names.pirate_to_volcano), can_enter_volcano)

    # Ice World
    world.set_rule(world.get_entrance(entrance_names.ice_north_to_gold_mine), HAS_HAR_MIRROR)
    world.set_rule(world.get_entrance(entrance_names.gold_mine_to_ice_south), HAS_CREST)
    
    can_enter_lake_tower = HasAll(item_names.tidal_bell, item_names.sky_shield, "Ice World Complete")
    world.set_rule(world.get_entrance(entrance_names.ice_north_to_lake_tower), can_enter_lake_tower)
    
    # Sky World
    world.set_rule(world.get_entrance(entrance_names.sky_entrance_to_bridge_pass_1), HAS_CHANGE_STAFF)
    
    can_enter_small_cave = HasAny(item_names.sky_shield, item_names.har_mirror)
    world.set_rule(world.get_entrance(entrance_names.sky_main_to_small_cave), can_enter_small_cave)
    
    world.set_rule(world.get_entrance(entrance_names.sky_main_to_wind_tower), HAS_SKY_SHIELD)
    world.set_rule(world.get_entrance(entrance_names.sky_main_to_graveyard), HAS_SKY_SHIELD)
    world.set_rule(world.get_entrance(entrance_names.hitano_to_hitano_castle), HAS_HEAVEN_GEAR)
    
    # Limbo World
    can_enter_darck_manor = HasAll(item_names.tidal_bell, item_names.har_mirror, item_names.sky_shield)
    world.set_rule(world.get_entrance(entrance_names.limbo_to_darck_manor), can_enter_darck_manor)
    
    if world.options.randomize_keys:
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_oasis), HAS_OASIS_KEY)
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_pirate), HAS_PIRATE_KEY)
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_ice), HAS_ICE_KEY)
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_sky), HAS_SKY_KEY)
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_limbo), HAS_LIMBO_KEY)
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_elf), HAS_ELF_KEY)
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_lonely), HAS_LONELY_KEY)
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_travel), HAS_TRAVEL_KEY)
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_brawn), HAS_BRAWN_KEY)
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_baffle), HAS_BAFFLE_KEY)
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_soul), HAS_SOUL_KEY)
    else:
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_pirate), Has("Oasis World Complete"))
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_ice), Has("Pirate World Complete"))
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_sky), Has("Ice World Complete"))
        world.set_rule(world.get_entrance(entrance_names.greatlog_to_limbo), Has("Sky World Complete"))
        # world.set_rule(world.get_entrance(entrance_names.greatlog_to_elf), HAS_ELF_KEY)
        # world.set_rule(world.get_entrance(entrance_names.greatlog_to_lonely), HAS_LONELY_KEY)
        # world.set_rule(world.get_entrance(entrance_names.greatlog_to_travel), HAS_TRAVEL_KEY)
        # world.set_rule(world.get_entrance(entrance_names.greatlog_to_brawn), HAS_BRAWN_KEY)
        # world.set_rule(world.get_entrance(entrance_names.greatlog_to_baffle), HAS_BAFFLE_KEY)
        # world.set_rule(world.get_entrance(entrance_names.greatlog_to_soul), HAS_SOUL_KEY)


def set_all_location_rules(world: DQM2World) -> None:
    # Greatlog
    # TODO: Do these actually require Sky World?
    world.set_rule(world.get_location(location_names.treetop_chest_1), Has("Sky World Complete"))
    world.set_rule(world.get_location(location_names.treetop_chest_2), Has("Sky World Complete"))
    world.set_rule(world.get_location(location_names.rare_key_shelf), Has("Ice World Complete"))

    # Canal
    world.set_rule(world.get_location(location_names.canal_ne_vase_1), HAS_TIDAL_BELL)
    world.set_rule(world.get_location(location_names.canal_ne_vase_2), HAS_TIDAL_BELL)
    world.set_rule(world.get_location(location_names.canal_chest_east_boss), HAS_TIDAL_BELL)
    world.set_rule(world.get_location(location_names.canal_sw_chest_1), HAS_TIDAL_BELL)
    world.set_rule(world.get_location(location_names.canal_sw_chest_2), HAS_TIDAL_BELL)

    # Cape Cave
    world.set_rule(world.get_location(location_names.cape_nw_chest), HAS_TIDAL_BELL)
    world.set_rule(world.get_location(location_names.cape_ne_chest_1), HAS_TIDAL_BELL)
    world.set_rule(world.get_location(location_names.cape_ne_chest_2), HAS_TIDAL_BELL)
    world.set_rule(world.get_location(location_names.cape_ne_chest_3), HAS_TIDAL_BELL)
    world.set_rule(world.get_location(location_names.cape_mid_chest), HAS_TIDAL_BELL)

    # Volcano
    world.set_rule(world.get_location(location_names.volcano_b2f_s_chest_1), HAS_SKY_SHIELD)
    world.set_rule(world.get_location(location_names.volcano_b2f_s_chest_2), HAS_SKY_SHIELD)
    world.set_rule(world.get_location(location_names.volcano_b2f_s_chest_3), HAS_SKY_SHIELD)

    # Spirit Spring
    can_finish_ice_world = CanReachLocation(location_names.norden_boss_defeated) & \
                           CanReachLocation(location_names.westania_castle_boss_defeated) & \
                           CanReachLocation(location_names.estria_boss_defeated)
    world.set_rule(world.get_location("Ice World Complete"), can_finish_ice_world)

    # Norden Castle
    world.set_rule(world.get_location(location_names.norden_boss_defeated), HAS_HAR_MIRROR)

    # Westania Castle
    world.set_rule(world.get_location(location_names.westania_castle_boss_defeated), HAS_YUNA_SOUL)

    # Estria
    world.set_rule(world.get_location(location_names.estria_boss_defeated), HAS_SLEEP_HERB)
            
    if world.options.goal > 0:
        # Kiral's House
        world.set_rule(world.get_location("Lonely World Complete"), HAS_WIZ_STONE)

        # Dark Tower
        world.set_rule(world.get_location(location_names.dark_tower_boss_defeated), HAS_PRETTY_RING)
        world.set_rule(world.get_location(location_names.dark_tower_1f_chest), HAS_PRETTY_RING)
        world.set_rule(world.get_location(location_names.dark_tower_3f_chest), HAS_PRETTY_RING)
        world.set_rule(world.get_location(location_names.dark_tower_5f_chest), HAS_PRETTY_RING)
        world.set_rule(world.get_location(location_names.dark_tower_7f_chest), HAS_PRETTY_RING)
        world.set_rule(world.get_location("Travel World Complete"), HAS_PRETTY_RING)

def set_completion_condition(world: DQM2World) -> None:
    world.set_completion_rule(Has("Victory"))
