require "shared"

--[[ Task A:

]]
local function TaskA(inputLines)
    local braceVals = {}
    braceVals['('] = 2
    braceVals[')'] = 3
    braceVals['['] = 56
    braceVals[']'] = 57
    braceVals['{'] = 1196
    braceVals['}'] = 1197
    braceVals['<'] = 25136
    braceVals['>'] = 25137
    
    local ret = 0
    for i = #inputLines, 1, -1 do
        local inString = ""
        for char in inputLines[i]:gmatch"." do
            if((braceVals[char] % 2) == 0) then
                inString = inString..char
            elseif(braceVals[char] - braceVals[inString:sub(-1)] == 1) then
                inString = string.sub(inString, 1, #inString - 1)
            else
                ret = ret + braceVals[char]
                table.remove(inputLines, i)
                break
            end
        end
    end
    
    return ret, {}
end

--[[ Task B:

]]
local function TaskB(inputLines)
    local braceVals = {}
    braceVals['('] = 11
    braceVals[')'] = 1
    braceVals['['] = 12
    braceVals[']'] = 2
    braceVals['{'] = 13
    braceVals['}'] = 3
    braceVals['<'] = 14
    braceVals['>'] = 4
    
    points = {}
    
    local ret = 0
    for i = 1, #inputLines do
        points[i] = 0
        local inString = ""
        for char in inputLines[i]:gmatch"." do
            if(braceVals[char] > 10) then
                inString = inString..char
            elseif(braceVals[char] - braceVals[inString:sub(-1)] == -10) then
                inString = string.sub(inString, 1, #inString - 1)
            end
        end
        
        repeat
            local lastChar = inString:sub(-1)
            points[i] = (points[i] * 5) + (braceVals[lastChar] - 10)
            inString = string.sub(inString, 1, #inString - 1)
        until(#inString == 0)
    end
    
    table.sort(points)
    ret = ((#points + 1) // 2)
    return points[ret], {}
end

--[[ Main function:

    * Open the input file and add the content to a list.
    * Solve task A and task B
    * Plot the population growth of lanternfish over time
]]
local function Main(filename, taskPart)
    local hFile = OpenFile(filename)
    if(hFile == nil) then return 0 end

    local grid = {}
    local inputLine = hFile:read("*line")
    local rowLen = #inputLine
    
    while inputLine do
        table.insert(grid, inputLine)
        inputLine = hFile:read("*line")
    end
    io.close(hFile)

    local retTaskA = 0 
    local retTaskB = 0
    local plotTaskA = {}
    local plotTaskB = {}
  
    retTaskA, plotTaskA = TaskA(grid)
    retTaskB, plotTaskB = TaskB(grid)
  
    return 0
end

Main(arg[1])