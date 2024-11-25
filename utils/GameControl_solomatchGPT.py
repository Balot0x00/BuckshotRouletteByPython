from loguru import logger as log
from typing import List
from collections import Counter
from .GameControl import PlayerInit, RoundInit, GunInit
from .PropEffect import *
from .config import dct_actions, dct_action_other, dct_action_all
from .GameControl import PlayerActions
from .RandomGenter import RandomSelectTools


class PlayerActionsSoloMatch:
    """玩家行动管理"""

    def __init__(self, players: List[PlayerInit], round: RoundInit) -> None:
        self.players = players  # 玩家列表
        self.round = round  # 当前回合
        self.switch = 0  # 标志位
        self.currnet_player = self.ActionSwitch()  # 初始玩家

    def GunNew(self):
        """重新填充弹夹"""
        log.info("重新填充弹夹")
        new_gun = GunInit()
        self.round.gun = new_gun.gun
        self.round.props_num = new_gun.props_num

        log.debug("为所有玩家添加道具")
        for player in self.players:
            new_props = RandomSelectTools(self.round.props_num)
            player.props = (player.props + new_props[:8])[:8]

    def GunCheck(self):
        """弹夹检查"""
        if len(self.round.gun) == 0:
            self.GunNew()

    def CheckPlayerState(self) -> bool:
        """
        检查当前玩家生命状态和行动状态
        :return: 是否可以继续行动
        """
        if self.currnet_player.life <= 0:
            log.warning(f"玩家 {self.currnet_player.name} 死亡")
            self.currnet_player.status = "dead"
            self.ActionSwitch()
            return False
        elif self.currnet_player.status in ["dead", "slience"]:
            log.warning(
                f"玩家 {self.currnet_player.name} 行动无效 ({self.currnet_player.status})"
            )
            self.ActionSwitch()
            return False
        return True

    def RoundCheck(self) -> bool:
        """对局状态检查，是否有玩家胜出"""
        lst_life = [player.life for player in self.players]
        vitory = Counter(lst_life)
        return vitory[1] == 1

    def ActionSwitch(self) -> PlayerInit:
        """切换行动玩家"""
        log.debug(f"当前标志位 {self.switch}")
        self.currnet_player = self.players[self.switch]
        self.switch = (self.switch + 1) % len(self.players)
        log.debug(f"切换标志位 {self.switch}")
        return self.currnet_player

    def ShowTarget(self, filter_status: List[str]) -> List[int]:
        """
        展示符合条件的目标, 不包括当前玩家
        :param filter_status: 过滤条件
        :return: 目标玩家列表
        """
        lst_targets = [
            idx
            for idx, player in enumerate(self.players)
            if player.status in filter_status
        ]
        current_idx = self.players.index(self.currnet_player)
        lst_targets.remove(current_idx)
        return lst_targets

    def SwitchTarget(self) -> PlayerInit:
        """切换指定目标"""
        available_targets = self.ShowTarget(["alive", "slience"])
        target_input = int(input(f"请选择目标 {available_targets}: "))
        while target_input not in available_targets:
            log.warning("目标无效, 请重新选择")
            target_input = int(input(f"请选择目标 {available_targets}: "))
        return self.players[target_input]

    def UseProps(self, prop_select: str):
        """使用道具"""
        action = dct_actions.get(prop_select)
        action_other = dct_action_other.get(prop_select)
        action_all = dct_action_all.get(prop_select)

        if not self.CheckPlayerState():
            return

        if callable(action):
            log.debug("道具有效")
            action(self.currnet_player, self.round)
        elif callable(action_other):
            log.debug("交互道具, 需选择目标")
            target_obj = self.SwitchTarget()
            action_other(self.currnet_player, self.round, target_obj)
        elif callable(action_all):
            log.debug("全体作用道具")
            target_obj = self.SwitchTarget()
            bullet = action_all(self.currnet_player, self.round, target_obj)

            if bullet == 0 and target_obj == self.currnet_player:
                log.info(f"玩家 {self.currnet_player.name} 自空枪")
            else:
                self.ActionSwitch()
        else:
            log.warning("道具无效")

        if self.currnet_player.status == "slience":
            self.currnet_player.status = "alive"
