import csv
def csv2arr (filename: str):
    out = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if (row != "" and row != None):
                out.append(row)
    # remove blank strings
    while("" in out):
        out.remove("")

    return out