import csv
import sys
import re


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return

    # Read database file into a variable
    db = []
    with open(sys.argv[1]) as csvfile:
        # Read the csv file as a sequence of lists
        database = csv.reader(csvfile)
        for row in database:
            db.append(row)

    # Read DNA sequence file into a variable
    with open(sys.argv[2]) as file:
        dnafile = file.read()

    # Find longest match of each STR in DNA sequence
    STRs = {}
    # To get the names of the STR sequence and store it as keys in the dictionary
    strarray = str(db[0])
    strarray = list(strarray.split())
    strarray.pop(0)
    names = []
    # Keep only letters in the list
    for element in strarray:
        lettersonly = ""
        for char in str(element):
            if char.isalpha():
                lettersonly += char
        names.append(lettersonly)
    for i in range(len(names)):
        STRs[names[i]] = longest_match(dnafile, names[i])

    # Check database for matching profiles
    values = list(STRs.values())
    for i in range(len(values)):
        values[i] = int(values[i])

    dbvals = []
    for i in range(len(db) - 1):
        currentVal = str(db[i + 1]).split()
        currentVal2 = []
        # Covert each row in db to an int list, except the first element: Name
        for element in currentVal:
            ldonly = ""
            for letter in element:
                if letter.isalnum():
                    ldonly += letter
            currentVal2.append(ldonly)
        NAME = currentVal2[0]
        currentVal2.pop(0)
        val = []
        for element in currentVal2:
            val.append(int(element))

        if val == values:
            print(NAME)
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
