"""
玩家行动, 行动前逻辑判断, 玩家状态判断
根据道具效果对玩家状态进行修改
"""

from loguru import logger as log
from .GameControl import PlayerInit, RoundInit
from .PropEffect import *
from .config import dct_actions , dct_actionsv2


class PlayerActionsDemo:
    """玩家行动管理"""

    def __init__(self, player: PlayerInit, round: RoundInit) -> None:
        self.player = player
        self.round = round

    def UseCiga(self, *args, **kwargs):
        """使用香烟"""
        log.debug(f"玩家 {self.player.name} 使用香烟")
        # 检查玩家是否有香烟
        if self.player.life > 0:
            pass



    def UseProp(self, num: str, *args, **kwargs):
        """使用道具"""
        log.debug(f"玩家 {self.player.name} 使用道具 {num}")

        action_name = dct_actionsv2.get(num, None)

        if action_name and hasattr(self, action_name):  # 确保方法存在
            # if action 属于扩展行动字典, 即有使用对象的行动字典
            action_method = getattr(self, action_name)  # 获取方法
            action_method(*args, **kwargs)  # 调用方法并传递参数
        else:
            log.warning(f"无效道具: {num}")

