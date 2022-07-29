#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Get user input
    string text = get_string("Text: ");

    // Count
    float letters = count_letters(text);
    float words = count_words(text);
    float sentences = count_sentences(text);

    // Calculate
    float l = letters / words * 100;
    float s = sentences / words * 100;
    int index = round(0.0588 * l - 0.296 * s - 15.8);

    if (index >= 16)
    {
        printf("Grade 16+\n");
        return 0;
    }
    if (index < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }
    printf("Grade %i\n", index);
}

int count_letters(string text)
{
    int count = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        // Turn letter to lowercase
        char letter = tolower(text[i]);
        // Check if is a letter
        if (letter >= 'a' && letter <= 'z')
        {
            count++;
        }
    }
    return count;
}

int count_words(string text)
{
    int count = 1;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        char letter = text[i];
        if (letter == ' ')
        {
            count++;
        }
    }
    return count;
}

int count_sentences(string text)
{
    int count = 0;
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        char letter = text[i];
        if (letter == '.' || letter == '?' || letter == '!')
        {
            count++;
        }
    }
    return count;
}
