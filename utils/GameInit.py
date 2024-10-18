import random
from loguru import logger as log

from .RandomSelect import RandomSelectTools


def RandomToolNum() -> int:
    """
    随机发放道具数量 1-5
    :return: {num:tool}
    """
    result = random.randint(1, 5)
    log.debug(f"道具数量: {result}")
    return result


def RandomLife() -> int:
    """
    本次随机生命 1-4

    :param: l 生命
    :return:
    """
    result = random.randint(1, 4)
    log.debug(f"本局生命: {result}")
    return result


def TheGun():
    """
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


class GunInit:
    """
    一次 gun 的初始化，控制道具数量和子弹状态。
    """

    def __init__(self):
        self.tools_num = RandomToolNum()
        self.gun = TheGun()  # 假设 TheGun() 已经初始化好


class RoundInit:
    """
    一次回合的初始化。
    """

    def __init__(self, gun: GunInit):
        self.gun = gun.gun
        self.props = RandomSelectTools(gun.tools_num)
        self.life = RandomLife()


class PlayerInit:
    def __init__(self, round: RoundInit):
        self.id: int = 0
        self.name: str = ""
        self.life = round.life
        self.props = round.props
        # self.round = round
