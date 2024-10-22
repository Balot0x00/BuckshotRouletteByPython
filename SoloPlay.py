"""
单人游戏:无对局NPC, 仅单人进行游戏交互
"""

import utils
from loguru import logger as log

round01 = utils.RoundInit()
zhangsan = utils.PlayerInit(round01)
action = utils.PlayerActions(zhangsan, round01)

log.info(f"开始游戏, 本回合生命: {round01.max}, 当前道具{round01.props}")

while True:
    action.GunCheck()
    if not action.LifeCheck():
        break
    p_slelect = input()
    action.UseProp(p_slelect)