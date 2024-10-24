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

ps = [zhangsan, npc01]
action = utils.PlayerActionsSoloMatch(ps, round01)
print(action.currnet_player.name)

# 给NPC设置沉默状态
if action.currnet_player.name == "NPC":
    action.currnet_player.status = "slience"

while True:
    action.GunCheck()
    action.ActionCheck()
    action.LifeCheck()
    print(f"当前行动:  {action.currnet_player.name}")
    num = input("选择道具")
    action.UseProps(num)
