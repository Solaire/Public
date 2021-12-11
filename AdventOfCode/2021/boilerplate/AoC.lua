require "shared"
local Menu = require "boilerplate.Menu"
local Rect = require "boilerplate.Rectangle"

--[[ 
	Generate AoC calendar. An entry for each day is created
	but only days with existing solutions are activated
	
	Calendar is 25 days. Create menu as 5x5 grid
	
	w = available width
	h = available height
]]
function GenerateCalendar(w, h)
	-- Assume square
	local PADDING = math.floor(w / 100)
	local rwh = w / 5
		
	local DAILY_SOLUTION = "C:\\dev\\public\\AdventOfCode\\2021\\day%d.lua" -- %d will be replaced with a number
	local elements = {}
	
	local i = 1
	local ry = PADDING
	for x = 1, 5 do
		local rx = PADDING
		for y = 1, 5 do
			local active = FileExists(string.format(DAILY_SOLUTION, i))
			local rect = Rect:New(rx, ry, rwh - (PADDING * 2), rwh - (PADDING * 2))
			local rgb = {{255, 0, 0}, {128, 128, 128}}
			
			table.insert(elements, Menu:NewElement(i, rect, active, rgb))
			i = i + 1
			rx = rx + rwh
		end
		ry = ry + rwh
	end
	return elements
end
