from loguru import logger as log


def UserInput(prompt, lt=[]):
    """
    输入函数
    :param prompt: 提示信息
    :return: 输入的内容
    """
    log.debug(f"lt: {lt}")
    while True:
        num = input(prompt)
        
        if not num.isdigit():
            log.warning("非法字符，请重新输入")
        elif not len(lt) == 0 and not num in lt:
            log.warning("超出范围, 请重新输入")
        else:
            return num