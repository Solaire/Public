require "shared"

--[[ Task A:

]]
local function TaskA(inputArray)
    local input = {}
    
    for i = 1, #inputArray do
      table.insert(input, tonumber(inputArray[i]))
    end
    
    table.sort(input)
    
    local modal = 0
    local half = #input // 2
    if(#input % 2 ~= 0) then
      modal = input[half]
    else
      modal = (input[half] + input[half + 1]) // 2
    end
    
    local ret = 0
    for i = 1, #input do
      ret = ret + math.abs(input[i] - modal)
    end
    
    print(string.format("Optimal position: %d, total cost %d", modal, ret))
    return ret, {}
end

--[[ Task B:

]]
local function TaskB(inputArray)
    local input = {}
    local total = 0
    
    for i = 1, #inputArray do
      table.insert(input, tonumber(inputArray[i]))
      total = total + tonumber(inputArray[i])
    end
    
    -- Since the number of movements must be a full number, check both floor and ceil values and pick the smallest one
    mean = {min = math.floor(total / #input), max = math.floor((total / #input) + 0.5)}
    
    local ret = {a = 0, b = 0}
    for i = 1, #input do
      local diff_mn = math.abs(input[i] - mean.min)
      local diff_mx = math.abs(input[i] - mean.max)
      ret.a = ret.a + (diff_mn * (diff_mn + 1) / 2)
      ret.b = ret.b + (diff_mx * (diff_mx + 1) / 2)
    end
    
    print(string.format("total cost %d", math.min(ret.a, ret.b)))
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

    local inputArray = StringSplit(hFile:read("*all"), ",")
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