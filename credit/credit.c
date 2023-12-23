// Algorithm to check whether a credit card number is valid
#include <cs50.h>
#include <stdio.h>
#include <math.h>

string type(long n);
int length(long n);

int main(void)
{
    // Prompt the user for the credit card number
    long n = get_long("Number: ");

    // Luhn's Algorithm
    int evenSum = 0;
    for (int i = 2; (n / (long) pow(10, i - 2)) > 0; i += 2)
    {
        // To shift the position of the required digits to unit place
        long temp = n / (long)pow(10, i - 1);
        // Extract the number
        long digit = temp % 10;
        // Multiply the digit by 2
        digit *= 2;
        // Adding the digits
        for (int sum = 0; digit > 0; digit /= 10)
        {
            evenSum += digit % 10;
        }
    }
    int oddSum = 0;
    for (int i = 1; (n / (long) pow(10, i - 1)) > 0; i += 2)
    {
        long temp = n / (long) pow(10, i - 1);
        long digit = temp % 10;
        for (int sum = 0; digit > 0; digit /= 10)
        {
            oddSum += digit % 10;
        }
    }

    // Total
    int sum = evenSum + oddSum;

    // Check if the total's last digit is 0
    if (sum % 10 == 0)
    {
        printf("%s\n", type(n));
    }
    else
    {
        printf("INVALID\n");
    }
}

// Function that prints the length of the number
int length(long n)
{
    int i = 0;
    while (n != 0)
    {
        // Utilising Truncation
        n = n / 10;
        i++;
    }
    return i;
}

// Function that prints the type of the card , if valid
string type(long n)
{
    int firstDigit = n / (long) pow(10, length(n) - 1);
    int secondDigit = (n / (long) pow(10, length(n) - 2)) % 10;
    if (firstDigit == 3)
    {
        if ((secondDigit == 4 || secondDigit == 7) && length(n) == 15)
        {
            return "AMEX";
        }
        else
        {
            return "INVALID";
        }
    }
    else if (firstDigit == 4 && (length(n) == 13 || length(n) == 16))
    {
        return "VISA";
    }
    else if ((firstDigit == 5) && length(n) == 16)
    {
        if (secondDigit == 1 || secondDigit == 2 || secondDigit == 3 || secondDigit == 4 || secondDigit == 5)
        {
            return "MASTERCARD";
        }
        else
        {
            return "INVALID";
        }
    }
    else
    {
        return "INVALID";
    }
}