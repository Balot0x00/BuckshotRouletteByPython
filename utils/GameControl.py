import random
from loguru import logger as log

from utils.InitPlayer import PlayerInit
from utils.InitGame import RoundInit, GunInit
from utils.ConsolePrint import PrintStatus

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
        new_props = old_props + player.props
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
        props_key = [str(a.split(":")[0]) for a in self.player.props]
        if num == "0":
            return True
        if not num  in props_key:
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
        from utils.DctProps import dct_actions,dct_action_shot

        # 使用道具前, 玩家状态检查
        if not self.LifeCheck():
            return
        if not self.PropsCheck(num):
            return

        action = dct_actions.get(num, None)
        action_2 = dct_action_shot.get(num, None)
        if callable(action):
            action(self.player, self.round)

        if callable(action_2):
            action_2(self.player, self.round)

        else:
            log.warning(f"玩家 {self.player.name} 使用道具 {num} 无效")

        # 道具使用后, 移除道具
        self.PropsRemove(num)

        # 使用道具后, 检查状态
        if self.LifeCheck():
            self.GunCheck()
            PrintStatus(self.player)

        return
