from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, Toggle, OptionGroup, Range, DefaultOnToggle, OptionSet


class Goal(Choice):
    """
    Pick your victory condition.

    Darck: Defeat Darck at Darck Manor
    """
    disply_name = "Goal"
    option_darck = 0
    default = 0


class GameVersion(Choice):
    """
    Which version of the game you're playing.
    """
    display_name = "Game Version"
    option_cobi = 0
    option_tara = 1
    default = 0


class Character(Choice):
    """
    Which character do you want to play as?
    """
    display_name = "Character"
    option_cobi = 0
    option_tara = 1
    default = 0


class RandomizeKeys(Choice):
    """
    Randomize World Keys into the pool.
    *** Not currently implemented. Leave on none

    None: Keys are in their vanilla locations.
    Shuffle: Keys are shuffled with each other.
    Anywhere: Keys are found anywhere.
    """
    display_name = "Randomize Keys"
    option_none = 0
    # option_shuffle = 1
    # option_anywhere = 2
    default = 0


class RandomizeLevelSkills(DefaultOnToggle):
    """
    Randomizes the skills monster learn on level up.
    """
    display_name = "Randomize Level Up Skills"


class BetterJoinRate(DefaultOnToggle):
    """
    Makes monsters more likely to join you.
    """
    display_name = "Better Join Rate"


class RandomizeEXPGrowth(Choice):
    """
    Randomize how quickly monsters gain exp.

    Vanilla: EXP Growth is unchanged.
    Randomized: EXP Growth is randomized.
    Fast: EXP Growth is randomized, but only fast growth rates are selected.
    """
    display_name = "Randomize EXP Growth"
    option_vanilla = 0
    option_randomized = 1
    option_fast = 2
    default = 0


class RandomizeStatGrowths(Toggle):
    """
    Randomize monster stat growths.
    """
    display_name = "Randomize Stat Growths"


class RandomizeEncounters(DefaultOnToggle):
    """
    Randomize Encounters.
    *** Not currently implemented, all monsters are randomized always with no restrictions.
    """
    display_name = "Randomize Encounters"


