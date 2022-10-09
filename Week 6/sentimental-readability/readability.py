from cs50 import get_string


# Take text from the user's input
text = get_string("Text: ")

sentences = 0
# 'words' must start from 1, because in 3 words there are only 2 spaces, in 7 words there are 6 spaces
words = 1
letters = 0

for i in text:
    if i in [".", "!", "?"]:
        sentences += 1
    elif i == " ":
        words += 1
    # If 'i' is alphabetic (a-z or A-Z)
    elif i.isalpha():
        letters += 1

# Average number of letters per 100 words in the text
L = (letters / words) * 100
# Average number of sentences per 100 words in the text
S = (sentences / words) * 100

# Coleman-Liau index
index = 0.0588 * L - 0.296 * S - 15.8
grade = round(index)

if grade < 1:
    print("Before Grade 1")
elif grade >= 16:
    print("Grade 16+")
else:
    print(f"Grade {grade}")
