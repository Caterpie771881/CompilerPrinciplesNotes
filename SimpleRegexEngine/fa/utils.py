from typing import Union


class AnyCondition():
    __instance = None

    @classmethod
    def instance(cls) -> "AnyCondition":
        if not cls.__instance:
            cls.__instance = AnyCondition()
        return cls.__instance
    
    def __str__(self) -> str:
        return "<any>"
    
    def __len__(self) -> int:
        return 1


fa_condition = Union[str, AnyCondition]

ANY = AnyCondition.instance()
