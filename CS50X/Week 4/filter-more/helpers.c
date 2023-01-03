#include "helpers.h"
#include <math.h>
#include <stdlib.h>

int check(int height, int width, int i, int j);
int get_nx(int x, int y);
int get_ny(int x, int y);

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

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
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
            int rednx = 0;
            int greennx = 0;
            int bluenx = 0;
            int redny = 0;
            int greenny = 0;
            int blueny = 0;
            for (int x = 0; x < 3; x++)
            {
                int xx = list[x] + i;
                for (int y = 0; y < 3; y++)
                {
                    int yy = list[y] + j;
                    int nx = get_nx(list[x], list[y]);
                    int ny = get_ny(list[x], list[y]);

                    if (check(height, width, xx, yy))
                    {
                        rednx += copy[xx][yy].rgbtRed * nx;
                        greennx += copy[xx][yy].rgbtGreen * nx;
                        bluenx += copy[xx][yy].rgbtBlue * nx;

                        redny += copy[xx][yy].rgbtRed * ny;
                        greenny += copy[xx][yy].rgbtGreen * ny;
                        blueny += copy[xx][yy].rgbtBlue * ny;
                    }
                }
            }
            int red = round(sqrt(rednx * rednx + redny * redny));
            int green = round(sqrt(greennx * greennx + greenny * greenny));
            int blue = round(sqrt(bluenx * bluenx + blueny  * blueny));

            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }

            image[i][j].rgbtRed = (BYTE) red;
            image[i][j].rgbtGreen = (BYTE) green;
            image[i][j].rgbtBlue = (BYTE) blue;
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

int get_nx(int x, int y)
{
    int n;
    if (x == 0 & y == 0 || x == -1 & y == 0 || x == 1 & y == 0)
    {
        n = 0;
    }
    if (x == -1 & y == 1 || x == 1 & y == 1)
    {
        n = 1;
    }
    if (x == -1 & y == -1 || x == 1 & y == -1)
    {
        n = -1;
    }
    if (x == 0 & y == -1)
    {
        n = -2;
    }
    if (x == 0 & y == 1)
    {
        n = 2;
    }
    return n;
}

int get_ny(int x, int y)
{
    int n;
    if (x == 0 & y == 0 || x == 0 & y == -1 || x == 0 & y == 1)
    {
        n = 0;
    }
    if (x == 1 & y == -1 || x == 1 & y == 1)
    {
        n = 1;
    }
    if (x == -1 & y == -1 || x == -1 & y == 1)
    {
        n = -1;
    }
    if (x == -1 & y == 0)
    {
        n = -2;
    }
    if (x == 1 & y == 0)
    {
        n = 2;
    }
    return n;
}
