#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get height from the user. Valid input 1-8
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);


    // Loop for each row until the height is achieved
    for (int i = 1; i < height + 1; i++)
    {
        // From height subtract the number of hashes in that row
        for (int space = 0; space < height - i; space++)
        {
            printf(" ");
        }
        // Each loop adds one more hash at the end
        for (int hash = 0; hash < i; hash++)
        {
            printf("#");
        }
        // Break the row at the end of the row
        printf("\n");
    }
}
