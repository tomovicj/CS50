#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int only_digits(string arg);
char rotate(char ptext, int k);

int main(int argc, string argv[])
{
    int key;
    string plaintext;

    // If given more or less than 2 arg
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // If input is numeric save it as 'key'
    if (only_digits(argv[1]))
    {
        key = atoi(argv[1]);
    }
    else
    {
        // Input is not numeric only
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Get text to encrypt
    plaintext = get_string("Plaintext:  ");
    int len = strlen(plaintext);
    // Creating 'ciphertext' array with length of the inputed 'plaintext'
    string ciphertext[len];

    printf("Ciphertext: ");
    for (int i = 0; i < len; i++)
    {
        printf("%c", rotate(plaintext[i], key));
    }
    printf("\n");
}

int only_digits(string arg)
{
    int count = 0;
    int len = strlen(arg);
    for (int i = 0; i < len; i++)
    {
        char c = arg[i];
        // If number if not in between 1-9
        if (!(c >= '1' && c <= '9'))
        {
            return 0;
        }
    }
    return 1;
}

char rotate(char c, int k)
{
    int was_upper = 0;
    if (isupper(c))
    {
        was_upper = 1;
        c = tolower(c);
    }
    // If between a-z
    if (c >= 'a' && c <= 'z')
    {
        for (int i = 0; i < k; i++)
        {
            // Wrapping around from z to a
            if (c + 1 > 'z')
            {
                c = 'a';
            }
            else
            {
                c += 1;
            }
        }
    }
    // If char was uppercase this will turn it back to uppercase
    if (was_upper)
    {
        return toupper(c);
    }
    return c;
}
