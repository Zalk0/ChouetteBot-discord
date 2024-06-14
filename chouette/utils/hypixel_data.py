async def experience_to_level(type_xp: str, xp_amount: float) -> float:
    """
    Calcule le niveau correspondant à une quantité donnée de XP cumulative.

    Args:
        type_xp (str): Le type d'XP pour lequel calculer le niveau (compétence, type de tueur, donjon). Pour `slayer_type`, utilisez l'un des suivants: slayer_zombie, slayer_spider, slayer_web, slayer_vampire.
        xp_amount (float): La quantité d'XP cumulée.

    Returns:
        level (float): Le niveau correspondant à la quantité donnée d'XP cumulée.
    """
    skill_xp_data: list[tuple(int, int)] = [
        (0, 0),
        (1, 50),
        (2, 175),
        (3, 375),
        (4, 675),
        (5, 1175),
        (6, 1925),
        (7, 2925),
        (8, 4425),
        (9, 6425),
        (10, 9925),
        (11, 14925),
        (12, 22425),
        (13, 32425),
        (14, 47425),
        (15, 67425),
        (16, 97425),
        (17, 147425),
        (18, 222425),
        (19, 322425),
        (20, 522425),
        (21, 822425),
        (22, 1222425),
        (23, 1722425),
        (24, 2322425),
        (25, 3022425),
        (26, 3822425),
        (27, 4722425),
        (28, 5722425),
        (29, 6822425),
        (30, 8022425),
        (31, 9322425),
        (32, 10722425),
        (33, 12222425),
        (34, 13822425),
        (35, 15522425),
        (36, 17322425),
        (37, 19222425),
        (38, 21222425),
        (39, 23322425),
        (40, 25522425),
        (41, 27822425),
        (42, 30222425),
        (43, 32722425),
        (44, 35322425),
        (45, 38072425),
        (46, 40972425),
        (47, 44072425),
        (48, 47472425),
        (49, 51172425),
        (50, 55172425),
        (51, 59472425),
        (52, 64072425),
        (53, 68972425),
        (54, 74122425),
        (55, 79672425),
        (56, 85472425),
        (57, 91572425),
        (58, 97572425),
        (59, 104672425),
        (60, 111672425),
        (61, 10e24),
    ]
    dungeon_xp_data: list[tuple(int, int)] = [
        (0, 0),
        (1, 50),
        (2, 125),
        (3, 235),
        (4, 395),
        (5, 625),
        (6, 955),
        (7, 1425),
        (8, 2095),
        (9, 3045),
        (10, 4385),
        (11, 6275),
        (12, 8940),
        (13, 12700),
        (14, 17960),
        (15, 25340),
        (16, 35640),
        (17, 50040),
        (18, 70040),
        (19, 97640),
        (20, 135640),
        (21, 188140),
        (22, 259640),
        (23, 356640),
        (24, 488640),
        (25, 668640),
        (26, 911640),
        (27, 1239640),
        (28, 1684640),
        (29, 2284640),
        (30, 3084640),
        (31, 4149640),
        (32, 5559640),
        (33, 7459640),
        (34, 9959640),
        (35, 13259640),
        (36, 17559640),
        (37, 23159640),
        (38, 30359640),
        (39, 39559640),
        (40, 51559640),
        (41, 66559640),
        (42, 85559640),
        (43, 109559640),
        (44, 139559640),
        (45, 177559640),
        (46, 225559640),
        (47, 285559640),
        (48, 360559640),
        (49, 453559640),
        (50, 569809640),
        (51, 10e24),
    ]
    slayer_xp_data: list[list[tuple(int, int)]] = [
        [
            (0, 0),
            (1, 5),
            (2, 15),
            (3, 200),
            (4, 1000),
            (5, 5000),
            (6, 20000),
            (7, 100000),
            (8, 400000),
            (9, 1000000),
        ],
        [
            (0, 0),
            (1, 5),
            (2, 25),
            (3, 200),
            (4, 1000),
            (5, 5000),
            (6, 20000),
            (7, 100000),
            (8, 400000),
            (9, 1000000),
        ],
        [
            (0, 0),
            (1, 10),
            (2, 30),
            (3, 250),
            (4, 1500),
            (5, 5000),
            (6, 20000),
            (7, 100000),
            (8, 400000),
            (9, 1000000),
        ],
        [
            (0, 0),
            (1, 20),
            (2, 75),
            (3, 240),
            (4, 840),
            (5, 2400),
        ],
    ]

    # Skill XP data
    if type_xp == "skill":
        xp_data = skill_xp_data
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
    # Dungeon XP data
    elif type_xp == "dungeon":
        xp_data = dungeon_xp_data
    else:
        raise ValueError(f"Unknown type of XP: {type_xp}")

    for i in range(len(xp_data) - 1):
        current_level, current_xp = xp_data[i]
        next_level, next_xp = xp_data[i + 1]
        if xp_amount <= next_xp:
            return current_level + (xp_amount - current_xp) / (next_xp - current_xp)
    return xp_data[-1][0]
