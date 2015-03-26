
def get_setting(name):
    with open("settings.txt") as input:
        for line in input:
            line = line.split()
            if len(line) > 1 and line[0] == name:
                setting = line[2].strip()
                if setting in ["yes", "no"]:
                    return setting == "yes"
                elif setting in [str(i) for i in range(10)]:
                    return int(setting)
                else:
                    return setting


def prettify(string):
    return string.replace("_", " ").title()
