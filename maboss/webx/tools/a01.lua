
--[[
print("Hello World")

print("ok")

sum = 0

num = 1

while num <= 3 do
    sum = sum + num
    num = num + 1
end

print("sum =",sum)

age = 40

sex = "Male"

if age == 40 and sex =="Male" then
    print("男人四十一枝花")
elseif age > 60 and sex ~="Female" then
    print("old man without country!")
elseif age < 20 then
    io.write("too young, too naive!\n")
else
    --local age = io.read()
    print("Your age is "..age)
end

print('1'..'2')

]]

cc = [[.

abc

.]]

print(cc)

function newCounter()
    local i = 0
    return function()     -- anonymous function
       i = i + 2
        return i
    end
end
 
c1 = newCounter()
print(c1())  --> 1
print(c1())  --> 2