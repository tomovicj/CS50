import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")

    # Read database file into a variable
    data = []
    with open(sys.argv[1], "r") as f:
        file = csv.DictReader(f)
        for row in file:
            data.append(row)

    # Gets a list of all STR names
    with open(sys.argv[1], "r") as f:
        st = (f.readline()).split(",")
        # Gets a ride of "name"
        st.pop(0)
        # Gets a ride of "\n"
        st[-1] = st[-1].split("\n")[0]

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as f:
        sequence = f.read()

    # Find longest match of each STR in DNA sequence
    highest = {}
    for i in st:
        highest[i] = longest_match(sequence, i)

    # Check database for matching profiles
    for i in data:
        n = 0
        for j in st:
            if int(i[j]) == highest[j]:
                n += 1
        if n == len(st):
            print(i["name"])
            return
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
