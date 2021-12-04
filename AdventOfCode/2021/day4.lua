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
  self.rows = {}
  self.columns = {}
  
  setmetatable(self, BingoGrid)
  return self
end

function BingoGrid:AddRow(strRow)
  local tokens = StringSplit(strRow, " ")
  self.pointTable[#self.pointTable + 1] = {}
  self.rows[#self.pointTable] = 0
  
  for i = 1, #tokens do
    self.totalVal = self.totalVal + tonumber(tokens[i])
    local point = BingoPoint:New(tonumber(tokens[i]))
    self.pointTable[#self.pointTable][i] = point
    self.columns[i] = 0
  end
end

function BingoGrid:Mark(value)
  for i = 1, #self.pointTable do
      for ii = 1, #self.pointTable[i] do
          if(self.pointTable[i][ii].value == value) then
              self.pointTable[i][ii]:Mark()
              self.totalVal = self.totalVal - value
              self.rows[i] = self.rows[i] + 1
              self.columns[ii] = self.columns[ii] + 1
          end
      end
  end
end

function BingoGrid:IsWinner()
    for i = 1, #self.rows do
        if(self.rows[i] == 5) then
            return true
        end
    end
    
    for i = 1, #self.columns do
        if(self.columns[i] == 5) then
            return true
        end
    end
    
    return false
end

function BingoGrid:GetUnmarkedSum()
    return self.totalVal
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
    
    -- Create grid objects
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
    
    local winningBoard = 0
    local unmarkedSum  = 0
    local lastInput    = 0
    
    for i = 1, #randSequence do
        for ii = 1, #grids do
            grids[ii]:Mark(tonumber(randSequence[i]))
            if(grids[ii]:IsWinner()) then
                winningBoard = ii
                unmarkedSum = grids[ii]:GetUnmarkedSum()
                lastInput = i
                break
            end
        end
        if(unmarkedSum ~= 0) then
          break
        end
    end

    print(string.format("Winning board: %d", winningBoard))
    print(string.format("Last input: %d", randSequence[lastInput]))
    print(string.format("Bingo score: %d", unmarkedSum * randSequence[lastInput]))
    
    return winningBoard * randSequence[lastInput]
end

--[[ Task B:

]]
local function TaskB(hFile)
    -- Get Input. First line is random sequence
    local inputLine = hFile:read("*line")
    local randSequence = StringSplit(inputLine, ",")
    local grids = {}
    local i = 1
    
    -- Create grid objects
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
    
    local winningBoard = 0
    local unmarkedSum  = 0
    local lastInput    = 0
    
    for i = 1, #randSequence do
        --for ii = 1, #grids do
          for ii = #grids, 1, -1 do
            grids[ii]:Mark(tonumber(randSequence[i]))
            if(grids[ii]:IsWinner()) then
                if(#grids == 1) then
                    winningBoard = ii
                    unmarkedSum = grids[ii]:GetUnmarkedSum()
                    lastInput = i
                    break
                else
                    table.remove(grids, ii)
                end
            end
        end
        if(unmarkedSum ~= 0) then
          break
        end
    end

    print(string.format("Winning board: %d", winningBoard))
    print(string.format("Last input: %d", randSequence[lastInput]))
    print(string.format("Bingo score: %d", unmarkedSum * randSequence[lastInput]))
    
    return winningBoard * randSequence[lastInput]
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