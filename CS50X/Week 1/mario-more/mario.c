#include <cs50.h>
#include <stdio.h>

void hashes(int i)
{
    for (int hash = 0; hash < i; hash++)
    {
        printf("#");
    }
}

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
        // Space at the front
        // From height subtract the number of hashes in that row
        for (int space = 0; space < height - i; space++)
        {
            printf(" ");
        }
        // Left side
        hashes(i);
        // Space in the middle
        printf("  ");
        // Right side
        hashes(i);
        // Break the row at the end of the row
        printf("\n");
    }
}
