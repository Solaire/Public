local Rect = {}
package.loaded["Rect"] = Rect
Rect.__index = Rect

function Rect:New(x, y, w, h)
	self = {}
	self.x = x
	self.y = y
	self.w = w
	self.h = h
	
	setmetatable(self, Rect)
	return self
end

function Rect:IsOverlapping(other)
	if(other == nil) then
		return false
	end
	local x = ( (other.x > self.x and other.x < self.x + self.w) and (self.x > other.x and self.x < other.x + other.w) )
	local y = ( (other.y > self.y and other.y < self.y + self.h) and (self.y > other.y and self.y < other.y + other.h) )
	return (x and y)
end
	
return Rect