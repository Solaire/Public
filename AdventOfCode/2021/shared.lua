--[[ StringSplit(str, delimiter)

    * Split the string according to the delimiter.
    * Return array of string tokens.
]]
function StringSplit(str, delimiter)
    local result = {};
    for match in (str..delimiter):gmatch("(.-)"..delimiter) do
        if(match ~= "") then
          table.insert(result, match)
        end
    end
    return result
end

-- Open a file from given filename
-- Return file handle on open, or nil on failure

--[[ OpenFile(filename)

    * Open a file from given filename
    * Return file handle on open, or nil on failure
]]
function OpenFile(filename)
    local hFile = io.open(filename, "r")
    if(hFile == nil) then
        print(string.format("Could not open file: %s",filename))
    end
    return hFile
end