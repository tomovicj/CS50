#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

const int BLOCK_SIZE = 512;

int check(BYTE buffer[BLOCK_SIZE]);

int main(int argc, char *argv[])
{
    // Check if the number of arguments is one
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Check if given file can be loaded
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Looks like there is an error with loading your file!\n");
        printf("Make sure you entered the correct file name.\n");
        return 1;
    }


    BYTE buffer[BLOCK_SIZE];
    char *filename = malloc(sizeof(int) * 3 + sizeof(char) * 5);
    int n = -1;

    // Goes thru every "block" in the file
    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        if (check(buffer))
        {
            n++;
            // Formatting the filename
            sprintf(filename, "%03i.jpg", n);
            FILE *image = fopen(filename, "a");
            fwrite(buffer, 1, BLOCK_SIZE, image);
            fclose(image);
        }
        else
        {
            // Only runs if JPEG header is first founded
            if (n >= 0)
            {
                FILE *image = fopen(filename, "a");
                fwrite(buffer, 1, BLOCK_SIZE, image);
                fclose(image);
            }
        }
    }

    fclose(file);
    free(filename);
    return 0;
}

// Checks for JPEG header
int check(BYTE buffer[BLOCK_SIZE])
{
    if (buffer[0] == 0xff & buffer[1] == 0xd8 & buffer[2] == 0xff & (buffer[3] & 0xf0) == 0xe0)
    {
        return 1;
    }
    return 0;
}
