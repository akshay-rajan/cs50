#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Find the average rgb value
            BYTE avg = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);

            // Replace the pixel with the average value
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
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
            // Calculate the sepia-rgb values
            int Red = round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue);
            int Green = round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue);
            int Blue = round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue);

            // If the value is out of range
            BYTE sepiaRed = (Red > 255) ? 255 : Red;
            BYTE sepiaBlue = (Blue > 255) ? 255 : Blue;
            BYTE sepiaGreen = (Green > 255) ? 255 : Green;

            // Replace the pixel with these values
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
    // Iterate over half the width of the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Swap the pixel with the pixel opposite to it from the middle
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of the image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // Take values from the copy, and write the blurred values into original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Variables to store the sum of rgb values of all neighbourhood pixels
            int red = 0, green = 0, blue = 0;

            // Check if each pixel exists; and sum the rgb values if they do
            int pixel_num = 0;

            // For the row above the pixel
            if (i - 1 >= 0)
            {
                if (j - 1 >= 0)
                {
                    // First pixel
                    red += copy[i - 1][j - 1].rgbtRed;
                    green += copy[i - 1][j - 1].rgbtGreen;
                    blue += copy[i - 1][j - 1].rgbtBlue;
                    pixel_num++;
                }
                // Second pixel
                red += copy[i - 1][j].rgbtRed;
                green += copy[i - 1][j].rgbtGreen;
                blue += copy[i - 1][j].rgbtBlue;
                pixel_num++;
                if (j + 1 < width)
                {
                    // Third pixel
                    red += copy[i - 1][j + 1].rgbtRed;
                    green += copy[i - 1][j + 1].rgbtGreen;
                    blue += copy[i - 1][j + 1].rgbtBlue;
                    pixel_num++;
                }
            }
            // For the same row as the pixel
            if (j - 1 >= 0)
            {
                red += copy[i][j - 1].rgbtRed;
                green += copy[i][j - 1].rgbtGreen;
                blue += copy[i][j - 1].rgbtBlue;
                pixel_num++;
            }
            red += copy[i][j].rgbtRed;
            green += copy[i][j].rgbtGreen;
            blue += copy[i][j].rgbtBlue;
            pixel_num++;
            if (j + 1 < width)
            {
                red += copy[i][j + 1].rgbtRed;
                green += copy[i][j + 1].rgbtGreen;
                blue += copy[i][j + 1].rgbtBlue;
                pixel_num++;
            }
            // For the row below the pixel
            if (i + 1 < height)
            {
                if (j - 1 >= 0)
                {
                    red += copy[i + 1][j - 1].rgbtRed;
                    green += copy[i + 1][j - 1].rgbtGreen;
                    blue += copy[i + 1][j - 1].rgbtBlue;
                    pixel_num++;
                }
                red += copy[i + 1][j].rgbtRed;
                green += copy[i + 1][j].rgbtGreen;
                blue += copy[i + 1][j].rgbtBlue;
                pixel_num++;
                if (j + 1 < width)
                {
                    red += copy[i + 1][j + 1].rgbtRed;
                    green += copy[i + 1][j + 1].rgbtGreen;
                    blue += copy[i + 1][j + 1].rgbtBlue;
                    pixel_num++;
                }
            }
            // Write onto the image, the blurred rgb values
            image[i][j].rgbtRed = round(red / (float) pixel_num);
            image[i][j].rgbtGreen = round(green / (float) pixel_num);
            image[i][j].rgbtBlue = round(blue / (float) pixel_num);
        }
    }
    return;
}
