#include "stdio.h"

int main(void)
{
    int nums[] = {1,3,5,6};
    int numsSize = 4;
    int target = 2;
    int expected = 1;

    if(searchInsert(nums, numsSize, target) == expected)
    {
        printf("Success");
    }
    else
    {
        printf("Failure");
    }
    return 0;
}

int searchInsert(int* nums, int numsSize, int target)
{
    int lo = 0;
    int hi = numsSize - 1;
    while(lo < hi)
    {
        int mid = (lo + hi) / 2;
        if(target == nums[mid])
        {
            return mid;
        }
        if(target > nums[mid])
        {
            lo = mid + 1;
        }
        else if(target < nums[mid])
        {
            hi = mid;
        }
    }
    int index = (lo + hi) / 2;
    if(target > nums[index])
    {
        return index + 1;
    }
    if(target < nums[index])
    {
        return index;
    }
    return index;
}