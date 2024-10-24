class obja:
    def __init__(self):
        self.a = 1


class objb:
    def __init__(self, obj_a: obja):
        self.b = 2
        self.obj_a = obj_a  # 保存 obja 的实例

    def func(self):
        print(self.obj_a.a)  # 访问 obja 实例的属性 a
        print(self.b)  # 访问 objb 的属性 b


# 示例用法
a_instance = obja()
b_instance = objb(a_instance)
b_instance.func()
