import argparse


class Wheel:
    class Node:

        def __init__(
            self,
            value: int,
            prev: "Wheel.Node | None" = None,
            next: "Wheel.Node | None" = None,
        ) -> None:
            self.value = value
            self.prev = prev or self
            self.next = next or self

    def __init__(self, ceil: int) -> None:
        self.first = self.last = self.Node(1)
        self.dict = {1: self.first}
        self.ceil = ceil

    def __str__(self) -> str:
        str_values = [str(num) for num in self.get_values()]
        return "[" + ", ".join(str_values) + "]"

    def append(self, value: int) -> None:
        node = self.Node(value, self.last, self.first)

        self.last.next = self.first.prev = node
        self.last = node

        self.dict[value] = node

    def remove(self, value: int) -> None:
        node = self.dict.pop(value)

        node.next.prev = node.prev
        node.prev.next = node.next

        if node is self.first:
            self.first = node.next
        if node is self.last:
            self.last = node.prev

    def get_values(self) -> list[int]:
        iter = self.first
        values = [iter.value]
        while iter is not self.last:
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

        last_value = wheel.last.value
        composites = []
        for num in wheel.dict:
            composite = num * prime
            if composite > last_value:
                break

            composites.append(composite)

        for c in composites:
            wheel.remove(c)

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
