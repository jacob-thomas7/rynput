from abc import ABC, abstractmethod
from typing import Optional

class Validator():
    @abstractmethod
    def validate(self, string: str) -> Optional[any]:
        pass

class Integer(Validator):
    def __init__(self):
        pass

    def validate(self, string: str) -> Optional[int]:
        if string.isdigit() or (string[0] in ('-', '+') and string[1:].isdigit()):
            return int(string)
        return None


class MinMax:
    def __init__(self, min: int, max: int):
        self.min = min
        self.max = max

    def validate(self, string: str) -> Optional[int]:
        if string.isdigit() or (string[0] in ('-', '+') and string[1:].isdigit()):
            if int(string) >= self.min and int(string) <= self.max:
                return int(string)
        return None

properties = [
    {"name" : "integer", "value_type" : Integer(), "default" : 5},
    {"name" : "minmax", "value_type" : MinMax(3, 8), "default" : 5},
]

def validate():
    for property in properties:
        value = None
        while value is None:
            response = input("input a " + property["name"])
            if not response.strip():
                value = property["default"]
                continue
            value = property["value_type"].validate(response)
        print(value)

validate()