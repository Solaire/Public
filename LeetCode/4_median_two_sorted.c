#include "stdio.h"
#include "math.h"
#include <limits.h>

double findMedianSortedArrays(int* nums1, int nums1Size, int* nums2, int nums2Size);

int main(void)
{
    int nums1[] = {1, 3};
    int nums1Size = 2;
    int nums2[] = {2};
    int nums2Size = 1;

    double res = findMedianSortedArrays(nums1, nums1Size, nums2, nums2Size);

    return 0;
}

double findMedianSortedArrays(int* nums1, int nums1Size, int* nums2, int nums2Size)
{
    // Ensure that nums1 is the smaller array
    if(nums1Size > nums2Size)
    {
        return findMedianSortedArrays(nums2, nums2Size, nums1, nums1Size);
    }

    // Basic size variables + left-right partition for the smaller array
    int total = nums1Size + nums2Size;
    int half  = total / 2;
    int lo  = 0;
    int hi = nums1Size - 1;

    // Guaranteed a median so run infinitely
    while(1)
    {
        // Midpoints for the nums1 and nums2 arrays
        // variable b is calculated from the size difference
        int a = floor(lo + (hi - lo) / 2.0);
        int b = half - a - 2; // take away 2 because 0-based index

        int leftA  = (a     >= 0)        ? nums1[a]      : INT_MIN;
        int rightA = (a + 1 < nums1Size) ? nums1[a + 1]  : INT_MAX;

        int leftB  = (b     >= 0)        ? nums2[b]      : INT_MIN;
        int rightB = (b + 1 < nums2Size) ? nums2[b + 1]  : INT_MAX;

        // Partitions are correct, get the median
        if(leftA <= rightB && leftB <= rightA)
        {
            if(total & 1)
            {
                return fmin(rightA, rightB);
            }
            return (fmax(leftA, leftB) + fmin(rightA, rightB)) / 2.0f;
        }
        else if(leftA > rightB)
        {
            hi = a - 1;
        }
        else
        {
            lo = a + 1;
        }
    }
    return -1.f;
}