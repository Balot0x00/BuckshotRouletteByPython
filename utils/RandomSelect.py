import random
from collections import Counter
from loguru import logger as log


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


def RandomSelectTools(k: int):
    """
    随机发放道具 1-5
    :return: {num:tool}
    """
    # log.debug(f"抽取道具数量:{k}")
    dct_tools = {
        1: "香烟",
        2: "过期药品",
        3: "啤酒",
        4: "放大镜",
        5: "逆转器",
        6: "肾上腺素",
        7: "短锯",
        8: "神秘电话",
        9: "手铐",
    }
    # k = random.randint(1, 5)
    r = RandmonSelector(list(dct_tools.keys()), k)

    # 生成多个道具时, 可能出现重复的道具, 改用list字典表示
    result = []
    for i in r:
        result.append(str(i) + ":" + dct_tools[i])
    return result
