"""
单人与NPC对局测试
"""

import utils
from loguru import logger as log

# 初始化对局
round01 = utils.RoundInit()


# 初始化NPC
npc01 = utils.NPCInit(round01)
print(f"NPC: {npc01.life}, 道具: {npc01.props}")


# 初始化玩家
zhangsan = utils.PlayerInit(round01)
print(f"Player: {zhangsan.life}, 道具: {zhangsan.props}")

ps = [zhangsan,npc01]
action = utils.PlayerActionsSoloMatch(ps, round01)
print (action.currnet.name)

# 切换玩家
# action.ActionSwitch()
# print (action.currnet.name)

# 展示可选目标
lst_target = action.ShowTarget()
print(lst_target)