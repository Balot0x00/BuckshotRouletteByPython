"""
单人与NPC对局测试
"""

import utils
from loguru import logger as log

# 初始化对局
round01 = utils.RoundInit()


# 初始化NPC
npc01 = utils.NPCInit(round01)
# print(f"NPC: {npc01.life}, 道具: {npc01.props}")


# 初始化玩家
zhangsan = utils.PlayerInit(round01)
# print(f"Player: {zhangsan.life}, 道具: {zhangsan.props}")

ps = [zhangsan, npc01]
action = utils.PlayerActionsSoloMatch(ps, round01)
# print(action.current_player.name)


while True:
    action.CheckPlayerState()
    action.GunCheck()
    # if not action.CheckPlayerState() and not action.CheckVirtoy():
    #     break
    utils.PrintRoundInfo(ps)
    print(f"当前行动:  {action.current_player.name}")
    num = utils.UserInput("请输入道具编号:",[tool_num.split(':')[0] for tool_num in action.current_player.props])
    action.UseProps(num)
