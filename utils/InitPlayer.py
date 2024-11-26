from .InitGame import (
    RoundInit,
    RandomSelectTools,
    RandomToolNum,
    RandomGunLoad,
    RandomLife,
)


class PlayerInit:
    def __init__(self, round: RoundInit):
        self.id: int = 1
        self.name: str = "playername"
        self.life = round.life
        self.props = RandomSelectTools(round.props_num)

        # 状态标志位 alive slience dead
        self.status = "alive"
        # 添加局内编号
        self.round_id = "1"


class NPCInit(object):
    """
    NPC 初始化, NPC单独初始化, 当前NPC 的行动完全随机, 不获取round内的信息
    """

    def __init__(self, round: RoundInit):
        self.id: int = 0
        self.name: str = "NPC"
        self.life = round.life
        self.props = RandomSelectTools(round.props_num)
        self.status = "alive"
        # 先赋予0号, 根据玩家数量进行修改
        self.round_id = "0"