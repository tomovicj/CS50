from cs50 import get_int


def main():
    # Make sure input is numeric
    cc = get_int("Number: ")
    cc = str(cc)

    # Length of the credit card number
    length = len(cc)

    if check(cc, length):
        # Check if it is AMEX card
        if length == 15 and cc[0] == "3" and (cc[1] == "4" or cc[1] == "7"):
            print("AMEX")
        # Check if it is VISA card
        elif (length == 13 or length == 16) and cc[0] == "4":
            print("VISA")
        # Check if it is MASTERCARD card
        elif length == 16 and cc[0] == "5" and int(cc[1]) in range(1, 6):
            print("MASTERCARD")
        else:
            # If neither of those
            print("INVALID")
    else:
        # If check fails
        print("INVALID")


# Luhn’s Algorithm
def check(number, length):
    sum1 = 0
    sum2 = 0

    # Reversing a string
    number = number[::-1]

    # Add every other number from second last (second)
    for i in range(1, length, 2):
        x = str(int(number[i]) * 2)
        # If 'x' is a double-digit number sum each one
        if len(x) > 1:
            for n in range(len(x)):
                sum1 += int(x[n])
        else:
            sum1 += int(x)

    # Add every other number from last (first)
    for i in range(0, length, 2):
        sum2 += int(number[i])

    sum = str(sum1 + sum2)

    # If the last digit is 0
    if int(sum[-1]) == 0:
        return True
    else:
        return False


main()
