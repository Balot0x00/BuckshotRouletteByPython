"""
根据道具效果对玩家状态进行修改
涉及到使用对象, 需要对Use*额外添加一个对象参数
"""

from loguru import logger as log
from .GameControl import PlayerInit, RoundInit, GunInit
from .PropEffect import *
from .config import dct_actions, dct_action_other, dct_action_all
from .GameControl import PlayerActions
from .RandomSelect import RandomSelectTools


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
        # 切换标志位
        self.switch = 0
        self.currnet_player = self.ActionSwitch()

    def GunNew(self):
        log.info(f"重新填充弹夹")
        gun_new = GunInit()
        self.round.gun = gun_new.gun
        self.round.props_num = gun_new.props_num

        log.debug(f"为所有玩家添加道具")
        for player in self.players:
            props_new = RandomSelectTools(self.round.props_num)
            props_old = player.props
            props = props_old + props_new[0:8]
            player.props = props

    def GunCheck(self):
        """
        弹夹检查
        """
        if len(self.round.gun) == 0:
            self.GunNew()

    def LifeCheck(self):
        """
        检查当前玩家生命状态
        """
        result = False
        if self.currnet_player.life <= 0:
            log.warning(f"玩家 {self.currnet_player.name} 死亡")
            self.currnet_player.status = "dead"
            # self.players.remove(self.currnet)
            self.currnet_player = self.ActionSwitch()
        else:
            result = True
        return result

    def ActionCheck(self):
        """
        检查当前玩家行动状态,
        """
        result = True
        if self.currnet_player.status == "dead":
            log.warning(f"玩家 {self.currnet_player.name} 已死亡")
            self.currnet_player = self.ActionSwitch()
            result = False

        elif self.currnet_player.status == "slience":
            log.warning(f"玩家 {self.currnet_player.name} 已沉默")
            self.currnet_player = self.ActionSwitch()
            result = False
        return result

    def ActionSwitch(self) -> PlayerInit:
        """
        切换行动玩家
        """
        log.debug(f"当前标志位 {self.switch}")

        current_player = self.players[self.switch]
        self.switch += 1
        if self.switch >= len(self.players):
            self.switch = 0
        log.debug(f"切换标志位 {self.switch}")
        self.currnet_player = current_player

        return current_player

    def ShowTargetUnSlience(self) -> List[int]:
        """
        展示非沉默目标, 不包括当前玩家
        """
        lst_unslience_players = [
            self.players.index(player)
            for player in self.players
            if player.status == "alive"
        ]
        current_player = self.players.index(self.currnet_player)
        lst_unslience_players.pop(current_player)
        return lst_unslience_players

    def ShowTargetGun(self) -> List[int]:
        """
        展示当前alive alience, 0 为当前玩家

        [0, 1, 3]
        """
        lst_alive_players = [
            self.players.index(player)
            for player in self.players
            if player.status == "alive" or player.status == "slience"
        ]
        current_player = self.players.index(self.currnet_player)
        lst_alive_players.pop(current_player)
        lst_alive_players.insert(0, 0)
        log.debug(f"可选玩家 {lst_alive_players}")

        return lst_alive_players

    def SwitchTarget(self) -> PlayerInit:
        """
        切换指定目标
        """
        target_input = int(input(f"请选择目标: "))
        while target_input not in self.ShowTargetGun():
            log.warning(f"目标无效, 请重新选择")
            target_input = int(input(f"请选择目标: "))

        target = self.players[int(target_input)]
        log.debug(f"目标 {target.name}")
        return target

    def UseProps(self, p_slelect: str):
        """
        使用道具
        """
        action = dct_actions.get(p_slelect)
        action_other = dct_action_other.get(p_slelect)
        action_all = dct_action_all.get(p_slelect)

        if self.ActionCheck():
            if callable(action) and self.ActionCheck():
                log.debug(f"道具有效")
                action(self.currnet_player, self.round)

            elif callable(action_other):
                log.debug(f"交互道具, 对非当前 + alive 玩家生效")
                target_obj = self.SwitchTarget()
                action_other(self.currnet_player, self.round, target_obj)

            elif callable(action_all):
                log.debug(f"使用0号道具, 对alive slience生效")
                target_obj = self.SwitchTarget()
                buttle = action_all(self.currnet_player, self.round, target_obj)

                # 自空枪判断
                if buttle == 0 and target_obj == self.currnet_player:
                    log.info(f"玩家 {self.currnet_player.name} 自空枪")
                else:
                    self.ActionSwitch()
            else:
                log.warning(f"道具无效")
        else:
            log.warning(f"玩家 {self.currnet_player.name} 行动无效")

        # 重置slience 状态
        if self.currnet_player.status == "slience":
            self.currnet_player.status = "alive"
