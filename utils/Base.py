class BaseGun:
    def __init__(self):
        self.props_num = None
        self.gun = None


class BaseRound:
    def __init__(self):
        self.gun = BaseGun()
        self.props_num = int()
        self.life_max = int()
        self.life = int()
        self.gun_tag = int()


class BasePlayer:
    def __init__(self, round: BaseRound):
        self.id: int = int()
        self.name: str = str()
        self.life = int()
        self.props = None
        self.status = str()
        self.round_id = str()
