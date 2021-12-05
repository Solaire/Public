require "shared"

Grid = {cols = {}}
Grid.__index = Grid

function Grid:New()
  self = {}
  self.cols = {}
  
  setmetatable(self, Grid)
  return self
end

function Grid:AddVector(x1, y1, x2, y2, incDiagonal)
    if(x1 ~= x2 and y1 ~= y2) then
      if(math.abs(x1 - x2) ~= math.abs(y1 - y2)) then
        return
      elseif(incDiagonal) then
          local x = x1
          local y = y1
          
          repeat
            if(self.cols[x] == nil) then
              self.cols[x] = {}
            end
              
            if(self.cols[x][y] == nil) then
              self.cols[x][y] = 1
            else
              self.cols[x][y] = self.cols[x][y] + 1
            end
            
            if(x > x2) then
              x = x - 1
            elseif(x < x2) then
              x = x + 1
            end
            
            if(y > y2) then
              y = y - 1
            elseif(y < y2) then
              y = y + 1
            end
          until(x == x2 and y == y2)
          if(self.cols[x] == nil) then
            self.cols[x] = {}
          end
              
          if(self.cols[x2][y2] == nil) then
              self.cols[x2][y2] = 1
          else
              self.cols[x2][y2] = self.cols[x2][y2] + 1
          end
          
          return
      else
        return
      end
    end
  
    if(x1 ~= x2) then
        local mn = math.min(x1, x2)
        local mx = math.max(x1, x2)
        for x = mn, mx do
            if(self.cols[x] == nil) then
                self.cols[x] = {}
            end
    
            if(self.cols[x][y1] == nil) then
                self.cols[x][y1] = 1
            else
                self.cols[x][y1] = self.cols[x][y1] + 1
            end
        end
    else
        if(self.cols[x1] == nil) then
            self.cols[x1] = {}
        end
        
        local mn = math.min(y1, y2)
        local mx = math.max(y1, y2)
        for y = mn, mx do            
            if(self.cols[x1][y] == nil) then
                self.cols[x1][y] = 1
            else
                self.cols[x1][y] = self.cols[x1][y] + 1
            end
        end
    end
end


function Grid:GetOverlappingPoints()
  local count = 0
  for k1, v1 in pairs(self.cols) do
    for k2, val in pairs(v1) do
      if(val > 1) then
        count = count + 1
      end
    end
  end
  return count
end

--[[ Task A:

]]
local function TaskA(hFile)
    local grid = Grid:New()
    
    local inputLine = hFile:read("*line")
    while inputLine do
        local points = StringSplit(inputLine, "->")
        local x1y1 = StringSplit(points[1], ",")
        local x2y2 = StringSplit(points[2], ",")
        
        grid:AddVector(x1y1[1] + 1, x1y1[2] + 1, x2y2[1] + 1, x2y2[2] + 1, false)
        
        inputLine = hFile:read("*line")
    end
    
    local overlapping = grid:GetOverlappingPoints()
    print(string.format("Number of overlapping points: %d", overlapping))
    return overlapping
end

--[[ Task B:

]]
local function TaskB(hFile)
    local grid = Grid:New()
    
    local inputLine = hFile:read("*line")
    while inputLine do
        local points = StringSplit(inputLine, "->")
        local x1y1 = StringSplit(points[1], ",")
        local x2y2 = StringSplit(points[2], ",")
        
        grid:AddVector(x1y1[1] + 1, x1y1[2] + 1, x2y2[1] + 1, x2y2[2] + 1, true)
        
        inputLine = hFile:read("*line")
    end
    
    local overlapping = grid:GetOverlappingPoints()
    print(string.format("Number of overlapping points: %d", overlapping))
    return overlapping
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