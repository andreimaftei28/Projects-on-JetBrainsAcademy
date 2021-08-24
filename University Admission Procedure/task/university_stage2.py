def get_mean(a, b, c):
    return sum((a, b, c)) / 3
def acceptance(grade):
    if grade >= 60:
        return f"{grade}\nCongratulations, you are accepted!"
    return f"{grade}\nWe regret to inform you that we will not be able to offer you admission."
mean = get_mean(int(input()), int(input()), int(input()))
print(acceptance(mean)
