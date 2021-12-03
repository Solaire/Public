require "shared"

--[[ Task A:

    * Each value in the input array represents a depth measurement.
    * Count the number of times a depth measurement
    increases from the previous measurement.
    * Return the counter.
]]
local function DepthIncrements(inputArray)
    local incrementCount = 0
    for i = 2, #inputArray do
        if(inputArray[i] > inputArray[i - 1]) then
            incrementCount = incrementCount + 1
        end
    end
    print(string.format("Number of depth increments: %d", incrementCount))
    return incrementCount
end

--[[ Task B:

    * Each value in the input array represents a depth measurement.
    * Create a three-measurement sliding window, which sums the values 
    (i, i + 1, i + 2) and compares them to the next window (i + 1, i + 2, i + 3).
    * Count the number of times the sum of measurements 
    in this sliding window increases from the previous sum.
    * Return the counter.
]]
local function SlidingWindowIncrements(inputArray)
    local incrementCount = 0
    local i = 1
    while(i + 3 <= #inputArray) do
        local sumA = inputArray[i]     + inputArray[i + 1] + inputArray[i + 2]
        local sumB = inputArray[i + 1] + inputArray[i + 2] + inputArray[i + 3]
        if(sumB > sumA) then
            incrementCount = incrementCount + 1
        end
        i = i + 1
    end
    print(string.format("Number of sliding window sum increments: %d", incrementCount))
    return incrementCount
end

--[[ Main function:

    * Open the input file and add the content to a list.
    * Solve task A or task B.
]]
local function Main(filename, taskPart)
    local hFile = OpenFile(filename)
    if(hFile == nil) then return 0 end

    local inputArray = {}
    local inputLine = hFile:read("*line")
    while inputLine do
        table.insert(inputArray, tonumber(inputLine))
        inputLine = hFile:read("*line")
    end

    local ret = 0
    if("a" == taskPart:lower()) then
        ret = DepthIncrements(inputArray)
    elseif("b" == taskPart:lower()) then
        ret = SlidingWindowIncrements(inputArray)
    else
        print("Second argument must be A or B!")
        ret = -1
    end

    io.close(hFile)
    return ret
end

Main(arg[1], arg[2])