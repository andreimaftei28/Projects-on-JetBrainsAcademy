n = int(input())
m = int(input())
aplicants = [input() for _ in range(n)]
results = []
for member in aplicants:
    aplicant = member.split()
    name = " ".join((aplicant[0], aplicant[1]))
    gpa = float(aplicant[-1])
    results.append([name, gpa])
results = sorted(results, key=lambda x: (-x[1], x[0]))
print("Successful applicants:")
for i in range(m):
    print(results[i][0]
