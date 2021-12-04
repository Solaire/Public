require "shared"

BingoPoint = {value = 0, marked = false}
BingoPoint.__index = BingoPoint

function BingoPoint:New(value)
  self = {}
  self.value = value
  self.marked = false
  
  setmetatable(self, BingoPoint)
  return self
end

function BingoPoint:Mark()
  self.marked = true
end

BingoGrid = {totalVal = 0, pointTable = {}}
BingoGrid.__index = BingoGrid

function BingoGrid:New()
  self = {}
  self.totalVal = 0
  self.pointTable = {}
  
  setmetatable(self, BingoGrid)
  return self
end

function BingoGrid:AddRow(strRow)
  local tokens = StringSplit(strRow, " ")
  self.pointTable[#self.pointTable + 1] = {}
  
  for i = 1, #tokens do
    self.totalVal = self.totalVal + tonumber(tokens[i])
    local point = BingoPoint:New(tonumber(tokens[i]))
    self.pointTable[#self.pointTable][i] = point
  end
end

--[[ Task A:
  
  * Input contains a list of random numbers and a set of bingo boards.
  * Calculate the final score by taking a sum of all unmarked numbers 
   in the winning board, and multiply that sum by the last number called.
]]
local function FindWinningBingoBoard(hFile)
    -- Get Input. First line is random sequence
    local inputLine = hFile:read("*line")
    local randSequence = StringSplit(inputLine, ",")
    local grids = {}
    local i = 1
    
    inputLine = hFile:read("*line")
    while inputLine do
        if(inputLine == "") then
          local grid = BingoGrid:New()
          grids[#grids + 1] = grid
        else
          grids[#grids]:AddRow(inputLine)
        end
        inputLine = hFile:read("*line")
    end
    
    local x = 0
    local y = 0
    print(string.format("Winning board: %d", x))
    print(string.format("Bingo score: %d", x * y))
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
        ret = FindWinningBingoBoard(hFile)
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