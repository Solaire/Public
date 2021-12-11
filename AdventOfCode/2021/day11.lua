require "shared"

OctopusMap = {cols = {}, flash = 0, stepFlash = 0}
OctopusMap.__index = OctopusMap

function OctopusMap:New()
	self = {}
	self.cols = {}
	self.flash = 0
	self.stepFlash = 0
	setmetatable(self, OctopusMap)
	return self
end

function OctopusMap:GetCount()
	return #self.cols * #self.cols[1]
end

function OctopusMap:GetStepFlash()
	return self.stepFlash
end

function OctopusMap:AddPoint(x, y, val)
	if(self.cols[x] == nil) then
		self.cols[x] = {}
	end
	self.cols[x][y] = val
end

function OctopusMap:IncrementEnergy(x, y)
	if(self.cols[x] == nil or self.cols[x][y] == nil or self.cols[x][y] == 0) then
		return false
	end
	if(self.cols[x][y] >= 9) then
		self.cols[x][y] = 0
		self.flash = self.flash + 1
		self.stepFlash = self.stepFlash + 1
		return true
	end
	self.cols[x][y] = self.cols[x][y] + 1
	return false
end

function OctopusMap:IncrementAdjecent(x, y)
	if(self:IncrementEnergy(x - 1, y - 1)) 	then self:IncrementAdjecent(x - 1, y - 1) end
	if(self:IncrementEnergy(x, y - 1)) 		then self:IncrementAdjecent(x, y - 1) 	 end
	if(self:IncrementEnergy(x + 1, y - 1)) 	then self:IncrementAdjecent(x + 1, y - 1) end
	if(self:IncrementEnergy(x - 1, y)) 		then self:IncrementAdjecent(x - 1, y) 	 end
	if(self:IncrementEnergy(x + 1, y)) 		then self:IncrementAdjecent(x + 1, y) 	 end
	if(self:IncrementEnergy(x - 1, y + 1)) 	then self:IncrementAdjecent(x - 1, y + 1) end
	if(self:IncrementEnergy(x, y + 1)) 		then self:IncrementAdjecent(x, y + 1) 	 end
	if(self:IncrementEnergy(x + 1, y + 1)) 	then self:IncrementAdjecent(x + 1, y + 1) end
end

function OctopusMap:Step()
	for x = 1, #self.cols do
		for y = 1, #self.cols[x] do
			self.cols[x][y] = self.cols[x][y] + 1
		end
	end
	
	self.stepFlash = 0
	for x = 1, #self.cols do
		for y = 1, #self.cols[x] do
			if(self.cols[x][y] > 9) then
				self.cols[x][y] = 0
				self.flash = self.flash + 1
				self.stepFlash = self.stepFlash + 1
				self:IncrementAdjecent(x, y)
			end
		end
	end
	return self.flash
end

--[[ Task A:

]]
local function TaskA(omap)
	local ret = 0
	for i = 1, 100 do
		ret = ret + omap:Step()
	end
	print(ret)
	return ret
end

--[[ Task B:

]]
local function TaskB(omap)
	local ret = 0
	local octopusCount = omap:GetCount()
	local i = 0
	repeat
		i = i + 1
		omap:Step()
	until (omap:GetStepFlash() == octopusCount)
	print(i)
	return i
end

--[[ Main function:

    * Open the input file and add the content to a list.
    * Solve task A and task B
    * Plot the population growth of lanternfish over time
]]
local function Main(filename, taskPart)
    local hFile = OpenFile(filename)
    if(hFile == nil) then return 0 end

    local omap = OctopusMap:New()
    local inputLine = hFile:read("*line")
    local rowLen = #inputLine
    
    local y = 1
    while inputLine do
        local x = 1
        inputLine:gsub(".", function(char)
            omap:AddPoint(x, y, tonumber(char))
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
  
    --retTaskA, plotTaskA = TaskA(omap)
    retTaskB, plotTaskB = TaskB(omap)
  
    return 0
end

Main(arg[1])