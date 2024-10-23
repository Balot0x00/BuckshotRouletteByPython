"""
根据道具效果对玩家状态进行修改
涉及到使用对象, 需要对Use*额外添加一个对象参数
"""

from loguru import logger as log
from .GameControl import PlayerInit, RoundInit
from .PropEffect import *
from .config import dct_actions, dct_actionsv2
from .GameControl import PlayerActions


# Python < 3.9 版本中不能直接使用 list[PlayerInit]作为类型注解
from typing import List


class PlayerActionsSoloMatch:
    """玩家行动管理"""

    def __init__(self, players: List[PlayerInit], round: RoundInit) -> None:
        """
        初始化玩家行动管理类。

        :param players: 包含多个 PlayerInit 对象的列表
        :param round: 当前回合的 RoundInit 对象
        """
        self.players = players  # 玩家列表
        self.round = round  # 当前回合
        self.flag = 0
        self.currnet = self.ActionSwitch()

    def ActionSwitch(self) -> PlayerInit:
        """
        切换行动玩家
        """
        log.debug(f"当前标志位 {self.flag}")

        current_player = self.players[self.flag]
        self.flag += 1
        if self.flag >= len(self.players):
            self.flag = 0
        log.debug(f"切换标志位 {self.flag}")
        self.currnet = current_player

        return current_player

    def ShowTarget(self):
        """
        展示当前玩家外, 剩余玩家下标
        """
        lct_value_players = [self.players.index(player) for player in self.players]

        current_player = self.players.index(self.currnet)
        lct_value_players.pop(current_player)
        log.debug(lct_value_players)

        return lct_value_players

    def UseProp(self, p_slelect: str):
        """
        使用道具
        """
        action = dct_actions.get(p_slelect)
        actionv2 = dct_actionsv2.get(p_slelect)

        if callable(action):
            log.debug(f"道具有效")
        elif callable(actionv2):
            log.debug(f"对敌道具有效")

            actionv2(self.currnet, self.round, target="")
        else:
            log.warning(f"道具无效")
