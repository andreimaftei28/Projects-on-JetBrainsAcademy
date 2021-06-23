import os
import argparse
import hashlib


parser = argparse.ArgumentParser()
parser.add_argument("path", nargs="?", default=None)
args = parser.parse_args()
if args.path is None:
    print("Directory is not specified")
    exit()
try:
    arg = args.path
    size_dict = {}
    dup_list = []
    free_space = 0
    form = input("Enter file format:\n")
    print("Size sorting options:\n1. Descending\n2. Ascending\n")
    sorting_option = input("Enter a sorting option:\n")
    while sorting_option not in "12":
        print("\nWrong option\n")
        sorting_option = input("Enter a sorting option:\n")
    else:
        for root, dirs, files in os.walk(arg, topdown=False):
            for name in files:
                try:
                    path = os.path.join(root, name)
                    size = os.path.getsize(path)
                    size_dict.setdefault(size, []).append(path)
                except OSError as e:
                    print("error")
    keys = list(size_dict.keys())[::-1] if sorting_option == "1" else list(size_dict.keys())
    for key in keys:
        print(f"{key} bytes")
        if form == "":
            try:
                print(*size_dict[key], sep="\n")
            except Exception:
                continue
        else:
            try:
                print(*[x for x in size_dict[key] if x.endswith(form)], sep="\n")
            except Exception:
                continue
    duplicates = input("\nCheck for duplicates?\n")
    while duplicates not in "yesno":
        print("Wrong option")
        duplicates = input("\nCheck for duplicates?\n")
    else:
        if duplicates == "no":
            exit()
    counter = 1
    for key in keys:
        hash_dict = {}
        hash_set = set()
        print(f"{key} bytes")
        for value in size_dict[key]:
            if value.endswith(f"{form}"):
                with open(value, "rb") as file:
                    file_hash = hashlib.md5()
                    file_hash.update(file.read())
                    hash_dict.setdefault(file_hash.hexdigest(), []).append(value)
                for hash_val in hash_dict:
                    if len(hash_dict[hash_val]) > 1 and hash_val not in hash_set:
                        print(f"Hash: {hash_val}")
                        for filepath in hash_dict[hash_val]:
                            print(f"{counter}. {filepath}")
                            dup_list.append([filepath, key])
                            counter += 1
                        hash_set.add(hash_val)
    delete_files = input("\nDelete files?\n")
    while delete_files not in "yesno":
        print("Wrong option")
        delete_files = input("\nDelete files?\n")
    else:
        if delete_files == "no":
            exit()
    files = [x for x in input("Enter file numbers to delete:\n").split()]
    check_digit = (not x.isdigit() for x in files)
    try:
        check_max = max(int(x) for x in files)
    except ValueError:
        print("Wrong option")
    while len(files) < 1 or any(check_digit) or check_max > len(dup_list):
        print("Wrong format")
        files = [x for x in input("Enter file numbers to delete:\n").split()]

    for file in files:
        full_path = dup_list[int(file) - 1][0]
        os.remove(full_path)
        free_space += dup_list[int(file) - 1][1]
    print(f"Total freed up space: {free_space} bytes")

except IndexError:
    print("Directory is not specified")
