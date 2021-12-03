local BinaryScale = {}
package.loaded["BinaryScale"] = BinaryScale
BinaryScale.__index = BinaryScale

function BinaryScale:Create()
    self = {}
    self._leftList  = {}
    self._rightList = {}
    self._filter    = 0
    
    setmetatable(self, BinaryScale)
    return self
end

function BinaryScale:SetFilter(filter)
    self._filter = filter
end

function BinaryScale:ShiftFilter(movement)
    if(movement > 0) then
        self._filter = self._filter >> movement
    elseif(movement < 0)
        self._filter = self._filter << (-1 * movement)
    end 
end

function BinaryScale:Insert(data)
    if((data & self._filter) == self._filter) then
        table.insert(self._rightList, data)
    else
        table.insert(self._leftList, data)
    end
end

function BinaryScale:UpdateLists(greaterEq)
    local tmp = {}
    local ref = nil
    if(greaterEq) then
        ref = self._rightList
    else
        ref = self._leftList
    end

    for i = 1, #ref do
        table.insert(tmp, ref[i])
    end

    self._leftList  = nil
    self._rightList = nil

    self._leftList  = {}
    self._rightList = {}

    for i = 1, #tmp do
        self:Insert(tmp[i])
    end
end

function BinaryScale:GetListSize()
    return #self._leftList, #self._rightList
end

function BinaryScale:GetMaxValue()
    if(#self._rightList >= #self._leftList) then
        return self._rightList[1]
    end

    return self._leftList[1]
end

function BinaryScale:GetMinValue()
    if(#self._leftList <= #self._rightList) then
        return self._leftList[1]
    end

    return self._rightList[1]
end

return BinaryScale