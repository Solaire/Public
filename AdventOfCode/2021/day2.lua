require "shared"
require "graph"

--[[ Task A:

    * Input contains a planned course for a submarine.
    * Each entry represents a command and a value:
    - forward X increases the horizontal position by X units.
    - down X increases the depth by X units.
    - up X decreases the depth by X units.
    * Calculate the horizontal position and
    depth you would have after following the planned course.
    * Return the product of depth and horizontal position, and a record of depth changes.
]]
local function SubmarineMovement(inputArray)
    local depth = 0
    local horizontal = 0
    local depthChange = {}

    for i = 1, #inputArray do
        local input = StringSplit(inputArray[i], " ")
        local oldDepth = depth
        
        if("forward" == input[1]:lower()) then
            horizontal = horizontal + tonumber(input[2])
        elseif ("down" == input[1]:lower()) then
            depth = depth + tonumber(input[2])
        elseif ("up" == input[1]:lower()) then
            depth = depth - tonumber(input[2])
        end
        local xy = {horizontal, depth - oldDepth}
        table.insert(depthChange, xy)
    end

    print(string.format("Submarine depth: %d | horizontal position = %d", depth, horizontal))
    return depth * horizontal, depthChange
end

--[[ Task B:

    * Input contains a planned course for a submarine.
    * Each entry represents a command and a value:
    - down X increases your aim by X units.
    - up X decreases your aim by X units.
    - forward X does two things:
        - It increases your horizontal position by X units.
        - It increases your depth by your aim multiplied by X.
    * Calculate the horizontal position and
    depth you would have after following the planned course.
    * Return the product of depth and horizontal position, and a record of depth changes.
]]
local function SubmarineAim(inputArray)
    local depth = 0
    local horizontal = 0
    local aim = 0
    local depthChange = {}

    for i = 1, #inputArray do
        local input = StringSplit(inputArray[i], " ")
        local oldDepth = depth
        
        if("forward" == input[1]:lower()) then
            horizontal = horizontal + tonumber(input[2])
            depth = depth + (aim * tonumber(input[2]))
        elseif ("down" == input[1]:lower()) then
            aim = aim + tonumber(input[2])
        elseif ("up" == input[1]:lower()) then
            aim = aim - tonumber(input[2])
        end
        local xy = {horizontal, depth - oldDepth}
        table.insert(depthChange, xy)
    end

    print(string.format("Submarine depth: %d | horizontal position = %d", depth, horizontal))
    return depth * horizontal, depthChange
end

--[[ Main function:

    * Open the input file and add the content to a list.
    * Solve task A and task B
    * Plot the submarine depth changes for both task and save the graph
]]
local function Main(filename, taskPart)
    local hFile = OpenFile(filename)
    if(hFile == nil) then return 0 end

    local inputArray = {}
    local inputLine = hFile:read("*line")
    while inputLine do
        table.insert(inputArray, inputLine)
        inputLine = hFile:read("*line")
    end
    io.close(hFile)

    local retTaskA = 0 
    local retTaskB = 0
    local plotTaskA = {}
    local plotTaskB = {}
  
    retTaskA, plotTaskA = SubmarineMovement(inputArray)
    retTaskB, plotTaskB = SubmarineAim(inputArray)
    
    -- Start plotting
    local wnd = graph.window("v..")
        
    local p1 = graph.plot("Submarine depth changes (flat)")
    local p1Line = graph.filine(function(i) return plotTaskA[i][2], plotTaskA[i][1] end, 1, #plotTaskA)
    p1:addline(p1Line, "red")
    p1.xtitle = "Horizontal position"
    p1.ytitle = "Depth change"
    
    local p2 = graph.plot("Submarine depth changes (angled)")
    local p2Line = graph.filine(function(i) return plotTaskB[i][2], plotTaskB[i][1] end, 1, #plotTaskB)
    p2:addline(p2Line, "blue")
    p2.xtitle = "Horizontal position"
    p2.ytitle = "Depth change"
    
    wnd:attach(p1, "2")
    wnd:attach(p2, "1")
    wnd:save_svg("outputs\\day2.svg", 1500, 1500)
  
    return 0
end

Main(arg[1])