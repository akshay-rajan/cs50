#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt the user for height of the pyramid
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    // Print the pyramid
    for (int i = 0; i < h; i++)
    {
        int x = h - i - 1;

        // Print 'x' spaces in each row
        for (int j = 0; j < x; j++)
        {
            printf(" ");
        }
        // Print 'h-x=i' #'s in each row
        for (int k = x; k < h; k++)
        {
            printf("#");
        }
        // Print two spaces in each row
        printf("  ");
        // Print 'h-x=i' #'s again
        for (int k = x; k < h; k++)
        {
            printf("#");
        }
        printf("\n");
    }

}