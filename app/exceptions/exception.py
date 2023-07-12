"""Own exceptions modul."""

class EnemyException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class WarriorException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class GameException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class LevelException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MenuException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class HelperException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
