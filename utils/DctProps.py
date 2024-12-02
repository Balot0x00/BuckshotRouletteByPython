from utils.DctAction import TestFunc

# dct_test = {
#     "a":TestFunc
# }


dct_props = {
    "1": "香烟",
    "2": "过期药品",
    "3": "啤酒",
    "4": "放大镜",
    "5": "逆转器",
    "6": "肾上腺素",
    "7": "短锯",
    "8": "神秘电话",
    "9": "手铐",
}
from utils.DctAction import *


dct_actions = {
    "1": UseCiga,
    "2": UseMedicine,
    "3": UseBear,
    "4": UseMagnifier,
    "5": UseReverse,
    "7": UseSaw,
    "8": UsePhone,
}


dct_action_other = {
    "9": UseHhandcuffs,
}


dct_action_all = {
    "6": UseAdrenaline,
    "0": UseGun,
}
