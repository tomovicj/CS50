#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int check(string arg);
char encrypt(char ptext, string k);

int main(int argc, string argv[])
{
    string key;
    // If given more or less than 2 arg
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    // Check length, if input is alphabetical and if one letter is used multiple times
    if (check(argv[1]))
    {
        key = argv[1];
    }
    else
    {
        // If check faills
        printf("Key must contain 26 different alphabetic characters.\n");
        return 1;
    }

    // Get text to encrypt
    string plaintext = get_string("plaintext:  ");
    int len = strlen(plaintext);
    // Creating 'ciphertext' array with length of the inputed 'plaintext'
    string ciphertext[len];

    printf("ciphertext: ");
    for (int i = 0; i < len; i++)
    {
        printf("%c", encrypt(plaintext[i], key));
    }
    printf("\n");
    return 0;
}

int check(string arg)
{
    // Checks the length
    int len = strlen(arg);
    if (len != 26)
    {
        return 0;
    }

    for (int i = 0, a = 0; i < len; i++, a = 0)
    {
        char c = arg[i];
        c = tolower(c);

        // Checks if char is a letter
        if (!isalpha(c))
        {
            return 0;
        }

        // Checks if some letter is used more than once in the key
        for (int x = 0; x < len; x++)
        {
            if (arg[i] == arg[x])
            {
                a++;
            }
        }
        if (a > 1)
        {
            return 0;
        }
    }
    return 1;
}

char encrypt(char c, string k)
{
    int was_upper = 0;
    if (isupper(c))
    {
        was_upper = 1;
        c = tolower(c);
    }
    // If alphabetical
    if (isalpha(c))
    {
        int x = c - 'a';
        c = k[x];
        c = tolower(c);
    }
    // If char was uppercase this will turn it back to uppercase
    if (was_upper)
    {
        return toupper(c);
    }
    return c;
}
