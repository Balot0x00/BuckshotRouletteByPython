round 回合


道具列表
{
    1: "香烟",
    2: "过期药品",
    3: "啤酒",
    4: "放大镜",
    5: "逆转器",
    6: "肾上腺素",
    7: "短锯",
    8: "神秘电话",
    9: "手铐",
}


血量 与 round 关联
每次填充子弹前发放道具

round 3局, 每次round 刷新道具

刷新子弹 不 刷新道具
手机查看除当前子弹外任意子弹的类型

一次load内为 gun gun init 发放道具
一次life == 0 内 为 round
3round 内 为 game

round init
    Extract props
    show life
    show bullets
    gun init

player init


弹夹 [] 从前向后action 
pop(0)