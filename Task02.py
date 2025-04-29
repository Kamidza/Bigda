from collections.abc import Sequence

def check_fibonacci(data: Sequence[int]) -> bool:
    if len(data) < 2:
        return True

    if len(data) == 2:
        return data == [0, 1] or data == [1, 1]

    for i in range(2, len(data)):
        if data[i] != data[i - 1] + data[i - 2]:
            return False

    return True