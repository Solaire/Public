require "shared"

Heightmap = {cols = {}}
Heightmap.__index = Heightmap

function Heightmap:New()
  self = {}
  self.cols = {}
  
  setmetatable(self, Heightmap)
  return self
end

function Heightmap:AddPoint(x, y, val)
    if(self.cols[x] == nil) then
        self.cols[x] = {}
    end
    self.cols[x][y] = val
end

function Heightmap:CountLowPoints()
    local count = 0
    local basinPoints = {}
    
    for x = 1, #self.cols do
        for y = 1, #self.cols[x] do
            local it = self.cols[x][y]
            local u = 10
            local d = 10
            local l = 10
            local r = 10
            
            if self.cols[x][y - 1] ~= nil then u = self.cols[x][y - 1] end
            if self.cols[x][y + 1] ~= nil then d = self.cols[x][y + 1] end
            if self.cols[x - 1]    ~= nil then l = self.cols[x - 1][y] end
            if self.cols[x + 1]    ~= nil then r = self.cols[x + 1][y] end
            
            if(it < u and it < d and it < l and it < r) then
                count = count + (it + 1)
                table.insert(basinPoints, {x, y})
            end
        end
    end
    return count, basinPoints
end

function Heightmap:IsValidBasinPoint(x, y, val)
    if(self.cols[x] == nil) then return false end
    if(self.cols[x][y] == nil or self.cols[x][y] == 9) then return false end
    if(self.cols[x][y] <= val) then return false end
    return true
end

local function SetContains(set, item)
    for i, val in ipairs(set) do
        if(val[1] == item[1] and val[2] == item[2]) then 
            return true 
        end
    end
    return false
end

function Heightmap:GetLowestBasins(basinPoints)
    local count = {}
    
    for i = 1, #basinPoints do
        local points = {}
        local x = basinPoints[i][1]
        local y = basinPoints[i][2]
        
        table.insert(points, {x, y})
        count[i] = 1  
                
        while(#points > 0) do
            x = points[1][1]
            y = points[1][2]
            local it = self.cols[x][y]
            
            if(self:IsValidBasinPoint(x, y - 1, it) and not SetContains(points, {x, y - 1})) then 
                table.insert(points, {x, y - 1})
                count[i] = count[i] + 1 
            end
            if(self:IsValidBasinPoint(x, y + 1, it) and not SetContains(points, {x, y + 1})) then 
                table.insert(points, {x, y + 1})
                count[i] = count[i] + 1 
            end
            if(self:IsValidBasinPoint(x - 1, y, it) and not SetContains(points, {x - 1, y})) then 
                table.insert(points, {x - 1, y})
                count[i] = count[i] + 1 
            end
            if(self:IsValidBasinPoint(x + 1, y, it) and not SetContains(points, {x + 1, y})) then 
                table.insert(points, {x + 1, y})
                count[i] = count[i] + 1 
            end
            self.cols[x][y] = 9
            table.remove(points, 1)
        end
    end

    table.sort(count)
    local ret = count[#count] * count[#count - 1] * count[#count - 2]
    return ret, {}
end

--[[ Task A:

]]
local function TaskA(hmap)
    return hmap:CountLowPoints()
end

--[[ Task B:

]]
local function TaskB(hmap, basinPoints)
    local ret = hmap:GetLowestBasins(basinPoints)
    
    return ret, {}
end

--[[ Main function:

    * Open the input file and add the content to a list.
    * Solve task A and task B
    * Plot the population growth of lanternfish over time
]]
local function Main(filename, taskPart)
    local hFile = OpenFile(filename)
    if(hFile == nil) then return 0 end

    local hmap = Heightmap:New()
    local inputLine = hFile:read("*line")
    local rowLen = #inputLine
    
    local y = 1
    while inputLine do
        local x = 1
        inputLine:gsub(".", function(char)
            hmap:AddPoint(x, y, tonumber(char))
            x = x + 1
        end)
        inputLine = hFile:read("*line")
        y = y + 1
    end
    io.close(hFile)

    local retTaskA = 0 
    local retTaskB = 0
    local plotTaskA = {}
    local plotTaskB = {}
  
    retTaskA, plotTaskA = TaskA(hmap)
    retTaskB, plotTaskB = TaskB(hmap, plotTaskA)
    
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