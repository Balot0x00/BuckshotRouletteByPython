"""
根据道具效果对玩家状态进行修改
涉及到使用对象, 需要对Use*额外添加一个对象参数
"""

from loguru import logger as log
from utils.GameControl import RoundInit, GunInit
from utils.PropEffect import *
from utils.DctProps import dct_actions, dct_action_other, dct_action_shot,dct_action_adrenaline
from utils.RandomGenter import RandomSelectTools
from utils.util import UserInput
from utils.InitPlayer import PlayerInit


# Python < 3.9 版本中不能直接使用 list[PlayerInit]作为类型注解
from typing import List


class PlayerActionsSoloMatch:
    """玩家行动管理"""

    def __init__(self, players: List[PlayerInit], round: RoundInit) -> None:
        """
        初始化玩家行动管理类。对玩家进行局内编号

        :param players: 包含多个 PlayerInit 对象的列表
        :param round: 当前回合的 RoundInit 对象
        """
        self.players = players  # 玩家列表
        self.PlayerReNumber()
        self.round = round  # 当前回合
        # 当前行动玩家数组下标
        self.action_num = 0
        #  从1号玩家开始行动
        self.current_player = players[0]

    def PlayerReNumber(self):
        """
        对玩家局内编号, 玩家赋予1号, NPC赋予末尾号
        """
        for i, player in enumerate(self.players):
            player.round_id = str(i+1)

    def GetPropList(self) -> List[str]:
        """
        获取当前玩家的道具列表, 追加 0 号道具
        """
        lt = [tool_num.split(":")[0] for tool_num in self.current_player.props]
        lt.insert(0, "0")
        return lt

    def GunNew(self):
        log.info(f"重新填充弹夹")
        gun_new = GunInit()
        self.round.gun = gun_new.gun
        self.round.props_num = gun_new.props_num

        # 清台
        log.debug(f"a new gun, clear all props")
        for player in self.players:
            player.props = []

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

    def CheckPlayerState(self) -> bool:
        """
        检查当前玩家生命状态和行动状态, 切换行动玩家。
        :return: None
        """
        result_check = True
        log.debug(
            f"检查玩家 {self.current_player.name} 状态 {self.current_player.status}"
        )

        if self.current_player.life <= 0:
            log.warning(f"玩家 {self.current_player.name} 死亡")
            self.current_player.status = "dead"
            # self.ActionSwitch()
            result_check = False
        elif self.current_player.status in ["dead", "slience"]:
            log.warning(
                f"玩家 {self.current_player.name} 行动无效: {self.current_player.status}"
            )
            # self.ActionSwitch()
            # slience 状态切换
            if self.current_player.status == "slience":
                self.current_player.status = "alive"
            result_check = False

        if result_check == False:
            self.ActionSwitch()
        

    def CheckVirtoy(self):
        """
        对局状态检查, 是否有玩家胜出
        """
        from collections import Counter

        result = False
        lst_life = [player.life for player in self.players]
        vitory = Counter(lst_life)
        log.debug(f"玩家存活状态 {vitory}")
        if vitory[0] == len(self.players)-1:
            result = True

        return result

    def ActionSwitch(self) -> PlayerInit:
        """
        切换行动玩家
        """
        log.debug(f"当前玩家数组下标: players {self.action_num}")

        # current_player = self.players[self.switch]
        self.action_num += 1
        if self.action_num >= len(self.players):
            self.action_num = 0
        log.debug(f"切换下标: players {self.action_num}")
        self.current_player = self.players[self.action_num]

        # return

    def PlayersShow(self, filter_status: List[str]) -> List[int]:
        """
        根据筛选条件展示目标
        alive: 返回非沉默死亡玩家, 使用9号道具
        alive, slience: 返回非死亡玩家, 使用0号道具
        """
        # current_player = self.players.index(self.current_player)

        lst_target = [
            player.round_id
            for player in self.players
            if player.status in filter_status
        ]
        lst_target.remove(self.current_player.round_id)
        if "slience" in filter_status:
            lst_target.insert(0, "0")
        print(f"可选玩家 {lst_target}")
        return lst_target

    def PlayersSelect(self, filter_status: List[str]) -> PlayerInit:
        """
        切换指定目标,
        """
        lst_target = self.PlayersShow(filter_status)
        target_input = int(UserInput("选择目标: ", lst_target))

        # 使用偏移后的数组下标表示目标玩家, 或遍历rid, 判断与输入一致的玩家
        if not target_input == 0:
            num_offset = target_input - 1
            log.debug(f"非0, 下标偏移: {num_offset}")
            target = self.players[int(num_offset)]
        else:
            num_offset = 0
            target = self.current_player

        log.debug(f"目标 {target.name}")
        return target

    def RemoveTool(self, tool_num: str):
        """
        移除道具
        """
        log.debug(f"移除道具 {tool_num}")
        for tool in self.current_player.props:
            if tool_num in tool:
                break
        try:
            self.current_player.props.remove(tool)
        except:
            log.warning(f"道具不存在")

    def UseProps(self, p_slelect: str):
        """
        使用道具
        """
        action = dct_actions.get(p_slelect)
        action_other = dct_action_other.get(p_slelect)
        action_shot = dct_action_shot.get(p_slelect)
        action_adrenaline = dct_action_adrenaline.get(p_slelect)

        if callable(action):
            log.debug(f"道具有效")
            action(self.current_player, self.round)
            self.RemoveTool(p_slelect)

        elif callable(action_other):
            log.debug(f"交互道具, 对非当前 + alive 玩家生效")
            target_obj = self.PlayersSelect(["alive"])
            if len(target_obj) ==0:
                log.warning(f"无有效目标")
                return
            action_other(self.current_player, self.round, target_obj)
            self.RemoveTool(p_slelect)

        elif callable(action_shot):
            log.debug(f"使用0号道具, 对alive slience生效")
            target_obj = self.PlayersSelect(["alive", "slience"])
            buttle = action_shot(self.current_player, self.round, target_obj)
            log.info(f"{self.current_player.name} shot to {target_obj.name}")

            # 自空枪判断
            if buttle == 0 and target_obj == self.current_player:
                log.info(f"玩家 {self.current_player.name} 自空枪")
            else:
                self.ActionSwitch()
        elif callable(action_adrenaline):
            log.debug(f"使用6号道具, 对alive/slience生效")
            target_obj = self.PlayersSelect(["alive", "slience"])
            prop_num = action_adrenaline(self.current_player, self.round,target_obj)
            # 选择道具后直接使用
            self.RemoveTool(p_slelect)
            self.UseProps(prop_num)
            self.ActionSwitch()
        else:
            log.warning(f"道具无效")
