from loguru import logger as log


from .GameControl import PlayerInit


def PrintStatus(player: PlayerInit):
    """
    实时打印当前对局信息, print
    """

    info_life = f"当前血量: {player.life}"
    info_props = f"当前道具栏: {player.props}"
    print(f"{player.name}: {info_life}, {info_props}")
    pass
