// Encrypt a message using Caesar's cypher

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

bool only_digits(string s);
char rotate(char ch, int i);

int main(int argc, string argv[])
{
    // Fallback
    if ((argc != 2) || (only_digits(argv[1]) == false))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        // Convert argv[1] to an integer
        int key = atoi(argv[1]);

        // Prompt the user for text
        string text = get_string("plaintext:  ");

        // Rotate the character by the key
        for (int i = 0; i < strlen(text); i++)
        {
            text[i] = rotate(text[i], key);
        }
        printf("ciphertext: %s\n", text);
    }
}

// Check whether each character in the string is a digit
bool only_digits(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        if (isdigit(s[i]))
        {
            continue;
        }
        else
        {
            return false;
        }
    }
    return true;
}

// Rotate a char to a certain int, if it is an alphabet, or return the same char otherwise
char rotate(char ch, int i)
{
    if (isalpha(ch))
    {
        if (isalpha(ch + i))
        {
            return ch + i;
        }
        // If ch is not an alphabet
        else
        {
            char base = isupper(ch) ? 'A' : 'a';
            return (char)(((ch - base + i) % 26) + base);
        }
    }
    return ch;
}