import random
from loguru import logger as log

from .RandomSelect import RandomSelectTools


def RandomToolNum() -> int:
    """
    随机发放道具数量 1-5
    :return: {num:tool}
    """
    result = random.randint(1, 5)
    # log.debug(f"道具数量: {result}")
    return result


def RandomLife() -> int:
    """
    本次随机生命 2-4

    :param: l 生命
    :return:
    """
    result = random.randint(1, 4)
    log.debug(f"本局生命: {result}")
    return result


def TheGun():
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


class GunInit:
    """
    一次 gun 的初始化，生成道具组和弹夹
    """

    def __init__(self):
        self.props_num = RandomToolNum()
        self.gun = TheGun()
        # self.props = RandomSelectTools(props_num)


class RoundInit:
    """
    一次回合的初始化, 绑定弹夹信息, 设定血量上限
    """

    def __init__(self):
        gun = GunInit()
        self.gun = gun.gun
        # self.props = RandomSelectTools(gun.props_num)
        # self.props = gun.props
        self.props_num = gun.props_num
        self.max = RandomLife()
        self.life = self.max
        self.gun_tag = 1


class PlayerInit:
    def __init__(self, round: RoundInit):
        self.id: int = 1
        self.name: str = "playername"
        self.life = round.life
        self.props = RandomSelectTools(round.props_num)

        # 状态标志位 alive slience dead
        self.status = "alive"


class NPCInit(PlayerInit):
    """
    NPC 初始化, NPC单独初始化, 当前NPC 的行动完全随机, 不获取round内的信息
    """

    def __init__(self, round: RoundInit):
        self.id: int = 0
        self.name: str = "NPC"
        self.life = round.life
        self.props = RandomSelectTools(round.props_num)
        self.status = "alive"


from .config import dct_actions
from .LogControl import PrintStatus


class PlayerActions:
    """
    玩家行动
    """

    def __init__(
        self,
        player: PlayerInit,
        round: RoundInit,
        # gun: GunInit,
    ) -> None:
        self.player = player
        self.round = round

    def NewGun(self, player: PlayerInit, round: RoundInit):
        """
        设置新弹夹, 继承上一个弹夹的剩余道具
        """
        log.info(f"重新填充弹夹")
        newgun = GunInit()
        round.gun = newgun.gun
        # player.round = newgun.gun
        old_props = player.props
        new_props = old_props + newgun.props
        player.props = new_props[0:8]

    def GunCheck(self):
        if len(self.round.gun) == 0:
            self.NewGun(self.player, self.round)
        pass

    def LifeCheck(self):
        if self.player.life <= 0:
            log.warning(f"玩家 {self.player.name} 死亡")
            return False
        # if self.player.life >= self.round.max:
        #     self.player.life = self.round.max
        #     log.warning(f"玩家 {self.player.name} 生命上限")
        #     return False
        return True

    def PropsCheck(self, num):
        props_key = [a.split(":")[0] for a in self.player.props]
        if num == "0":
            return True
        if num not in props_key:
            log.warning(f"玩家 {self.player.name} 使用道具 {num} 无效")
            return False

        return True

    def PropsRemove(self, num):
        for a in self.player.props:
            if num in a:
                self.player.props.remove(a)
        return

    def UseProp(self, num):
        """
        使用道具
        """
        # log.debug(f"玩家 {self.player.name} 使用道具 {num}")
        # if num in
        # log.debug(f"道具列表: {self.player.props}")

        # 使用道具前, 玩家状态检查
        if not self.LifeCheck():
            return
        if not self.PropsCheck(num):
            return

        action = dct_actions.get(num, None)
        if callable(action):
            action(self.player, self.round)

        else:
            log.warning(f"玩家 {self.player.name} 使用道具 {num} 无效")

        # 道具使用后, 移除道具
        self.PropsRemove(num)

        # 使用道具后, 检查状态
        if self.LifeCheck():
            self.GunCheck()
            PrintStatus(self.player)

        return
