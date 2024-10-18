import utils
from loguru import logger as log

# 声明单个玩家
gun01 = utils.GunInit()
round01 = utils.RoundInit(gun01)
zhangsan = utils.PlayerInit(round01)



# print(zhangsan.props)
# print(zhangsan.life)
# print (zhangsan, round01.gun)

# action: 开枪
# utils.UseGun(zhangsan, round01)


# player input
# p_slelect = input()

action = utils.PlayerActions(zhangsan, round01)
action.UseProp("3")
print (round01.gun)