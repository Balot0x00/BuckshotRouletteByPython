"""
根据道具效果对玩家状态进行修改
"""
import random
from loguru import logger as log

from utils.Base import BaseRound, BasePlayer
from utils.PropEffect import TheCiga, TheMedicine


def UseCiga(player: BasePlayer, round: BaseRound):
    """
    使用香烟
    """
    life = player.life
    life = TheCiga()
    log.debug(f"玩家 {player.name} 使用香烟, 获得效果: 生命 {life}")
    player.life = life
    return player


def UseMedicine(player: BasePlayer, round: BaseRound):
    """
    使用过期药品
    """

    life = TheMedicine()
    log.debug(f"玩家 {player.name} 使用过期药品, 获得效果: 生命 {life}")
    player.life = player.life + life
    if player.life <= 0:
        player.life = 0
        # log.warning(f"玩家 {player.name} 使用过期药品, 生命 {player.life} 死亡")
    if player.life >= 4:
        player.life = 4

    return player


def UseBear(player: BasePlayer, round: BaseRound):
    """
    3: 使用啤酒, 退出当前子弹
    """

    # if len(round.gun) > 0:
    bullet = round.gun.pop(0)

    log.debug(f"玩家 {player.name} 使用啤酒, 退出 {bullet} 当前弹夹 {round.gun}")
    return


def UseMagnifier(player: BasePlayer, round: BaseRound):
    """
    4: 使用放大镜, 查看当前子弹类型
    """

    log.debug(f"玩家 {player.name} 使用放大镜")
    log.info(f"当前子弹 {round.gun[0]}")
    return


def UseReverse(player: BasePlayer, round: BaseRound):
    """
    5: 使用逆转器, 将当前子弹类型进行逆转

    """
    bullet = round.gun[0]
    if bullet == 1:
        round.gun[0] = 0
    else:
        round.gun[0] = 1

    log.debug(f"玩家 {player.name} 使用逆转器, 当前子弹 {round.gun}")
    return



from .util import UserInput
def UseAdrenaline(player: BasePlayer, round: BaseRound,target: BasePlayer):
    from utils.RandomGenter import RandomSelectTools
    """
    6: 使用肾上腺素, 获取对方一种道具, 但不能是6
    """
    # 临时处理, 避免选择6
    target_props = target.props
    for a in target_props:
        if a.split(":")[0] == "6":
            target_props.remove(a)
    target_props_num = [x.split(":")[0] for x in target_props]
    
    # 
    prop_num =UserInput(prompt=f"{target_props} 选择道具: ",lt=target_props_num)
    for item in target.props:
        if prop_num == item.split(":")[0]:
            target.props.remove(item)
            player.props.append(item)
            break
    log.debug(f"玩家 {player.name} 使用肾上腺素, 获得道具 {item}")
    return prop_num


def UseSaw(player: BasePlayer, round: BaseRound):
    """
    7: 使用短锯, 当前子弹伤害翻倍
    修改gun_tag 标志位为2, 伤害翻倍
    """
    log.debug(f"玩家 {player.name} 使用短锯")
    round.gun_tag = 2
    return


def UsePhone(player: BasePlayer, round: BaseRound):
    """
    8: 使用神秘电话, 查看除当前子弹外, 随机一颗子弹类型
    """
    current_bullet_len = len(round.gun)
    random_bullet = random.randint(1, current_bullet_len - 1)

    log.info(
        f"玩家 {player.name} 使用神秘电话, 第 {random_bullet +1} 子弹为 {round.gun[random_bullet]}"
    )
    return


# 以下道具需要选择使用对象 target
def UseGun(player: BasePlayer, round: BaseRound, target: BasePlayer):
    """
    0: 使用枪
    """
    bullet = round.gun.pop(0)
    if bullet == 1:
        target.life = target.life - 1 * round.gun_tag
        # 打出翻倍伤害后, 恢复为1倍伤害
        if round.gun_tag == 2:
            round.gun_tag = 1

    if bullet == 0:
        pass
    log.debug(
        f"玩家 {player.name} 对 {target.name} 开枪, 子弹 {'实弹' if bullet == 1 else '空包弹'}, 目标生命 {target.life}"
    )
    log.debug(f"剩余子弹: {round.gun}")
    return bullet


def UseHhandcuffs(player: BasePlayer, round: BaseRound, target: BasePlayer):
    """
    9. 使用手铐
    """
    if target.status == "slience":
        log.warning(f"玩家 {target.name} 已经被手铐")
        return False

    log.debug(f"玩家 {player.name} 对 {target.name} 使用手铐")
    target.status = "slience"
    return True

def TestFunc():
    return "call test func"
