import utils
from loguru import logger as log

# gun01
gun01 = utils.GunInit()
round01 = utils.RoundInit(gun01)
zhangsan = utils.PlayerInit(round01)

# player action
action = utils.PlayerActions(zhangsan, round01)
print (f"player: {zhangsan.life} {round01.gun}, {zhangsan.props}")
action.UseProp("6")

log.critical(f"弹夹清空")
round01.gun = []
action.UseProp("1")
print (f"player: {zhangsan.life} {round01.gun}, {zhangsan.props}")

# player dead
log.critical(f"玩家 {zhangsan.name} 死亡")

zhangsan.life = 0
action.UseProp("3")

