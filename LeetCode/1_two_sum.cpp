#include <stdlib.h>
#include <vector>
#include <map>
#include <algorithm>

class Solution 
{
public:
    std::vector<int> twoSum(std::vector<int>& nums, int target) 
    {
        int a = 0;
        int b = 0;
        //BruteForce(nums, target, a, b);
        //FastMapSolution(nums, target, a, b);
        FastGridSolution(nums, target, a, b);
        std::vector<int> ret;
        ret.push_back(a);
        ret.push_back(b);
        return ret;
    }

private:
    // Sort the vector and traverse it from both ends until the target is found
    // or until the both indexes meet
    // Time Complexity: O(N log(N)) // std::sort
    // Space Complexity O(n)
    void FastGridSolution(std::vector<int>& nums, int target, int & a, int & b)
    {
        a = -1;
        b = -1;
        int start   = 0;
        int end     = nums.size() - 1;
        std::sort(nums.begin(), nums.end());
        
        while(start < nums.size() && end > 0)
        {
            if(start == end)            
            {
                end--;
            }
            if(target < nums[start] + nums[end])
            {
                end--;
            }
            else if(target > nums[start] + nums[end])
            {
                start++;
            }
            else
            {
                a = start;
                b = end;
                return;
            }
        }
    }
    
    // Use the map structure to cache visited elements
    // Iterate through the vector once, checking if the map contains a value
    // equal to (target - nums[i])
    // Time Complexity: O(n)
    // Space Complexity O(n*2)
    void FastMapSolution(std::vector<int>& nums, int target, int & a, int & b)
    {
        std::map<int, int> mp;
        a = -1;
        b = -1;

        for(int i=0; i < nums.size(); i++)
        {
            if(mp.find(target - nums[i]) != mp.end())
            {
                a = mp[target-nums[i]];
                b = i;
                return;
            }
            mp[nums[i]] = i;
        }
    }
    
    // Naive brute force approach
    // Compare the nth element with all further elements until found
    // Time Complexity: O(n^2)
    void BruteForce(std::vector<int>& nums, int target, int & a, int & b)
    {
        a = -1;
        b = -1;
        for(int i = 0; i < nums.size(); i++)
        {
            for(int ii = i; ii < nums.size(); ii++)
            {
                if(i == ii)
                {
                    continue;
                }
                if(nums[i] + nums[ii] == target)
                {
                    a = i;
                    b = ii;
                    return;
                }
            }
        }
    }
};

int main(void)
{
    Solution sol;
    std::vector<int> a;
    a.push_back(3);
    a.push_back(2);
    a.push_back(4);
    int target = 6;

    std::vector<int> b = sol.twoSum(a, target);

    return 0;
}