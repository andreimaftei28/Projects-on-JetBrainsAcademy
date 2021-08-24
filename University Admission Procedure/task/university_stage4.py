departments = {'Biotech': [], 'Chemistry': [], 'Engineering': [], 'Mathematics': [], 'Physics': []}

max_accepted = int(input())
with open('applicants.txt') as f:
    applicants = [line.split() for line in f]
for i in range(3, 6):  # priority fields in input file
    for dep in departments.keys():
        sort_key = lambda x: (-float(x[2]), x[0], x[1])
        for applicant in sorted(applicants, key=sort_key):
            if applicant[i] == dep and len(departments[dep]) < max_accepted:
                score = float(applicant[2])
                departments[dep].append([applicant[0], applicant[1], score])
                applicants.remove(applicant)

for dep in departments.keys():
    print(dep)
    for student in sorted(departments[dep], key=lambda x: (-x[2], x[0], x[1])):
        print(*student)
