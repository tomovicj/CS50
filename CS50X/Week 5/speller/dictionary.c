// Implements a dictionary's functionality

#include <ctype.h>
#include <strings.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Count every word when loaded
unsigned int word_counter = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int hash_index = hash(word);
    node *n = table[hash_index];

    // If no word with that hash_index was loaded from the dictionary
    if (n == NULL)
    {
        return false;
    }

    // Check all words in that hash_index except the last one
    while (n->next != NULL)
    {
        if (strcasecmp(n->word, word) == 0)
        {
            return true;
        }
        n = n->next;
    }
    // Check the last word in that hash_index
    if (strcasecmp(n->word, word) == 0)
    {
        return true;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    char c;
    char word[LENGTH + 1];
    unsigned int i = 0;
    while (fread(&c, sizeof(char), 1, file))
    {
        // When a word ends
        if (c == '\n')
        {
            unsigned int hash_index = hash(word);

            // Creating new node
            node *n = malloc(sizeof(node));
            if (n == NULL)
            {
                return false;
            }

            for (int j = 0; j < i; j++)
            {
                n->word[j] = word[j];
            }

            // TODO: fix valgrind errors (not memory related)
            // Probably because I didn't explicitly set n->next to NULL
            n->next = table[hash_index];
            table[hash_index] = n;

            i = 0;
            word_counter++;
        }
        // For every letter in the word
        else
        {
            word[i] = c;
            i++;
        }
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Goes through every hash_index
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];

        // If at least one word with that hash_index was loaded from the dictionary
        if (n != NULL)
        {
            // Frees all words in that hash_index except the last one
            while (n->next != NULL)
            {
                node *next = n->next;
                free(n);
                n = next;
            }
            // Frees the last word in that hash_index
            free(n);
        }
    }
    return true;
}
