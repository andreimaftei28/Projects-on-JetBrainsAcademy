def get_mean(a, b, c):
    return sum((a, b, c)) / 3
mean = get_mean(int(input()), int(input()), int(input()))
print(mean, "Congratulations, you are accepted!", sep="\n")