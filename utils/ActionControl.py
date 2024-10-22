"""
玩家行动, 行动前逻辑判断, 玩家状态判断
根据道具效果对玩家状态进行修改
"""

from loguru import logger as log

from .GameControl import PlayerInit, RoundInit
from .PropEffect import *


def UseGun(player: PlayerInit, round: RoundInit):
    """
    使用枪
    """
    log.debug(f"玩家 {player.name} 开枪")
    bullet = round.gun.pop(0)
    if bullet == 1:
        player.life = player.life - 1
    if bullet == 0:
        pass
    log.debug(
        f"玩家 {player.name} 开枪, 子弹 {'实弹' if bullet == 1 else '空包弹'}, 生命 {player.life}"
    )
    log.debug(f"剩余子弹: {round.gun}")
    return


def UseCiga(player: PlayerInit, round: RoundInit):
    """
    使用香烟
    """
    life = player.life
    life = TheCiga()
    log.debug(f"玩家 {player.name} 使用香烟, 获得效果: 生命 {life}")
    player.life = life
    return player


def UseMedicine(player: PlayerInit, round: RoundInit):
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


def UseBear(player: PlayerInit, round: RoundInit):
    """
    3: 使用啤酒, 退出当前子弹
    """

    # if len(round.gun) > 0:
    bullet = round.gun.pop(0)

    log.debug(f"玩家 {player.name} 使用啤酒, 退出 {bullet} 当前弹夹 {round.gun}")
    return


def UseMagnifier(player: PlayerInit, round: RoundInit):
    """
    4: 使用放大镜, 查看当前子弹类型
    """

    log.debug(f"玩家 {player.name} 使用放大镜")
    log.info(f"当前子弹 {round.gun[0]}")
    return


def UseReverse(player: PlayerInit, round: RoundInit):
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

from .RandomSelect import RandomSelectTools

def UseAdrenaline(player: PlayerInit, round: RoundInit):
    """
    6: 使用肾上腺素, 获取对方一种道具, 但不能是6
    """
    prop = RandomSelectTools(1)
    # log.debug(f"首次获得道具 {prop}")
    while prop[0].split(":")[0] == "6":
        prop = RandomSelectTools(1)


    
    player.props.append(prop[0])
    log.debug(f"玩家 {player.name} 使用肾上腺素, 获得道具 {prop}")
    return


def UseSaw(player: PlayerInit, round: RoundInit):
    """
    7: 使用短锯, 当前子弹伤害翻倍
    """
    log.debug(f"玩家 {player.name} 使用短锯")
    return


def UsePhone(player: PlayerInit, round: RoundInit):
    """
    8: 使用神秘电话, 查看除当前子弹外, 随机一颗子弹类型
    """
    current_bullet_len = len(round.gun)
    random_bullet = random.randint(1, current_bullet_len-1)

    log.info(
        f"玩家 {player.name} 使用神秘电话, 第 {random_bullet +1} 子弹为 {round.gun[random_bullet]}"
    )
    return


def UseHhandcuffs(player: PlayerInit, round: RoundInit):
    """
    9. 使用手铐
    """
    log.debug(f"玩家 {player.name} 使用手铐")
    return

