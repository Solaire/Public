require "shared"
local BinaryScale = require "scale"

--[[ Task A:

    * Input file contains a diagnostic report data, in the
    form of binary numbers
    * The binary numbers can be used to generate two values:
    - Gamma rate,
    - Epsilon rate
    * Each bit of the gamma and epsilon rates can be determined by either
    the most common bit (gamma rate) and the least common bit (epsilon rate)
    in the corresponding position of all numbers in the diagnostic report
    * Product of gamma rate and epsilon rate will generate the power consumption value
    
]]
local function CalculatePowerConsumption(hFile)
    local bitCounter = {}
    local lineCounter = 0

    -- Count all  the times 1 appears in the given position
    local inputLine = hFile:read("*line")
    while inputLine do
        lineCounter = lineCounter + 1
        local i = 1

        for c in inputLine:gmatch"." do
            if("1" == c and bitCounter[i] ~= nil) then
                bitCounter[i] = bitCounter[i] + 1
            elseif("1" == c) then
                bitCounter[i] = 1
            end
            i = i + 1
        end
        inputLine = hFile:read("*line")
    end

    -- Create two lists which will represent the final binary numbers
    local mostCommon = {}
    local leastCommon = {}
    for i, val in ipairs(bitCounter) do
        if(val == lineCounter / 2) then
            -- Ignore
        elseif(val > lineCounter / 2) then
            mostCommon[i] = "1"
            leastCommon[i] = "0"
        else
            mostCommon[i] = "0"
            leastCommon[i] = "1"
        end
    end

    -- Convert the binary numbers to numbers
    local s = ""
    for k, v in ipairs(mostCommon) do
        s = s..v
    end
    local gamma = tonumber(s, 2)

    s = ""
    for k, v in ipairs(leastCommon) do
        s = s..v
    end
    local epsilon = tonumber(s, 2)

    print(string.format("Gamma rate: %d", gamma))
    print(string.format("Epsilon rate: %d", epsilon))
    print(string.format("Power consumption: %d", gamma * epsilon))

    return gamma * epsilon
end

--[[ Task B:

    * Input file contains a diagnostic report data, in the
    form of binary numbers
    * The binary numbers can be used to generate two values:
    - Oxygen generator rating,
    - CO2 scrubber rating,
    * Both values are located using a similar process that involves
    filtering out values until only one remains. Before searching 
    for either rating value, start with the full list of binary numbers from
    your diagnostic report and consider just the first bit of those numbers.
    Then:
        - Keep only numbers selected by the bit criteria for the type of rating 
        value for which you are searching. Discard numbers which do not match the bit criteria.
        - If you only have one number left, stop; this is the rating value for which you are searching.
        - Otherwise, repeat the process, considering the next bit to the right.

    * The bit criteria depends on which type of rating value you want to find:
        - To find oxygen generator rating, determine the most common value (0 or 1) in the
        current bit position, and keep only numbers with that bit in that position. If 0 and 1
        are equally common, keep values with a 1 in the position being considered.
        - To find CO2 scrubber rating, determine the least common value (0 or 1) in
        the current bit position, and keep only numbers with that bit in that position.
        If 0 and 1 are equally common, keep values with a 0 in the position being considered.
    * Product of Oxygen generator rating and the CO2 scrubber rating will
    generate the life support rating value
]]
local function CalculateLifeSupportRating(hFile)
    local maxScale = BinaryScale:Create()
    local minScale = BinaryScale:Create()
    
    local inputLine = hFile:read("*line")
    maxScale:SetFilter(0x1 << (#inputLine - 1))
    minScale:SetFilter(0x1 << (#inputLine - 1))

    while inputLine do
        maxScale:Insert(tonumber(inputLine, 2))
        minScale:Insert(tonumber(inputLine, 2))
        inputLine = hFile:read("*line")
    end

    local left, right = maxScale:GetListSize()
    repeat
        maxScale:ShiftFilter(1)
        maxScale:UpdateLists(right >= left)
        left, right = maxScale:GetListSize()
    until(left + right <= 2) 
    local oxygen = maxScale:GetMaxValue()

    left, right = minScale:GetListSize()
    repeat
        minScale:ShiftFilter(1)
        minScale:UpdateLists(left > right)
        left, right = minScale:GetListSize()
    until(left + right <= 2)
    local co2 = minScale:GetMinValue()
    print(string.format("Oxygen generator rating: %d", oxygen))
    print(string.format("CO2 scrubber rating: %d", co2))
    print(string.format("Life support rating: %d", oxygen * co2))
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
        ret = CalculatePowerConsumption(hFile)
    elseif("b" == taskPart:lower()) then
        ret = CalculateLifeSupportRating(hFile)
    else
        print("Second argument must be A or B!")
        ret = -1
    end
    io.close(hFile)
    return ret
end

Main(arg[1], arg[2])