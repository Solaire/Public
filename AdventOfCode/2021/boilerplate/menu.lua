local MenuElement = {}
MenuElement.__index = MenuElement

function MenuElement:New(index, rect, isActive, colour)
	self = {}
	self.m_index = index
	self.m_rect = rect
	self.m_isActive = isActive
	self.m_colour = colour -- [1]: active, [2]: inactive
	
	setmetatable(self, MenuElement)
	return self
end

function MenuElement:SetActive(isActive)
	self.m_isActive = isActive
end

function MenuElement:Draw()
	if(self.m_isActive) then
		love.graphics.setColor(255, 0, 0, 128)
	else
		love.graphics.setColor(128, 128, 128, 128)
	end
	love.graphics.rectangle("line", self.m_rect.x, self.m_rect.y, self.m_rect.w, self.m_rect.h)
	love.graphics.setColor(255, 255, 255, 255)
	
	local str = string.format("Day %d", self.m_index)
	local off = #str / 2
	love.graphics.print(str, (self.m_rect.x - off) + (self.m_rect.w / 2), self.m_rect.y + (self.m_rect.h / 2))
	return
end

local Menu = {}
package.loaded["Menu"] = Menu
Menu.__index = Menu

function Menu:New(rect, elements)
	self = {}
	self.m_rect = rect
	self.m_elements = elements
	self.m_currentSelection = -1
	
	setmetatable(self, Menu)
	return self
end

function Menu:Draw()
	for i = 1, #self.m_elements do
		self.m_elements[i]:Draw()
	end
	return
end

function Menu:NewElement(title, rect, isActive, colour)
	return MenuElement:New(title, rect, isActive, colour)
end

return Menu