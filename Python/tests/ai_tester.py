import ai
import json


def run():
    file = "./tests/ai_tests/test1.json"

    test_document = json.loads(open(file).read())
