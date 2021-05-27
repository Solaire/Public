import sys
import random
import time
import collections

'''
    Naive brute force search
    Compare each element against each other element.
    Very Slow
    Return first matching pair
'''
def TwoSum_Brute(arr, target):
    for i in range(len(arr)):
        for ii in range(len(arr)):
            if (i != ii) and (arr[i] + arr[ii] == target):
                return (arr[i], arr[ii])
    return (-1, -1)

'''
    
'''
def TwoSum_Map(arr, target):
    items = dict()
    for i in range(len(arr)):
        items[arr[i]] = i

    for i in range(len(arr)):
        if (target - arr[i]) in items and items[target - arr[i]] != i:
            return (arr[i], target - arr[i])
    return (-1, -1)
    
def TwoSum_Grid(arr, target):
    arr.sort()
    x = len(arr) - 1
    y = 0
    while x > 0 and y < len(arr):
        if x == y:
            x -= 1
        if arr[x] + arr[y] > target:
            x -= 1
        elif arr[x] + arr[y] < target:
            y += 1
        else:
            return (arr[x], arr[y])

def main(argv):
    size = argv
    target = random.randint(size - (size // 2), (size * 2) - (size // 2))
    arr = list(range(1, size))

    print("Array size = {}, target value = {}".format(size, target))
    print("Array: {}\n".format(arr))

    start = time.time()
    s1 = TwoSum_Brute(arr, target)
    end = time.time()
    print("Brute force result {}:{}".format(s1[0], s1[1]))
    print("Brute force solution took {} seconds\n".format((end - start) % 60))
    
    start = time.time()
    s2 = TwoSum_Map(arr, target)
    end = time.time()
    print("Map solution result {}:{}".format(s2[0], s2[1]))
    print("Map solution took {} seconds\n".format((end - start) % 60))
    
    start = time.time()
    s3 = TwoSum_Grid(arr, target)
    end = time.time()
    print("Grid solution result: {}:{}".format(s3[0], s3[1]))
    print("Grid solution took {} seconds\n".format((end - start) % 60))

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        print("Provide array size")
        return
    main(sys.argv[1])
