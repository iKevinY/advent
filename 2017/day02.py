import fileinput

checksum = 0
result = 0

for line in fileinput.input():
    nums = sorted((int(x) for x in line.split()), reverse=True)

    checksum += nums[0] - nums[-1]

    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] % nums[j] == 0:
                result += nums[i] // nums[j]

print "Spreadsheet checksum:", checksum
print "Spreadsheet result:", result
