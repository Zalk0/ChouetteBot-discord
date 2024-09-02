from typing import Optional


def experience_to_level(
    type_xp: str, xp_amount: float, max_level: Optional[int] = None
) -> (float, float):
    """
    Calcule le niveau correspondant à une quantité donnée d'expérience cumulative.

    Args:
        type_xp: Le type d'expérience pour lequel calculer le niveau (compétence, type de slayer, donjon).
            Pour `slayer_type`, utilisez l'un des suivants: slayer_zombie, slayer_spider, slayer_web, slayer_vampire.
        xp_amount: La quantité d'expérience cumulée.
        max_level: Le niveau maximum

    Returns:
        level: Le niveau correspondant à la quantité donnée d'expérience cumulée.
    """
    skill_xp_data: list[int] = [
        0,
        50,
        175,
        375,
        675,
        1175,
        1925,
        2925,
        4425,
        6425,
        9925,
        14925,
        22425,
        32425,
        47425,
        67425,
        97425,
        147425,
        222425,
        322425,
        522425,
        822425,
        1222425,
        1722425,
        2322425,
        3022425,
        3822425,
        4722425,
        5722425,
        6822425,
        8022425,
        9322425,
        10722425,
        12222425,
        13822425,
        15522425,
        17322425,
        19222425,
        21222425,
        23322425,
        25522425,
        27822425,
        30222425,
        32722425,
        35322425,
        38072425,
        40972425,
        44072425,
        47472425,
        51172425,
        55172425,
        59472425,
        64072425,
        68972425,
        74172425,
        79672425,
        85472425,
        91572425,
        97972425,
        104672425,
        111672425,
    ]
    dungeon_xp_data: list[int] = [
        0,
        50,
        125,
        235,
        395,
        625,
        955,
        1425,
        2095,
        3045,
        4385,
        6275,
        8940,
        12700,
        17960,
        25340,
        35640,
        50040,
        70040,
        97640,
        135640,
        188140,
        259640,
        356640,
        488640,
        668640,
        911640,
        1239640,
        1684640,
        2284640,
        3084640,
        4149640,
        5559640,
        7459640,
        9959640,
        13259640,
        17559640,
        23159640,
        30359640,
        39559640,
        51559640,
        66559640,
        85559640,
        109559640,
        139559640,
        177559640,
        225559640,
        285559640,
        360559640,
        453559640,
        569809640,
    ]
    # Common part for the slayer levels
    common_slayer_xp_data: list[int] = [
        200,
        1000,
        5000,
        20000,
        100000,
        400000,
        1000000,
    ]
    slayer_xp_data: tuple[list[int], list[int], list[int], list[int]] = (
        [
            0,
            5,
            15,
            *common_slayer_xp_data,
        ],
        [
            0,
            5,
            25,
            *common_slayer_xp_data,
        ],
        [
            0,
            10,
            30,
            250,
            1500,
            *common_slayer_xp_data[2:],
        ],
        [
            0,
            20,
            75,
            240,
            840,
            2400,
        ],
    )

    # Skill XP data
    if type_xp == "skill":
        xp_data = skill_xp_data
    # Dungeon XP data
    elif type_xp == "dungeon":
        xp_data = dungeon_xp_data
    # Slayer XP data
    # Slayer Zombie
    elif type_xp == "slayer_zombie":
        xp_data = slayer_xp_data[0]
    # Slayer Spider
    elif type_xp == "slayer_spider":
        xp_data = slayer_xp_data[1]
    # Slayer Wolf/Enderman/Blaze
    elif type_xp == "slayer_web":
        xp_data = slayer_xp_data[2]
    # Slayer Vampire
    elif type_xp == "slayer_vampire":
        xp_data = slayer_xp_data[3]
    else:
        raise ValueError(f"Unknown type of XP: {type_xp}")

    for level, xp in enumerate(xp_data):
        if max_level and level == max_level and xp_amount > xp:
            return max_level, xp_amount - xp
        if xp_amount <= xp:
            previous_xp = xp_data[level - 1]
            return level - 1 + (xp_amount - previous_xp) / (xp - previous_xp), None
    return len(xp_data) - 1, xp_amount - xp_data[-1]
