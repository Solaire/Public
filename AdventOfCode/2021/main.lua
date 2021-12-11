Rect = require "boilerplate.Rectangle"
Menu = require "boilerplate.Menu"
require "boilerplate.AoC"

local data = nil
local menu = nil

WINDOW_X = 750
WINDOW_Y = 750

function love.load(arg)
	if arg[#arg] == "-debug" then require("mobdebug").start() end
		
	love.window.setMode(WINDOW_X, WINDOW_Y)
	data = GenerateCalendar(WINDOW_X, WINDOW_Y)
	menu = Menu:New(Rect:New(0, 0, WINDOW_X, WINDOW_Y), data)
end

function love.update(dt)
	return
end

function love.draw()
	
	menu:Draw()
end
