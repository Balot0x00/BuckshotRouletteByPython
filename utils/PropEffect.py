"""
生成道具效果, 不进行效果附加
"""

import random


def TheMedicine() -> int:
    """
    过期药品, +2 or -1 生命
    0 失败 1 成功

    :param: l 生命
    :return:

    """
    result = 0
    r = random.choice([0, 1])
    if r == 0:
        result = 2
    else:
        result = -1
    return result


def TheCiga() -> int:
    """
    香烟效果 生命+1 总量 <=4
    """
    result = 1
    return result


def TheSkit():
    """
    手锯 双倍伤害
    """

    return 2
