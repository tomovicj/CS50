#include <cs50.h>
#include <stdio.h>

int counter(long number);
int check(long number);
string card(long number, int length);


int main(void)
{
    // Ask user for card number
    long number = get_long("Number: ");

    // Get length of a number
    int length = counter(number);

    printf("%s\n", card(number, length));
}

int counter(long number)
{
    // Credit card numbers can only be 13-16 digits long
    if (number >= 10000000000000000) return -1;             // Return -1 if the number is higher than 16 digits
    if (number >= 1000000000000000) return 16;              // Return 16 if number is 16 digits long
    if (number >= 100000000000000) return 15;               // Return 15 if number is 15 digits long
    if (number >= 10000000000000) return 14;                // Return 14 if number is 14 digits long
    if (number >= 1000000000000) return 13;                 // Return 13 if number is 13 digits long
    return -1;                                              // Return -1 if the number is lower than 13 digits
}

int check(long number)
{
    long n = number;
    int a = 0;
    int a_temp;
    int b = 0;
    int sum;
    int x = 1;

    for (long _ = 1; _ <= number; _ *= 10)
    {
        n /= x;
        b += n % 10;
        x = 10;

        n /= x;
        a_temp = n % 10 * 2;

        // Checks if 'a_temp' is two digit number
        if (a_temp >= 10 && a_temp <= 99)
        {
            a += a_temp % 10;
            a_temp /= 10;
            a += a_temp % 10;
        }
        else
        {
            a += a_temp;
        }
    }
    sum = a + b;
    // Returns the last digit
    return sum % 10;
}

string card(long number, int length)
{
    int first_one;
    int first_two;
    if (length == -1 || check(number) != 0)
    {
        return "INVALID";
    }


    long x = 1;
    for (int _ = 0; _ < length - 2; _++)
    {
        x *= 10;
    }
    // Take first two digits
    first_two = number / x;


    if (first_two == 34 || first_two == 37)
    {
        return "AMEX";
    }
    if (first_two == 51 || first_two == 52 || first_two == 53 || first_two == 54 || first_two == 55)
    {
        return "MASTERCARD";
    }
    else
    {
        // Take first digit
        first_one = first_two / 10;
    }
    if (first_one == 4)
    {
        return "VISA";
    }
    else
    {
        return "INVALID";
    }
}
