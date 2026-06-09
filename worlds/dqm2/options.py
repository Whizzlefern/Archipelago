from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, Toggle


class GameVersion(Choice):
    """
    Which version of the game you're playing.
    """
    display_name = "Game Version"
    option_cobi = 0
    option_tara = 1
    default = 0

class Goal(Choice):
    """
    Pick your victory condition.

    Darck: Defeat Darck at Darck Manor
    """
    disply_name = "Goal"
    option_darck = 0
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

class Character(Choice):
    """
    Which character do you want to play as?
    """
    display_name = "Character"
    option_cobi = 0
    option_tara = 1
    default = 0

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

@dataclass
class DQM2Options(PerGameCommonOptions):
    game_version: GameVersion
    goal: Goal
    randomize_keys: RandomizeKeys
    better_join_rate: BetterJoinRate
    character: Character
    randomize_encounters: RandomizeEncounters