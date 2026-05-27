from __future__ import annotations

from typing import Dict, Optional, TYPE_CHECKING

from BaseClasses import Entrance, Region

from .items import DQM2Item
from .locations import DQM2Location, location_data
from .names import entrance_names as en, region_names as rn

if TYPE_CHECKING:
    from .world import DQM2World


class DQM2Region(Region):
    game = "Dragon Quest Monsters 2"

def create_regions(world: DQM2World) -> None:
    # GreatLog
    greatlog_region = create_region(world, rn.greatlog)
    
    # Oasis World
    oasis_region = create_region(world, rn.oasis_world)
    kalka_region = create_region(world, rn.kalka)
    asiya_region = create_region(world, rn.asiya)
    canal_region = create_region(world, rn.canal)
    mirage_lake_region = create_region(world, rn.mirage_lake)
    
    # Pirate World
    pirate_region = create_region(world, rn.pirate_world)
    yold_region = create_region(world, rn.yold)
    polona_region = create_region(world, rn.polona)
    mermaid_region = create_region(world, rn.mermaid)
    ritz_region = create_region(world, rn.ritz)
    cape_region = create_region(world, rn.cape_cave)
    ghost_ship_region = create_region(world, rn.ghost_ship)
    lighthouse_region = create_region(world, rn.lighthouse)
    volcano_region = create_region(world, rn.volcano)
    
    # Ice World
    ice_north_region = create_region(world, rn.ice_world_north)
    norden_region = create_region(world, rn.norden)
    spirit_spring_region = create_region(world, rn.spirit_spring)
    nofor_region = create_region(world, rn.nofor)
    gold_mine_region = create_region(world, rn.gold_mine)
    ice_south_region = create_region(world, rn.ice_world_south)
    weston_region = create_region(world, rn.weston)
    westania_castle_region = create_region(world, rn.westania_castle)
    southern_forest_region = create_region(world, rn.southern_forest)
    estria_region = create_region(world, rn.estria)
    eastern_mountain_region = create_region(world, rn.eastern_mountain)
    lake_tower_region = create_region(world, rn.lake_tower)
    
    # Sky World
    sky_entrance_region = create_region(world, rn.sky_world_entrance)
    fhunt_region = create_region(world, rn.fhunt)
    sage_tower_region = create_region(world, rn.sage_tower)
    bridge_pass_1_region = create_region(world, rn.bridge_pass_1)
    sky_main_region = create_region(world, rn.sky_world_main)
    pei_region = create_region(world, rn.pei)
    nest_region = create_region(world, rn.nest)
    small_cave_region = create_region(world, rn.small_cave)
    wind_tower_region = create_region(world, rn.wind_tower)
    graveyard_region = create_region(world, rn.graveyard)
    hitano_castle_region = create_region(world, rn.hitano_castle)
    demon_castle_region = create_region(world, rn.demon_castle)
    
    # Limbo World
    limbo_region = create_region(world, rn.limbo_world)
    darck_manor_region = create_region(world, rn.darck_manor)
    
    # Elf World
    elf_world_region = create_region(world, rn.elf_world)
    west_forest_region = create_region(world, rn.west_forest)
    elven_village_region = create_region(world, rn.elven_village)
    east_forest_region = create_region(world, rn.east_forest)
    
    # Lonely World
    lonely_world_region = create_region(world, rn.lonely_world)
    kiral_house_region = create_region(world, rn.kiral_house)
    kiral_basement_region = create_region(world, rn.kiral_basement)
    
    # Travel World
    travel_world_region = create_region(world, rn.travel_world)
    miagen_region = create_region(world, rn.miagen)
    traveler_hut_region = create_region(world, rn.traveler_hut)
    dark_tower_region = create_region(world, rn.dark_tower)
    
    # Brawn World
    brawn_world_region = create_region(world, rn.brawn_world)
    brawn_tower_region = create_region(world, rn.brawn_tower)
    # Baffle World
    baffle_world_region = create_region(world, rn.baffle_world)
    baffle_tower_region = create_region(world, rn.baffle_tower)
    # Soul World
    soul_world_region = create_region(world, rn.soul_world)
    soul_tower_region = create_region(world, rn.soul_tower)

    world.multiworld.regions += [
        greatlog_region,
        oasis_region,
        kalka_region,
        asiya_region,
        canal_region,
        mirage_lake_region,
        pirate_region,
        yold_region,
        polona_region,
        mermaid_region,
        ritz_region,
        cape_region,
        ghost_ship_region,
        lighthouse_region,
        volcano_region,
        ice_north_region,
        norden_region,
        spirit_spring_region,
        nofor_region,
        gold_mine_region,
        ice_south_region,
        weston_region,
        westania_castle_region,
        southern_forest_region,
        estria_region,
        eastern_mountain_region,
        lake_tower_region,
        sky_entrance_region,
        fhunt_region,
        sage_tower_region,
        bridge_pass_1_region,
        sky_main_region,
        pei_region,
        nest_region,
        small_cave_region,
        wind_tower_region,
        graveyard_region,
        hitano_castle_region,
        demon_castle_region,
        limbo_region,
        darck_manor_region,
        elf_world_region,
        west_forest_region,
        elven_village_region,
        east_forest_region,
        lonely_world_region,
        kiral_house_region,
        kiral_basement_region,
        travel_world_region,
        miagen_region,
        traveler_hut_region,
        dark_tower_region,
        brawn_world_region,
        brawn_tower_region,
        baffle_world_region,
        baffle_tower_region,
        soul_world_region,
        soul_tower_region
    ]

