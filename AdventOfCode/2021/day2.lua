require "shared"

--[[ Task A:

    * Input file contains a planned course for a submarine.
    * Each line represents a command and a value:
    - forward X increases the horizontal position by X units.
    - down X increases the depth by X units.
    - up X decreases the depth by X units.
    * Calculate the horizontal position and
    depth you would have after following the planned course.
    * Return the product of depth and horizontal position.
]]
local function SubmarineMovement(hFile)
    local depth = 0
    local horizontal = 0

    local inputLine = hFile:read("*line")
    while inputLine do
        local input = StringSplit(inputLine, " ")
        if("forward" == input[1]:lower()) then
            horizontal = horizontal + tonumber(input[2])
        elseif ("down" == input[1]:lower()) then
            depth = depth + tonumber(input[2])
        elseif ("up" == input[1]:lower()) then
            depth = depth - tonumber(input[2])
        end
        inputLine = hFile:read("*line")
    end

    print(string.format("Product of depth and horizontal position = %d", depth * horizontal))
    return depth * horizontal
end

--[[ Task B:

    * Input file contains a planned course for a submarine.
    * Each line represents a command and a value:
    - down X increases your aim by X units.
    - up X decreases your aim by X units.
    - forward X does two things:
        - It increases your horizontal position by X units.
        - It increases your depth by your aim multiplied by X.
    * Calculate the horizontal position and
    depth you would have after following the planned course.
    * Return the product of depth and horizontal position.
]]
local function SubmarineAim(hFile)
    local depth = 0
    local horizontal = 0
    local aim = 0

    local inputLine = hFile:read("*line")
    while inputLine do
        local input = StringSplit(inputLine, " ")
        if("forward" == input[1]:lower()) then
            horizontal = horizontal + tonumber(input[2])
            depth = depth + (aim * tonumber(input[2]))
        elseif ("down" == input[1]:lower()) then
            aim = aim + tonumber(input[2])
        elseif ("up" == input[1]:lower()) then
            aim = aim - tonumber(input[2])
        end
        inputLine = hFile:read("*line")
    end

    print(string.format("Product of depth and horizontal position = %d", depth * horizontal))
    return depth * horizontal
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
        ret = SubmarineMovement(hFile)
    elseif("b" == taskPart:lower()) then
        ret = SubmarineAim(hFile)
    else
        print("Second argument must be A or B!")
        ret = -1
    end
    io.close(hFile)
    return ret
end

Main(arg[1], arg[2])