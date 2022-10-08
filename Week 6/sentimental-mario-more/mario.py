from cs50 import get_int

while True:
    # Get height from user
    height = get_int("Height: ")
    # Make sure height is 1-8
    if height >= 1 and height <= 8:
        break

for hashes in range(1, height + 1):
    # Determines how much spaces is needed
    blank = height - hashes
    # Prints out the first half of the pyramid
    print(" " * blank + "#" * hashes, end="  ")
    # Prints out the second half of the pyramid
    print("#" * hashes)