def connect_regions(world: DQM2World) -> None:
    # GreatLog
    connect(world, world.player, en.greatlog_to_oasis, rn.greatlog, rn.oasis_world)
    connect(world, world.player, en.greatlog_to_pirate, rn.greatlog, rn.pirate_world)
    connect(world, world.player, en.greatlog_to_ice, rn.greatlog, rn.ice_world_north)
    connect(world, world.player, en.greatlog_to_sky, rn.greatlog, rn.sky_world_entrance)
    connect(world, world.player, en.greatlog_to_limbo, rn.greatlog, rn.limbo_world)
    
    connect(world, world.player, en.greatlog_to_elf, rn.greatlog, rn.elf_world)
    connect(world, world.player, en.greatlog_to_lonely, rn.greatlog, rn.lonely_world)
    connect(world, world.player, en.greatlog_to_travel, rn.greatlog, rn.travel_world)
    connect(world, world.player, en.greatlog_to_brawn, rn.greatlog, rn.brawn_world)
    connect(world, world.player, en.greatlog_to_baffle, rn.greatlog, rn.baffle_world)
    connect(world, world.player, en.greatlog_to_soul, rn.greatlog, rn.soul_world)

    # Oasis World
    connect(world, world.player, en.oasis_to_kalka, rn.oasis_world, rn.kalka)
    connect(world, world.player, en.oasis_to_asiya, rn.oasis_world, rn.asiya)
    connect(world, world.player, en.oasis_to_mirage, rn.oasis_world, rn.mirage_lake)
    connect(world, world.player, en.kalka_to_canal, rn.kalka, rn.canal)
    
    # Pirate World
    connect(world, world.player, en.pirate_to_yold, rn.pirate_world, rn.yold)
    connect(world, world.player, en.pirate_to_polona, rn.pirate_world, rn.polona)
    connect(world, world.player, en.polona_to_mermaid, rn.polona, rn.mermaid)
    connect(world, world.player, en.pirate_to_ritz, rn.pirate_world, rn.ritz)
    connect(world, world.player, en.pirate_to_cape, rn.pirate_world, rn.cape_cave)
    connect(world, world.player, en.pirate_to_ghost_ship, rn.pirate_world, rn.ghost_ship)
    connect(world, world.player, en.pirate_to_lighthouse, rn.pirate_world, rn.lighthouse)
    connect(world, world.player, en.pirate_to_volcano, rn.pirate_world, rn.volcano)
    
    # Ice World
    connect(world, world.player, en.ice_north_to_norden, rn.ice_world_north, rn.norden)
    connect(world, world.player, en.ice_north_to_spirit_spring, rn.ice_world_north, rn.spirit_spring)
    connect(world, world.player, en.ice_north_to_nofor, rn.ice_world_north, rn.nofor)
    connect(world, world.player, en.ice_north_to_gold_mine, rn.ice_world_north, rn.gold_mine)
    connect(world, world.player, en.gold_mine_to_ice_south, rn.gold_mine, rn.ice_world_south)
    connect(world, world.player, en.ice_south_to_weston, rn.ice_world_south, rn.weston)
    connect(world, world.player, en.ice_south_to_westania_castle, rn.ice_world_south, rn.westania_castle)
    connect(world, world.player, en.ice_south_to_southern_forest, rn.ice_world_south, rn.southern_forest)
    connect(world, world.player, en.ice_south_to_estria, rn.ice_world_south, rn.estria)
    connect(world, world.player, en.ice_south_to_eastern_mountain, rn.ice_world_south, rn.eastern_mountain)
    connect(world, world.player, en.ice_north_to_lake_tower, rn.ice_world_north, rn.lake_tower)
    
    # Sky World
    connect(world, world.player, en.sky_entrance_to_fhunt, rn.sky_world_entrance, rn.fhunt)
    connect(world, world.player, en.fhunt_to_sage_tower, rn.fhunt, rn.sage_tower)
    connect(world, world.player, en.sky_entrance_to_bridge_pass_1, rn.sky_world_entrance, rn.bridge_pass_1)
    connect(world, world.player, en.bridge_pass_1_to_sky_main, rn.bridge_pass_1, rn.sky_world_main)
    connect(world, world.player, en.sky_main_to_pei, rn.sky_world_main, rn.pei)
    connect(world, world.player, en.sky_main_to_nest, rn.sky_world_main, rn.nest)
    connect(world, world.player, en.sky_main_to_small_cave, rn.sky_world_main, rn.small_cave)
    connect(world, world.player, en.sky_main_to_wind_tower, rn.sky_world_main, rn.wind_tower)
    connect(world, world.player, en.sky_main_to_graveyard, rn.sky_world_main, rn.graveyard)
    connect(world, world.player, en.sky_main_to_hitano_castle, rn.sky_world_main, rn.hitano_castle)
    connect(world, world.player, en.hitano_castle_to_demon_castle, rn.hitano_castle, rn.demon_castle)
    
    # Limbo World
    connect(world, world.player, en.limbo_to_darck_manor, rn.limbo_world, rn.darck_manor)
    
    # Elf World
    connect(world, world.player, en.elf_to_west_forest, rn.elf_world, rn.west_forest)
    connect(world, world.player, en.elf_to_elven_village, rn.elf_world, rn.elven_village)
    connect(world, world.player, en.elf_to_east_forest, rn.elf_world, rn.east_forest)
    
    # Lonely World
    connect(world, world.player, en.lonely_to_kiral_house, rn.lonely_world, rn.kiral_house)
    connect(world, world.player, en.kiral_house_to_kiral_basement, rn.kiral_house, rn.kiral_basement)
    
    # Travel World
    connect(world, world.player, en.travel_to_miagen, rn.travel_world, rn.miagen)
    connect(world, world.player, en.travel_to_traveler_hut, rn.travel_world, rn.traveler_hut)
    connect(world, world.player, en.travel_to_dark_tower, rn.travel_world, rn.dark_tower)
    
    # Brawn World
    connect(world, world.player, en.brawn_to_brawn_tower, rn.brawn_world, rn.brawn_tower)

    # Baffle World
    connect(world, world.player, en.baffle_to_baffle_tower, rn.baffle_world, rn.baffle_tower)
    
    # Soul World
    connect(world, world.player, en.soul_to_soul_tower, rn.soul_world, rn.soul_tower)


