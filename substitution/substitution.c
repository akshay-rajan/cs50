// Encrypt a message using substitution

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

bool validity(string s);
bool norepeat(string s);
bool isalphas(string s);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    if (validity(argv[1]) == false)
    {
        printf("Key invalid!\n");
        return 1;
    }

    // Prompt the user for a string
    string s = get_string("plaintext:");

    string key = argv[1];

    // Substitution
    for (int i = 0; i < strlen(s); i++)
    {
        // Replace each char in the string by the corresponding key
        int position;
        if (islower(s[i]))
        {
            position = s[i] - 97;
            s[i] = tolower(key[position]);
        }
        else if (isupper(s[i]))
        {
            position = s[i] - 65;
            s[i] = toupper(key[position]);
        }
    }
    printf("ciphertext:%s\n", s);
    return 0;
}

// Check if a key is valid
bool validity(string s)
{
    if (isalphas(s) && strlen(s) == 26 && norepeat(s))
    {
        return true;
    }
    return false;
}

// Check if a letter repeats
bool norepeat(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        for (int j = 0; j < strlen(s); j++)
        {
            if (i != j && s[i] == s[j])
            {
                return false;
            }
        }
    }
    return true;
}

// Check if a string contains only alphabets
bool isalphas(string s)
{
    for (int i = 0; i < strlen(s); i++)
    {
        // Check if each character is an alphabet
        if (isalpha(s[i]) == false)
        {
            return false;
        }
    }
    return true;
}