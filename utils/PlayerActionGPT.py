"""
玩家行动, 行动前逻辑判断, 玩家状态判断
根据道具效果对玩家状态进行修改
"""

from loguru import logger as log
from utils import PlayerInit, RoundInit
from utils import *

# from .config import dct_actions


class PlayerActionsGPT:
    """玩家行动管理"""

    def __init__(self, player: PlayerInit, round: RoundInit) -> None:
        self.player = player
        self.round = round

    def log_player_action(self, action: str):
        """通用日志记录函数"""
        log.debug(f"玩家 {self.player.name} {action}")

    def update_player_life(self, change: int):
        """更新玩家生命值，并记录状态"""
        self.player.life += change
        self.player.life = max(0, min(self.player.life, 4))  # 生命值限制在 0 到 4 之间
        log.debug(f"玩家 {self.player.name} 当前生命: {self.player.life}")

    def UseGun(self):
        """使用枪"""
        self.log_player_action("开枪")
        bullet = self.round.gun.pop()

        if bullet == 1:
            self.update_player_life(-1)  # 生命减1
        log.debug(f"子弹 {'实弹' if bullet == 1 else '空包弹'}, 剩余子弹: {self.round.gun}")

    def UseCiga(self):
        """使用香烟"""
        life_gain = TheCiga()
        self.update_player_life(life_gain)
        log.debug(f"使用香烟, 获得生命效果: {life_gain}")

    def UseMedicine(self):
        """使用过期药品"""
        life_gain = TheMedicine()
        self.update_player_life(life_gain)
        log.debug(f"使用过期药品, 获得生命效果: {life_gain}")

        if self.player.life <= 0:
            log.warning(f"玩家 {self.player.name} 死亡")

    def UseBear(self):
        """使用啤酒"""
        self.log_player_action("使用啤酒")

    def UseMagnifier(self):
        """使用放大镜"""
        self.log_player_action("使用放大镜")

    def UseReverse(self):
        """使用逆转器"""
        self.log_player_action("使用逆转器")

    def UseAdrenaline(self):
        """使用肾上腺素"""
        self.log_player_action("使用肾上腺素")

    def UseSaw(self):
        """使用短锯"""
        self.log_player_action("使用短锯")

    def UsePhone(self):
        """使用神秘电话"""
        self.log_player_action("使用神秘电话")

    def UseHhandcuffs(self):
        """使用手铐"""
        self.log_player_action("使用手铐")

    def UseProp(self, num: str):
        """使用道具"""
        log.debug(f"玩家 {self.player.name} 使用道具 {num}")
        dct_actions = {
            "0": self.UseGun,
        }
        action = dct_actions.get(num, None)
        # log.debug(dct_actions)
        if callable(action):  # 确保方法可调用
            action(self)
        else:
            log.warning(f"无效道具: {num}")


dct_actions = {
    "0": PlayerActionsGPT.UseGun,
    "1": PlayerActionsGPT.UseCiga,
    "2": PlayerActionsGPT.UseMedicine,
    "3": PlayerActionsGPT.UseBear,
    # "4": UseMagnifier,
    # "5": UseReverse,
    # "6": UseAdrenaline,
    # "7": UseSaw,
    # "8": UsePhone,
    # "9": UseHhandcuffs,
}