class AllowedMonsters(OptionSet):
    """
    Sets which monsters are allowed to be randomized.
    If left blank, all monsters are allowed.

    You can select any family name, such as "Material", or species names such as "Mimic".
    Use "Slime (Family)" or "Slime (Species)" for Slime.
    Use "Dragon (Family)" or "Dragon (Species)" for Dragon.
    """
    display_name = "Allowed Monsters for Randomization"
    valid_keys = frozenset(
        ["Slime (Family)", "Dragon (Family)", "Beast", "Bird", "Plant", "Bug", "Devil", "Zombie", "Material", "Water",
         "???", "DrakSlime", "SpotSlime", "WingSlime", "TreeSlime", "Snaily", "SlimeNite", "Babble", "BoxSlime",
         "PearlGel", "Slime (Species)", "Healer", "FangSlime", "RockSlime", "SlimeBorg", "Slabbit", "KingSlime",
         "Metaly", "Metabble", "SpotKing", "TropicGel", "MimeSlime", "HaloSlime", "MetalKing", "GoldSlime", "GranSlime",
         "WonderEgg", "DragonKid", "Tortragon", "Pteranod", "Gasgon", "FairyDrak", "LizardMan", "Poisongon", "Swordgon",
         "Drygon", "Dragon (Species)", "MiniDrak", "MadDragon", "Rayburn", "Chamelgon", "LizardFly", "Andreal",
         "KingCobra", "Vampirus", "SnakeBat", "Spikerous", "GreatDrak", "Crestpent", "WingSnake", "Coatol", "Orochi",
         "BattleRex", "SkyDragon", "Serpentia", "Divinegon", "Orligon", "GigaDraco", "Tonguella", "Almiraj", "Catfly",
         "PillowRat", "Saccer", "GulpBeast", "Skullroo", "WindBeast", "Beavern", "Anteater", "SuperTen", "IronTurt",
         "Mommonja", "HammerMan", "Grizzly", "Yeti", "ArrowDog", "NoctoKing", "BeastNite", "MadGopher", "FairyRat",
         "Unicorn", "Goategon", "WildApe", "Trumpeter", "KingLeo", "DarkHorn", "MadCat", "BigEye", "Gorago", "CatMage",
         "Dumbira", "Picky", "Wyvern", "BullBird", "FloraJay", "DuckKite", "MadPecker", "MadRaven", "MistyWing",
         "AquaHawk", "Dracky", "KiteHawk", "BigRoost", "StubBird", "LandOwl", "MadGoose", "MadCondor", "Emyu",
         "Blizzardy", "Phoenix", "ZapBird", "Garudian", "WhipBird", "FunkyBird", "RainHawk", "Azurile", "Shantak",
         "CragDevil", "MadPlant", "FireWeed", "FloraMan", "WingTree", "CactiBall", "Gulpple", "Toadstool", "AmberWeed",
         "Slurperon", "StubSuck", "Oniono", "DanceVegi", "TreeBoy", "Devipine", "FaceTree", "HerbMan", "BeanMan",
         "EvilSeed", "ManEater", "Snapper", "GhosTree", "Rosevine", "Egdracil", "Warubou", "Watabou", "Eggplaton",
         "FooHero", "GiantSlug", "Catapila", "Gophecada", "Butterfly", "WeedBug", "GiantWorm", "Lipsy", "StagBug",
         "Pyuro", "ArmyAnt", "GoHopper", "TailEater", "ArmorPede", "Eyeder", "GiantMoth", "Droll", "ArmyCrab",
         "MadHornet", "Belzebub", "WarMantis", "HornBeet", "Sickler", "Armorpion", "Digster", "Skularach", "MultiEyes",
         "Pixy", "MedusaEye", "AgDevil", "Demonite", "DarkEye", "EyeBall", "SkulRider", "EvilBeast", "Bubblemon",
         "1EyeClown", "Gremlin", "ArcDemon", "Lionex", "GoatHorn", "Orc", "Ogre", "GateGuard", "ChopClown", "BossTroll",
         "Grendal", "Akubar", "MadKnight", "EvilWell", "Gigantes", "Centasaur", "EvilArmor", "Jamirus", "Durran",
         "Titanis", "LampGenie", "Spooky", "Skullgon", "Putrepup", "RotRaven", "Mummy", "DarkCrab", "DeadNite",
         "Shadow", "Skulpent", "Hork", "Mudron", "NiteWhip", "WindMerge", "Reaper", "Inverzon", "FoxFire", "CaptDead",
         "DeadNoble", "WhiteKing", "BoneSlave", "Skeletor", "Servant", "Lazamanus", "Copycat", "MadSpirit", "PomPomBom",
         "Niterich", "JewelBag", "EvilWand", "MadCandle", "CoilBird", "Facer", "SpikyBoy", "MadMirror", "RogueNite",
         "Puppetor", "Goopi", "Voodoll", "MetalDrak", "Balzak", "SabreMan", "CurseLamp", "Brushead", "Roboster",
         "Roboster2", "EvilPot", "Gismo", "LavaMan", "IceMan", "Mimic", "Exaucers", "MudDoll", "Golem", "StoneMan",
         "BombCrag", "GoldGolem", "DarkMate", "ProtoMech", "CloudKing", "Petiteel", "Moray", "WalrusMan", "RayGigas",
         "Anemon", "Aquarella", "Merman", "Octokid", "PutreFish", "Octoreach", "Angleron", "FishRider", "RushFish",
         "Gamanian", "Clawster", "CancerMan", "RogueWave", "Scallopa", "SeaHorse", "HoodSquid", "MerTiger", "AxeShark",
         "Octogon", "KingSquid", "Digong", "WhaleMage", "Aquadon", "Octoraid", "Grakos", "Poseidon", "Pumpoise",
         "Starfish", "DracoLord", "DracoLord1", "LordDraco", "Hargon", "Sidoh", "Genosidoh", "Baramos", "Zoma",
         "AsuraZoma", "Pizzaro", "PsychoPiz", "Esterk", "Mirudraas1", "Mirudraas2", "Mudou", "DeathMore1", "DeathMore2",
         "DeathMore3", "DarkDrium", "Orgodemir", "Orgodemir2", "Darck", "Lamia", "Dimensaur", "Kagebou"])
    default = []


class FourSkills(Toggle):
    """
    Forces all encounters to have four.
    This means monsters that join you will be stronger, but so will your enemies.
    """
    display_name = "Force Four Skills"


class EXPMultiplier(Range):
    """
    Multiplies experience gained from battles.
    200 = 2x, 300 = 3x, etc
    """
    display_name = "Experience Multiplier"
    range_start = 100
    range_end = 300
    default = 100


@dataclass
class DQM2Options(PerGameCommonOptions):
    goal: Goal
    game_version: GameVersion
    character: Character
    randomize_keys: RandomizeKeys
    randomize_level_skills: RandomizeLevelSkills
    better_join_rate: BetterJoinRate
    randomize_exp_growth: RandomizeEXPGrowth
    randomize_stat_growths: RandomizeStatGrowths
    randomize_encounters: RandomizeEncounters
    allowed_monsters: AllowedMonsters
    four_skills: FourSkills
    exp_multiplier: EXPMultiplier


dqm2_option_groups = [
    OptionGroup("Logic Settings", [
        Goal,
        GameVersion,
        Character
    ]),

    OptionGroup("Item Settings", [
        RandomizeKeys
    ]),

    OptionGroup("Monster Settings", [
        RandomizeLevelSkills,
        BetterJoinRate,
        RandomizeEXPGrowth,
        RandomizeStatGrowths
    ]),

    OptionGroup("Encounter Settings", [
        RandomizeEncounters,
        AllowedMonsters,
        FourSkills,
        EXPMultiplier
    ])

    # OptionGroup("Cosmetic Settings", [
    #
    # ])
]
