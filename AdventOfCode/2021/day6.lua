require "shared"
require "graph"

Fish = {timer = 0}
Fish.__index = Fish

function Fish:New(timer)
    self = {}
    self.timer = timer
    
    setmetatable(self, Fish)
    return self
end

function Fish:Reproduce()
    self.timer = self.timer - 1
  
    if(self.timer < 0) then
        self.timer = 6
        return true
    end
  
    return false
end

--[[ Task A:

]]
local function TaskA(inputArray)
    local fishArr = {}
    local count = 0
    
    for i = 0, 8 do
      fishArr[i] = 0
    end
    
    for i = 1, #inputArray do
      fishArr[tonumber(inputArray[i])] = fishArr[tonumber(inputArray[i])] + 1
    end
    
    for i = 1, 256 do
        local newFish = fishArr[0]
        fishArr[0] = fishArr[1]
        fishArr[1] = fishArr[2]
        fishArr[2] = fishArr[3]
        fishArr[3] = fishArr[4]
        fishArr[4] = fishArr[5]
        fishArr[5] = fishArr[6]
        fishArr[6] = fishArr[7] + newFish
        fishArr[7] = fishArr[8]
        fishArr[8] = newFish
        print(string.format("After %d day:  %d", i, fishArr[0] + fishArr[1] + fishArr[2] + fishArr[3] + fishArr[4] + fishArr[5] + fishArr[6] + fishArr[7] + fishArr[8]))
    end
    
    for i = 0, #fishArr do
      count = count + fishArr[i]
    end
    
    --[[
    for i = 1, #inputArray do
        table.insert(fishArr, Fish:New(tonumber(inputArray[i])))
    end
    
    for i = 1, 80 do
        local currentCount = #fishArr
        for ii = 1, currentCount do
            if(fishArr[ii]:Reproduce()) then
                table.insert(fishArr, Fish:New(8))
            end
        end
        print(string.format("After %d day:  %d (increase of %d)", i, #fishArr,  #fishArr - currentCount))
    end
    ]]
    print(string.format("Number of lanternfish after 80 days: %d", #fishArr))
    return count, {}
end

--[[ Task B:

]]
local function TaskB(inputArray)
    local fishArr = {}
    
    for i = 1, #inputArray do
        table.insert(fishArr, Fish:New(tonumber(inputArray[i])))
    end
    
    for i = 1, 0 do
        local currentCount = #fishArr
        for ii = 1, currentCount do
            if(fishArr[ii]:Reproduce()) then
                table.insert(fishArr, Fish:New(8))
            end
        end
    end
    
    print(string.format("Number of lanternfish after 80 days: %d", #fishArr))
    return #fishArr, {}
end

--[[ Main function:

    * Open the input file and add the content to a list.
    * Solve task A and task B
    * Plot the population growth of lanternfish over time
]]
local function Main(filename, taskPart)
    local hFile = OpenFile(filename)
    if(hFile == nil) then return 0 end

    local inputArray = StringSplit(hFile:read("*all"), ",")
    io.close(hFile)

    local retTaskA = 0 
    local retTaskB = 0
    local plotTaskA = {}
    local plotTaskB = {}
  
    retTaskA, plotTaskA = TaskA(inputArray)
    --retTaskB, plotTaskB = TaskB(inputArray)
    
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
    wnd:save_svg("outputs\\day6.svg", 1500, 1500)
  
    return 0
end

Main(arg[1])