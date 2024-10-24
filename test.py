def func01():
    return False

def func02():
    return True


sw = {
    1: func01,
    2: func02,
}

res  = sw.get(1)()
print(res)