def create_region(world: DQM2World, name: str):
    ret = DQM2Region(name, world.player, world.multiworld)
    for loc_name, loc_data in location_data.items():
        if loc_data.region in name:
            location = DQM2Location(world.player, loc_name, loc_data.address, ret)
            ret.locations.append(location)

    return ret

def connect(world: DQM2World, player: int, entrance_name: str, source: str, target: str):
    source_region = world.multiworld.get_region(source, player)
    target_region = world.multiworld.get_region(target, player)

    connection = Entrance(player, entrance_name, source_region)

    source_region.exits.append(connection)
    connection.connect(target_region)

def create_events(world: DQM2World):
    mirage_lake_region = world.get_region(rn.mirage_lake)
    volcano_region = world.get_region(rn.volcano)
    spirit_spring_region = world.get_region(rn.spirit_spring)
    demon_castle_region = world.get_region(rn.demon_castle)
    darck_manor_region = world.get_region(rn.darck_manor)
    
    east_forest_region = world.get_region(rn.east_forest)
    kiral_basement_region = world.get_region(rn.kiral_basement)
    dark_tower_region = world.get_region(rn.dark_tower)

    mirage_lake_region.add_event("Oasis World Complete", "Oasis World Complete", location_type=DQM2Location, item_type=DQM2Item)
    volcano_region.add_event("Pirate World Complete", "Pirate World Complete", location_type=DQM2Location, item_type=DQM2Item)
    spirit_spring_region.add_event("Ice World Complete", "Ice World Complete", location_type=DQM2Location, item_type=DQM2Item)
    demon_castle_region.add_event("Sky World Complete", "Sky World Complete", location_type=DQM2Location, item_type=DQM2Item)
    
    east_forest_region.add_event("Elf World Complete", "Elf World Complete", location_type=DQM2Location, item_type=DQM2Item)
    kiral_basement_region.add_event("Lonely World Complete", "Lonely World Complete", location_type=DQM2Location, item_type=DQM2Item)
    dark_tower_region.add_event("Travel World Complete", "Travel World Complete", location_type=DQM2Location, item_type=DQM2Item)

    darck_manor_region.add_event("Final Boss Defeated", "Victory", location_type=DQM2Location, item_type=DQM2Item)