from dataclasses import field, dataclass
from time import time
from functools import wraps
from typing import List, Union, Any, Dict, Tuple


def prep_value(val):
    val = str(val)
    if val is None:
        return "None"
    if len(val) > 100:
        return val[:100]+"..."
    return val

@dataclass
class Call:
    id: int
    function_name: str
    args: Tuple[Any]
    kwargs: Dict[Any, Any]
    children: List = field(default_factory=lambda: [])

    def __repr__(self):

        args = ', '.join([prep_value(str(x)) for x in self.args])
        kwargs = ', '.join(f"{key}: {prep_value(str(value))}" for key, value in self.kwargs.items())
        return f"+{self.function_name}({','.join([args] + [kwargs])})"


@dataclass
class CallEnd:
    id: int
    return_value: str
    function_name: str
    duration: float

    def __repr__(self):
        return f"-{self.function_name} dur: {self.duration} ret: {prep_value(self.return_value)}"

class Elephant:
    history: List[Union[Call, CallEnd]] = []
    history_history: List[List[Union[Call, CallEnd]]] = []
    nest_level: int = 0

    def record(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.nest_level += 1
            self.history.append(Call(id=1, args=args, kwargs=kwargs, function_name=func.__qualname__))
            start_time = time()
            ret = func(*args, **kwargs)
            end_time = time()
            duration = end_time - start_time
            # self.history.append("end_"+func.__name__)
            self.nest_level -= 1
            self.history.append(CallEnd(id=1, function_name=func.__qualname__, return_value=ret, duration=duration))

            if self.nest_level == 0:
                self.history_history.append(self.history)
                self.history = []

            return ret

        return wrapper

    def print_last(self):
        intend = -1
        for r in self.history_history[-1]:
            if type(r) == Call:
                intend += 1
            print(("\t" * intend) + "|__  " +str(r))
            if type(r) == CallEnd:
                intend -= 1

    def save_flat(self):
        pass


elephant = Elephant()
