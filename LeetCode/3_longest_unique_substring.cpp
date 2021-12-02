#include <iostream>
#include <string>
#include <unordered_map>

class Solution 
{
public:
    int lengthOfLongestSubstring(std::string s) 
    {
        int longest = 0;
        int start = 0;
        std::unordered_map<char, int> cache;
    
        for(int i = 0; i < s.length(); i++)
        {
            std::cout << s[i] << std::endl;
            std::unordered_map<char, int>::const_iterator it = cache.find(s[i]);

            // Character already encountered and between start and current index
            if(it != cache.end() && it->second >= start)
            {
                start = it->second + 1;
            }
            else if(1 + i - start > longest) 
            {
                longest = 1 + i - start;
            }
            cache[s[i]] = i;
        }
        return longest;
    }
};

int main(void)
{
    Solution s;
    int val = s.lengthOfLongestSubstring("tmmzuxt");
    return 0;
}
