import os,sys

from loguru import logger as log
# 移除默认的日志处理器
log.remove()

# 添加一个新的日志处理器，只保留 info 及以上级别的日志
log.add(sink=sys.stderr, level="INFO")

#
from .ConsolePrint import PrintStatus, PrintRoundInfo
from .util import UserInput


from .GameControl import PlayerActions
from .GameControl_solomatch import PlayerActionsSoloMatch

from .RandomGenter import RandmonSelector, RandomSelectTools
from .PropEffect import TheCiga, TheMedicine, TheSkit

from .InitGame import RoundInit,GunInit
from .InitPlayer import PlayerInit,NPCInit
