from PIL.Image import Image

from abc import ABC, abstractproperty
from typing import Tuple, Union, Optional

from random import randint

class PastingRule(ABC):
    @abstractproperty
    def rule(self) -> Union[Tuple[int, int], Tuple[int, int, int, int]]:
        pass
    
class LeftCornerPaddingRule(PastingRule):
    def __init__(self, left_corner = Tuple[int, int]):
        self.__rule = left_corner
    
    @property
    def rule(self) -> Tuple[int, int, int, int]:
        return self.__rule

class RandomPaddingRule(PastingRule):
    def __init__(self, limit : Optional[int] = 20):
        self.__limit = limit

    @property
    def rule(self) -> Tuple[int, int, int, int]:
        return (randint(0, self.__limit), randint(0,self.__limit))
        
if __name__ == "__main__":
    lrule : PastingRule = LeftCornerPaddingRule((10, 10))
    print(lrule.rule)