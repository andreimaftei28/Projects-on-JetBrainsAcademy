formatters = "plain bold italic header link inline-code ordered-list unordered-list new-line".split()
commands = "!help !done".split()


def text_style(formater, text):
    if formater == "bold":
        return f"**{text}**"
    elif formater == "italic":
        return f"*{text}*"
    elif formater == "plain":
        return f"{text}"
    else:
        return f"`{text}`"


def header(level, text):
    return f"{'#' * level} {text}\n"


def link(label, url):
    return f"[{label}]({url})"

def list(format, row_number, line):

    if format == "unordered-list":
            return f"* {line}\n"
    else:
        return f"{row_number}. {line}\n"


display = ""
while True:
    command = input("- Choose a formatter: ")
    if command == "!done":
        with open("output.md", "w") as file:
            file.write(display)
        break
    elif command == "!help":
        print(f"Available formatters: {' '.join(formatters)}\nSpecial commands: !help !done")
    elif command not in formatters:
        print("Unknown formatting type or command. Please try again")

    else:
        if command == "new-line":
            display += "\n"

        if command in "plain bold italic inline-code":
            text = input("- Text: ")
            display += text_style(command, text)
        elif command == "header":
            level = int(input("- Level: "))
            text = input("- Text")
            display += header(level, text)
        elif command == "link":
            label = input("- Label: ")
            url = input("- URL: ")
            display += link(label, url)
        elif command in "unordered-list ordered-list":
            while True:
                length = int(input("- Number of rows: "))
                if length <= 0:
                    print("The number of rows should be greater than zero")
                else:
                    break

            if length > 0:
                for i in range(1, length + 1):
                    line = input(f"- Row #{i}")
                    display += list(command, i, line)

    print(display)
