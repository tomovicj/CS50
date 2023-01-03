#include "helpers.h"
#include <math.h>
#include <stdlib.h>


int check(int height, int width, int i, int j);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE red = image[i][j].rgbtRed;
            BYTE green = image[i][j].rgbtGreen;
            BYTE blue = image[i][j].rgbtBlue;

            float x = red + green + blue;
            BYTE average = round(x / 3);


            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            BYTE red = image[i][j].rgbtRed;
            BYTE green = image[i][j].rgbtGreen;
            BYTE blue = image[i][j].rgbtBlue;

            float fRed = .393 * red + .769 * green + .189 * blue;
            float fGreen = .349 * red + .686 * green + .168 * blue;
            float fBlue = .272 * red + .534 * green + .131 * blue;

            if (fRed > 255)
            {
                fRed = 255;
            }
            if (fGreen > 255)
            {
                fGreen = 255;
            }
            if (fBlue > 255)
            {
                fBlue = 255;
            }

            BYTE sepiaRed = round(fRed);
            BYTE sepiaGreen = round(fGreen);
            BYTE sepiaBlue = round(fBlue);

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE *row = malloc(width * sizeof(RGBTRIPLE));
    if (row == NULL)
    {
        return;
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            row[j] = image[i][j];
        }
        for (int n = 0, x = width - 1; n < width; n++, x--)
        {
            image[i][n] = row[x];
        }
    }

    free(row);
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }


    int list[] = {0, 1, -1};
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int n = 0;
            float redF = 0;
            float greenF = 0;
            float blueF = 0;
            for (int x = 0; x < 3; x++)
            {
                int xx = i + list[x];
                for (int y = 0; y < 3; y++)
                {
                    int yy = j + list[y];

                    if (check(height, width, xx, yy))
                    {
                        redF += copy[xx][yy].rgbtRed;
                        greenF += copy[xx][yy].rgbtGreen;
                        blueF += copy[xx][yy].rgbtBlue;
                        n += 1;
                    }
                }
            }
            BYTE red = round(redF / n);
            BYTE green = round(greenF / n);
            BYTE blue = round(blueF / n);

            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }
    }
    return;
}

// Check if pixel is in the image
int check(int height, int width, int i, int j)
{
    if (i < 0 || i == height)
    {
        return 0;
    }
    if (j < 0 || j == width)
    {
        return 0;
    }
    return 1;
}
