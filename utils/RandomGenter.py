"""
随机生成器, 控制对局内, life, tool_num, tools, gun 的生成
"""

import random
from collections import Counter
from typing import List
from loguru import logger as log
# 
from .config import dct_tools

def RandomLife() -> int:
    """
    本次随机生命 2-4

    :param: l 生命
    :return:
    """
    result = random.randint(1, 4)
    log.debug(f"本局生命: {result}")
    return result


def RandomToolNum() -> int:
    """
    随机发放道具数量 1-5
    :return: {num:tool}
    """
    result = random.randint(1, 5)
    # log.debug(f"道具数量: {result}")
    return result



def RandmonSelector(lst, k) -> list:
    """
    从道具池抽取道具
    """
    # 将每个元素最多重复两次加入新列表
    extended_list = [item for item in lst for _ in range(2)]

    # 使用 Counter 确保结果中不会有超过两个的重复元素
    selection = []
    while len(selection) < k:
        item = random.choice(extended_list)
        if Counter(selection)[item] < 2:  # 确保每个元素不会超过 2 次
            selection.append(item)
    return selection


def RandomSelectTools(k: int) -> List[str]:
    """
    随机发放道具 1-5
    :return: {num:tool}
    """
    r = RandmonSelector(list(dct_tools.keys()), k)

    # 生成多个道具时, 可能出现重复的道具, 改用list字典表示
    result = []
    for i in r:
        result.append(str(i) + ":" + dct_tools[i])
    return result

def RandomGunLoad():
    """
    准备弹夹
    总计8发子弹, 随机填充n发, 空包弹 0, 实弹 1 当前排列 2
    实弹 1-4
    """
    num = random.randint(2, 8)
    num_ones = random.randint(1, int(num / 2))
    # log.debug(f"子弹总数: {num} 实弹数量: {num_ones}")
    # 创建包含 num_ones 个 1 和 8 - num_ones 个 0 的列表
    lst = [1] * num_ones + [0] * (num - num_ones)
    # log.debug(f"生成子弹lst: {lst}")

    # 打乱列表顺序，使 1 和 0 随机分布
    result = random.shuffle(lst)
    log.debug(f"子弹总数: {num} 实弹数量: {num_ones} 子弹分布: {lst}")
    return lst