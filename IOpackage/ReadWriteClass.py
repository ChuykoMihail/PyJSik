
def read(path=""):
    if path == "":
        with open('input.txt', 'r') as f:
            inputCode = f.read()
    else:
        with open(path, 'r') as f:
            inputCode = f.read()
    inputCode = inputCode.replace("\n", " ")
    inputCode = inputCode.replace("    ", " ")
    inputCode = inputCode.replace(" ", "")
    return inputCode


def write(outputCode, path=""):
    if path == "":
        with open('output.txt', 'w') as f:
            f.write(outputCode)
    else:
        with open(path, 'w') as f:
            f.write(outputCode)
