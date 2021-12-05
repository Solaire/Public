require "shared"

--[[ Task A:

]]
local function TaskA(hFile)
    local grid = {}
    
    local inputLine = hFile:read("*line")
    while inputLine do
        local points = StringSplit(inputLine, "->")
        local x1y1 = StringSplit(points[1], ",")
        local x2y2 = StringSplit(points[2], ",")
        if(x1y1[1] - x2y2[1] ~= 0) then
            for i = x1y1[1] + 1, x2y2[1] + 1 do
                if(grid[i][x1y1[2] + 1] == nil) then
                    grid[i][x1y1[2] + 1] = 1
                else
                    grid[i][x1y1[2] + 1] = grid[i][x1y1[2] + 1] + 1
                end
            end
        else
            for i = x1y1[2] + 1, x2y2[2] + 1 do
                if(grid[x1y1[1] + 1][i] == nil) then
                    grid[x1y1[1] + 1][i] = 1
                else
                    grid[x1y1[1] + 1][i] = grid[x1y1[1] + 1][i] + 1
                end
            end
        end
        
        inputLine = hFile:read("*line")
    end
    
    print("123")
end

--[[ Task B:

]]
local function TaskB(hFile)
end

--[[ Main function:

    * Open the input file.
    * Solve task A or task B.
]]
local function Main(filename, taskPart)
    local hFile = OpenFile(filename)
    if(hFile == nil) then return 0 end

    local ret = 0
    if("a" == taskPart:lower()) then
        ret = TaskA(hFile)
    elseif("b" == taskPart:lower()) then
        ret = TaskB(hFile)
    else
        print("Second argument must be A or B!")
        ret = -1
    end
    io.close(hFile)
    return ret
end

Main(arg[1], arg[2])