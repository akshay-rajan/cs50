// Recursion
#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Global variable
int value = 0;

int convert(string input);

int main(void)
{
    string input = get_string("Enter a positive integer: ");

    // Check whether each character in the input is a number
    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (!isdigit(input[i]))
        {
            printf("Invalid Input!\n");
            return 1;
        }
    }

    // Convert string to int
    printf("%i\n", convert(input));
}

int convert(string input)
{
    // Length of the string: till the null terminator
    int len = strlen(input);

    // Base Case: null terminator at the beginning of the string
    if (len == 0)
    {
        return value;
    }

    int temp = 0;
    for (int i = len - 1; i >= 0; i--)
    {
        // To get the actual integer value, by subtract the (ascii value of the) base, and store it in 'temp'
        temp = input[i] - '0';

        // Replace that char with null, declaring it as the end of the string
        input[i] = '\0';

        // Calling the function 'len' times; converting (or just calling) each char from the end to an int and reducing the size of the string
        convert(input);

        // When len = 0: base case: calculate "value"
        // Value is 10 times the value of the rest of the digits, plus the value of the last digit----------RECURSION
        value = value * 10 + temp;
        return value;
    }
    return value;
}