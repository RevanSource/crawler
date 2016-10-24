lines = open('answ.json', 'r').readlines()

lines_set = set(lines)

out  = open('result.json', 'w')
sorted_result = sorted(lines_set)
for line in sorted_result:
    out.write(line)