def ack(m: int, n: int) -> int:
    if m == 0:
        return n + 1
    if n == 0:
        return ack(m - 1, 1)
    return ack(m - 1, ack(m, n - 1))


if __name__ == "__main__":
    import sys
    
    m, n = 1, 2
    print(f"A({m},{n}) = {ack(m, n)}")

    m, n = 2, 2
    print(f"A({m},{n}) = {ack(m, n)}")
