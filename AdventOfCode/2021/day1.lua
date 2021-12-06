require "shared"
require "graph"

--[[ Task A:

    * Each value in the input array represents a depth measurement.
    * Count the number of times a depth measurement
    increases from the previous measurement.
    * Return the counter and a table of sample differences
]]
local function DepthIncrements(inputArray)
    local incrementCount = 0
    local sampleDiff = {}
    
    for i = 2, #inputArray do
        if(inputArray[i] > inputArray[i - 1]) then
            incrementCount = incrementCount + 1
        end
        table.insert(sampleDiff, inputArray[i] - inputArray[i - 1])
    end
    print(string.format("Number of depth increments: %d", incrementCount))
    return incrementCount, sampleDiff
end

--[[ Task B:

    * Each value in the input array represents a depth measurement.
    * Create a three-measurement sliding window, which sums the values 
    (i, i + 1, i + 2) and compares them to the next window (i + 1, i + 2, i + 3).
    * Count the number of times the sum of measurements 
    in this sliding window increases from the previous sum.
    * Return the counter and a table of sample differences
]]
local function SlidingWindowIncrements(inputArray)
    local incrementCount = 0
    local i = 1
    local sampleDiff = {}
    
    while(i + 3 <= #inputArray) do
        local sumA = inputArray[i]     + inputArray[i + 1] + inputArray[i + 2]
        local sumB = inputArray[i + 1] + inputArray[i + 2] + inputArray[i + 3]
        if(sumB > sumA) then
            incrementCount = incrementCount + 1
        end
        i = i + 1
        table.insert(sampleDiff, sumB - sumA)
    end
    print(string.format("Number of cumulative depth increments: %d", incrementCount))
    return incrementCount, sampleDiff
end

--[[ Main function:

    * Open the input file and add the content to a list.
    * Solve task A and task B
    * Plot the difference in depth samples for both tasks and save the graph
]]
local function Main(filename)
    local hFile = OpenFile(filename)
    if(hFile == nil) then return 0 end

    local inputArray = {}
    local inputLine = hFile:read("*line")
    while inputLine do
        table.insert(inputArray, tonumber(inputLine))
        inputLine = hFile:read("*line")
    end
    io.close(hFile)

    local retTaskA = 0 
    local retTaskB = 0
    local plotTaskA = {}
    local plotTaskB = {}
    
    retTaskA, plotTaskA = DepthIncrements(inputArray)
    retTaskB, plotTaskB = SlidingWindowIncrements(inputArray)
    
    -- Start plotting
    local wnd = graph.window("v..")
    
    local p1 = graph.plot("Difference in single depth samples")
    local p1Line = graph.filine(function(i) return plotTaskA[i] end, 1, #plotTaskA)
    p1:addline(p1Line, "red")
    p1.xtitle = "Sample index"
    p1.ytitle = "Sample difference"
    
    local p2 = graph.plot("Difference in cumulative depth samples")
    local p2Line = graph.filine(function(i) return plotTaskB[i] end, 1, #plotTaskB)
    p2:addline(p2Line, "blue")
    p2.xtitle = "Sample sliding window index"
    p2.ytitle = "Sample sum difference"
    
    wnd:attach(p1, "2")
    wnd:attach(p2, "1")
    wnd:save_svg("outputs\\day1.svg", 1500, 1500)
    
    ret 0
end

Main(arg[1])