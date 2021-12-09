require "shared"

local function Difference(a, b)
    local cpy = a
    b:gsub(".", function(char)
        cpy = cpy:gsub(char, "") 
    end)
    return cpy
end

local function Contains(a, b)
    found = true
    b:gsub(".", function(char)
        if(not string.find(a, char)) then
            found = false
            return
        end
    end)
    return found
end

--[[ Task A:

]]
local function TaskA(inputArray)
    
    local count = 0
    for i = 1, #inputArray do
        local split = StringSplit(inputArray[i], '|')
        local out = StringSplit(split[2], " ")
        
        for i = 1, #out do
            local len = string.len(out[i])
            if((len >= 2 and len <= 4) or len == 7) then
                count = count + 1
            end
        end
    end
  
    return count, {}
end

--[[ Task B:

]]
local function TaskB(inputArray)
    
    local retVal = 0
    
    for i = 1, #inputArray do
        local split = StringSplit(inputArray[i], '|')
        local patterns = StringSplit(split[1], " ")
        local outVals  = StringSplit(split[2], " ")
        
        table.sort(patterns, function(a, b) return string.len(a) < string.len(b) end)
        
        --[[ 
            4 numbers have unique number of segments:
            1 = 2 segments
            4 = 4 segments
            7 = 3 segments
            8 = 7 segments (all)
            
            If number has 5 segments:
            3 = if contains all segments of number 1
            5 = if contains the difference of numbers 4 and 1 (little L shape)
            2 = if both of the above are false
            
            If number has 6 segments:
            9 = if contains all segments of number 4
            6 = if contains the difference of numbers 4 and 1 (little L shape) (note) number 9 also contains the 'L' shape)
            0 = if both of the above are false
        ]]
        
        -- Once sorted, the first three are 1, 7, 4 and last one is 8
        local one   = patterns[1]
        local four  = patterns[3]
        local seven = patterns[2]
        local eight = patterns[10]
        local fourDiff = Difference(four, one) -- Get the small 'L' shape
        
        local tmp = 0
        for ii = 1, #outVals do
            local len = string.len(outVals[ii])
            
            if(len == 2) then
                tmp = tmp + 1
            elseif(len == 3) then
                tmp = tmp + 7
            elseif(len == 4) then
                tmp = tmp + 4
            elseif(len == 7) then
                tmp = tmp + 8
                
            elseif(len == 5 and Contains(outVals[ii], one)) then
                tmp = tmp + 3
            elseif(len == 5 and Contains(outVals[ii], fourDiff)) then
                tmp = tmp + 5
            elseif(len == 5) then  
                tmp = tmp + 2
                
            elseif(len == 6 and Contains(outVals[ii], four)) then
                tmp = tmp + 9
            elseif(len == 6 and Contains(outVals[ii], fourDiff)) then
                tmp = tmp + 6
            end
            
            tmp = tmp * 10
        end
        
        tmp = tmp / 10
        retVal = retVal + tmp
    end
    
    return retVal, {}
end

--[[ Main function:

    * Open the input file and add the content to a list.
    * Solve task A and task B
    * Plot the population growth of lanternfish over time
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
  
    retTaskA, plotTaskA = TaskA(inputArray)
    retTaskB, plotTaskB = TaskB(inputArray)
    
    -- Start plotting
    local wnd = graph.window("v..")
        
    local p1 = graph.plot("Lanternfish daily growth rate")
    local p1Line = graph.filine(function(i) return plotTaskA[i][2], plotTaskA[i][1] end, 1, #plotTaskA)
    p1:addline(p1Line, "red")
    p1.xtitle = "Time (days)"
    p1.ytitle = "Population"
    --[[
    local p2 = graph.plot("Submarine depth changes (angled)")
    local p2Line = graph.filine(function(i) return plotTaskB[i][2], plotTaskB[i][1] end, 1, #plotTaskB)
    p2:addline(p2Line, "blue")
    p2.xtitle = "Horizontal position"
    p2.ytitle = "Depth change"
    ]]
    wnd:attach(p1, "2")
    --wnd:attach(p2, "1")
    wnd:save_svg("outputs\\day7.svg", 1500, 1500)
  
    return 0
end

Main(arg[1])