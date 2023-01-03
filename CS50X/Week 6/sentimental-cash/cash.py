from cs50 import get_float


def main():
    # Gets positive float input from the user
    while True:
        owed = get_float("Change owed: ")
        if owed > 0:
            break

    # Calculate the minimum number of coins we have to give
    n, owed = calculate(owed, 0.25)
    sum = n
    n, owed = calculate(owed, 0.10)
    sum += n
    n, owed = calculate(owed, 0.05)
    sum += n
    n, owed = calculate(owed, 0.01)
    sum += n

    # Print the minimum number of coins we have to give
    print(sum)


def calculate(owed, coin):
    x = owed / coin
    x = int(x)
    owed = owed - (x * coin)
    # Return number of coins you can give AND how much owed is left
    # Rounding is done because of floating point imprecision
    return x, round(owed, 2)


main()
