import argparse


class Wheel:
    class Node:
        def __init__(self, value: int) -> None:
            self.value = value

    def __init__(self, ceil: int) -> None:
        self.first = self.last = self.Node(1)
        self.dict = {1: self.first}
        self.ceil = ceil

    def __str__(self) -> str:
        str_values = [str(num) for num in self.get_values()]
        return "[" + ", ".join(str_values) + "]"

    def append(self, value: int) -> None:
        node = self.Node(value)

        self.last.next = self.first.prev = node
        node.prev = self.last
        node.next = self.first
        self.last = node

        self.dict[value] = node

    def remove(self, value: int) -> None:
        node = self.dict[value]

        node.next.prev = node.prev
        node.prev.next = node.next

        if node == self.first:
            self.first = node.next
        if node == self.last:
            self.last = node.prev

        del self.dict[value]

    def get_values(self) -> list[int]:
        iter = self.first
        values = [iter.value]
        while iter != self.last:
            iter = iter.next
            values.append(iter.value)
        return values

    def extend(self, prev_primorial: int, primorial: int) -> None:
        iter = self.first

        cur_ceil = min(self.ceil, primorial)
        next_num = iter.value + prev_primorial

        while next_num <= cur_ceil:
            self.append(next_num)

            iter = iter.next
            next_num = iter.value + prev_primorial


def sieve(ceil: int) -> list[int]:
    if ceil < 2:
        return []
    if ceil == 2:
        return [2]

    primes = [2]
    primorial = 2
    prime = 3

    wheel = Wheel(ceil)

    while True:
        prev_primorial = primorial
        primorial = prev_primorial * prime

        wheel.extend(prev_primorial, primorial)

        for num in list(wheel.dict.keys()):
            composite = num * prime

            if composite > wheel.last.value:
                break

            wheel.remove(composite)

        primes.append(prime)

        if min(prime * prime, primorial) > ceil:
            break

        prime = wheel.first.next.value

    return primes + list(wheel.dict)[1:]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find all primes up to a given limit.")
    parser.add_argument("limit", type=int, help="Upper limit (inclusive)")
    args = parser.parse_args()

    result = sieve(args.limit)
    print(result)
