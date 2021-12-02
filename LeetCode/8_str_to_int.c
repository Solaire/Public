#include <limits.h>
#include <stdint.h>

typedef char SIGN;
#define POSITIVE 1
#define NEGATIVE -1

/*

"42"
"   -42"
"4193 with words"
"words and 987"
"-91283472332"
"+1"
"+-12"
"20000000000000000000"
*/

int main(void)
{
    char * str = "-42";
    int res = myAtoi(str);
    return 0;
}

int myAtoi(char * s)
{
    SIGN sign = POSITIVE;
    int len   = strlen(s);
    int i     = 0;
    int val   = 0;

    while(i < len && s[i] == ' ')
    {
        i++;
        // Ignore leading whitespace
    }

    if(s[i] == '-' || s[i] == '+')
    {
        sign = (s[i] == '-') ? NEGATIVE : POSITIVE;
        i++;
    }

    while(i < len && s[i] >= 0x30 && s[i] <= 0x39)
    {
        val += (s[i] - 0x30) * sign;
        val *= 10;
        if(val / 10 < INT_MIN || val / 10 > INT_MAX)
        {
            return fmin(INT_MAX, fmax(INT_MIN, val / 10));
        }
        i++;
    }
    if(val == 0)
    {
        return 0;
    }
    return fmin(INT_MAX, fmax(INT_MIN, val / 10));

    /*
    BOOL isPositive = TRUE;
    BOOL started    = FALSE;
    int len = strlen(s);
    int32_t val = 0;
    
    for(int i = 0; i < len; i++)
    {        
        if(s[i] == '-' && !started)
        {
            isPositive = FALSE;
            started    = TRUE;
        }
        else if(s[i] == '+' && !started)
        {
            isPositive = TRUE;
            started    = TRUE;
        }
        else if(s[i] == ' ' && !started)
        {
            // ignore leading whitespace
        }
        else if(s[i] >= 0x30 && s[i] <= 0x39)
        {
            if(val >= INT_MIN && val <= INT_MAX)
            {
                //val += s[i] - 0x30;
                val = (isPositive) ? val + (s[i] - 0x30) ? val - (s[i] - 0x30);
                val *= 10LL;
                started = TRUE;
            }
        }
        else // First non-digit character. Return whe we found
        {
            break;
        }
    }

    if(val == 0)
    {
        return 0;
    }
    val /= 10LL;

    int64_t ret = fmin(INT_MAX, fmax(INT_MIN, val));
    if(!isPositive)
    {
        ret *= -1;
    }
    return fmin(INT_MAX, fmax(INT_MIN, ret));
    */
}