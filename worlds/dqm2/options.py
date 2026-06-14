from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, Toggle, OptionGroup, Range


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

class RandomizeLevelSkills(Toggle):
    """
    Randomizes the skills monster learn on level up.
    """
    display_name = "Randomize Level Up Skills"
    default = 1

class BetterJoinRate(Toggle):
    """
    Makes monsters more likely to join you.
    """
    display_name = "Better Join Rate"
    default = 1

class RandomizeEncounters(Choice):
    """
    Randomize Encounters.
    *** Not currently implemented, all monsters are randomized always with no restrictions.

    Vanilla: Encounters are the same as vanilla.
    Randomized No Boss: Encounters are random, but excludes ??? monsters.
    Randomized: Encounters are random.
    """
    display_name = "Randomize Encounters"
    option_vanilla = 0
    option_randomized_no_boss = 1
    option_randomized = 2
    default = 1

class FourSkills(Toggle):
    """
    Forces all encounters to have four.
    This means monsters that join you will be stronger, but so will your enemies.
    """
    display_name = "Force Four Skills"
    default = 0

class EXPMultiplier(Range):
    """
    Multiplies experience gained from battles.
    200 = 2x, 300 = 3x, etc
    """
    display_name = "Experience Multiplier"
    range_start = 100
    range_end = 300
    default = 150

@dataclass
class DQM2Options(PerGameCommonOptions):
    goal: Goal
    game_version: GameVersion
    character: Character
    randomize_keys: RandomizeKeys
    randomize_level_skills: RandomizeLevelSkills
    better_join_rate: BetterJoinRate
    randomize_encounters: RandomizeEncounters
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
        BetterJoinRate
    ]),

    OptionGroup("Encounter Settings", [
        RandomizeEncounters,
        FourSkills,
        EXPMultiplier
    ])

    # OptionGroup("Cosmetic Settings", [
    #
    # ])
]