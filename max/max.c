// Practice writing a function to find a max value

#include <cs50.h>
#include <stdio.h>

int max(int array[], int n);

int main(void)
{
    int n;
    do
    {
        n = get_int("Number of elements: ");
    }
    while (n < 1);

    int arr[n];

    for (int i = 0; i < n; i++)
    {
        arr[i] = get_int("Element %i: ", i);
    }

    printf("The max value is %i.\n", max(arr, n));
}

// Return the max value
int max(int array[], int n)
{
    // Use similar algorithm as bubble sort
    for (int i = 0; i < n - 1; i++)
    {
        if (array[i] > array[i + 1])
        {
            // Swap
            int x = array[i];
            int y = array[i + 1];
            array[i + 1] = x;
            array[i] = y;
        }
    }
    // This leads to the maximum value ending up at the final position of the array
    return array[n - 1];
}
