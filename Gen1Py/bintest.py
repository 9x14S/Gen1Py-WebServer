data = bytearray(5)
for i in range(0, 4):
    data[i] = 0x82
    
temp = 0
for j in range(0, 5):
    temp += data[i]
    print(hex(temp % 256))

print(hex((0xff + 0xf5)% 255))
print(~(~(0xff + 0xf5)))