// Convert text into instructions for the strip of bulbs on CS50’s stage

#include <cs50.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    string message = get_string("Message: ");

    for (int i = 0; i < strlen(message); i++)
    {
        // Convert each character in the string to a decimal
        int ascii = (int)message[i];

        // Array that stores the binary value of each decimal
        int bin[8] = {};

        // Convert decimal to 8-bit binary
        for (int j = 0 ; j < 8; j++)
        {
            if (ascii % 2 != 1)
            {
                bin[j] = 0;
                ascii = ascii / 2;
            }
            else
            {
                bin[j] = 1;
                ascii = ascii / 2;
            }
        }

        // Print the bulbs (in reverse order)
        for (int k = 0 ; k < 8; k++)
        {
            print_bulb(bin[7 - k]);
        }
        printf("\n");
    }
}

// Print an on/off bulb
void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}

