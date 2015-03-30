from json import JSONEncoder, dumps, loads
from datetime import datetime
from enum import Enum
from tests.dictdiffer import DictDiffer


def prettify(string):
    return string.replace("_", " ").title()


opponent_descriptions = {
    "HotSeat": "Start a new hot seat game on this machine",
    "AI": "Start a new game against an AI",
    "Load": "Load the most recent game",
    "Internet": "Start a new game against an opponent from the internet"
}

ai_descriptions = {
    "1": "Easy",
    "2": "Medium",
    "3": "Hard"
}


def merge(first_dictionary, second_dictionary, third_dictionary=None, fourth_dictionary=None):
    merged_dictionary = first_dictionary.copy()
    merged_dictionary.update(second_dictionary)

    if third_dictionary:
        merged_dictionary.update(third_dictionary)

    if fourth_dictionary:
        merged_dictionary.update(fourth_dictionary)

    return merged_dictionary


def assert_equal_documents(testcase, expected, actual, testcase_file):
    message = "Wrong document for " + testcase_file + "\n\n"

    message += "Expected:\n" + document_to_string(expected)
    message += "\nActual:\n" + document_to_string(actual) + "\n"

    difference = DictDiffer(actual, expected)
    if difference.added():
        message += "Added " + str(difference.added())
    if difference.removed():
        message += "Removed " + str(difference.removed())
    if difference.changed_recursive():
        message += "Changed " + str(difference.changed_recursive())

    if actual == expected:
        return True, "Everything is swell"
    else:
        return False, message


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
        if isinstance(obj, Enum):
            return obj.name
        return JSONEncoder.default(self, obj)


def document_to_string(document):
    return dumps(document, indent=4, cls=CustomJsonEncoder, sort_keys=False)


def convert_quoted_integers_to_integers(document):
    if type(document) is str:
        return document
    else:
        new_document = {}
        for key, value in document.items():
            try:
                key = int(key)
            except Exception:
                pass
            new_document[key] = convert_quoted_integers_to_integers(value)
        return new_document


def read_json(json_file):
    return loads(open(json_file).read())
