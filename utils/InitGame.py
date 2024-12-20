from loguru import logger as log

from utils.RandomGenter import RandomSelectTools, RandomToolNum
from utils.RandomGenter import RandomGunLoad, RandomLife
from utils.Base import BaseGun, BaseRound

class GunInit(BaseGun):
    """
    一次 gun 的初始化，生成道具组和弹夹
    """

    def __init__(self):
        self.props_num = RandomToolNum()
        self.gun = RandomGunLoad()


class RoundInit(BaseRound):
    """
    一次回合的初始化, 绑定弹夹信息, 设定血量上限
    """

    def __init__(self):
        gun = GunInit()
        self.gun = gun.gun
        self.props_num = gun.props_num
        self.life_max = RandomLife()
        self.life = self.life_max
        self.gun_tag = 1
