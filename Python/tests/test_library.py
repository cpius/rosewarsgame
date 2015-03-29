import json
from collections import Counter


def run_method(testcase_files, test_method):

    results = {}
    for file in testcase_files:
        test_document = json.loads(open(file).read())
        results[str(test_document["type"])] = Counter()

    for file in testcase_files:
        test_document = json.loads(open(file).read())

        try:
            exception_flag = True
            test = test_method(test_document)
            exception_flag = False
        finally:
            if exception_flag or not test:
                print(file)
                print()

        results[test_document["type"]][test] += 1

    print()
    total = Counter()
    for key, value in results.items():
        print(key + ": " + str(value[True]) + " passed, " + str(value[False]) + " failed")
        total += value
    print()
    print("Total:", str(total[True]) + " passed, " + str(total[False]) + " failed")