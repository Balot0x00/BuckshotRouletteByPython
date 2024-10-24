"""
根据道具效果对玩家状态进行修改
涉及到使用对象, 需要对Use*额外添加一个对象参数
"""

from loguru import logger as log
from .GameControl import PlayerInit, RoundInit
from .PropEffect import *
from .config import dct_actions, dct_action_other, dct_action_all
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
        self.currnet_player = self.ActionSwitch()

    def LifeCheck(self):
        """
        检查当前玩家生命状态
        """
        result = False
        if self.currnet_player.life <= 0:
            log.warning(f"玩家 {self.currnet_player.name} 死亡")
            # self.players.remove(self.currnet)
            self.currnet_player = self.ActionSwitch()
        else:
            result = True

        return result

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
        self.currnet_player = current_player

        return current_player

    def ShowTarget(self) -> List[int]:
        """
        展示当前可选玩家下标, 0 为当前玩家

        [0, 1, 3]
        """
        lct_value_players = [
            self.players.index(player) for player in self.players if self.LifeCheck()
        ]
        current_player = self.players.index(self.currnet_player)
        lct_value_players.pop(current_player)
        lct_value_players.insert(0, 0)
        log.debug(f"可选玩家 {lct_value_players}")

        return lct_value_players

    def SwitchTarget(self) -> PlayerInit:
        """
        切换指定目标
        """
        target_input = int(input(f"请选择目标: "))
        while target_input not in self.ShowTarget():
            log.warning(f"目标无效, 请重新选择")
            target_input = int(input(f"请选择目标: "))

        target = self.players[int(target_input)]
        log.debug(f"目标 {target.name}")
        return target

    def UseProp(self, p_slelect: str):
        """
        使用道具
        """
        action = dct_actions.get(p_slelect)
        action_other = dct_action_other.get(p_slelect)
        action_all = dct_action_all.get(p_slelect)

        if callable(action):
            log.debug(f"道具有效")
            action(self.currnet_player, self.round)

        elif callable(action_other):
            log.debug(f"对敌道具有效")
            target_obj = self.SwitchTarget()
            action_other(self.currnet_player, self.round, target_obj)

        elif callable(action_all):
            log.debug(f"全场道具有效")
            target_obj = self.SwitchTarget()
            action_all(self.currnet_player, self.round, target_obj)

        else:
            log.warning(f"道具无效")
