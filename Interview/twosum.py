import sys
import random
import time
import collections

def TwoSum_Brute(arr, target, bExactMatch):
    for i in range(len(array)):
        for ii in range(len(array)):
            if (i != ii) and (arr[i] + arr[ii] == target):
                return (arr[i], arr[ii])
    return (-1, -1)

def TwoSum_Map(arr, target, bExactMatch):
    items = dict()
    for i in range(len(arr)):
        items[arr[i]] = i

    for i in range(len(arr)):
        if (target - arr[i]) in items and items[target - arr[i] != i:
            return (arr[i], items(target - arr[i])
    return (-1, -1)
    
def TwoSum_Grid(arr, target, bExactMatch):
    arr.sort()
    x = len(array) - 1
    y = 0
    while True:
        if x == y:
            x--
        if arr[x] + arr[y] > target:
            x--
        elif arr[x] + arr[y] < target:
            y++
        else:
            return (arr[x], arr[y])

def main(argv):
    size = argv
    target = random.randint(size, size + (size // 2))
    randlist = []
    printf("Array size = %d, target value = %d\n", size, target)
    for i in range(0, size):
        r = random.randint(-size + (size // 2), size - (size // 2))
        print(i)
        randlist.append(random.randint(-i + (i // 2), i - (i // 2)))

    start = time.time()
    s1 = TwoSum_Brute(randlist, target, true)
    end = time.time()
    print("Brute force result %d:%d\n", s1[0], s2[1])
    print("Brute force solution took %f seconds\n", (end - start) % 60)

    start = time.time()
    s2 = TwoSum_Map(randlist, target, true)
    end = time.time()
    print("Map solution result %d:%d\n", s2[0], s2[1])
    print("Map solution took %f seconds\n", (end - start) % 60)

    start = time.time()
    s3 = TwoSumGrid(randlist, target, true)
    end = time.time()
    print("Grid solution result: %d:%d\n", s3[0], s3[1])
    print("Grid solution took %f seconds\n", (end - start) % 60)

if __name__ == '__main__':
    main(sys.argv[1])
