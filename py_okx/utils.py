from typing import Union


def secs_to_millisecs(secs: Union[int, float, str]) -> int:
    secs = int(secs)
    return secs * 1000 if len(str(secs)) == 10 else secs
