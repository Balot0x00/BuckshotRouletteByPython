import utils
from loguru import logger as log

# 声明单个玩家
gun01 = utils.GunInit()
round01 = utils.RoundInit(gun01)
zhangsan = utils.PlayerInit(round01)


action = utils.PlayerActionsDemo(zhangsan, round01)
action.UseProp("11")


def testfunc(*args,**kwargs):
    print(args)
    print(kwargs)
    print("testfunc")

lst = [1,2,3,4,5]
print (lst[0:4])