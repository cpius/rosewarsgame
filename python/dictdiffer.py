class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict = current_dict
        self.past_dict = past_dict
        self.set_current = set(current_dict.keys())
        self.set_past = set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def differences_recursive(self):
        return self.added() | self.removed() | self.changed_recursive()

    def added(self):
        return self.set_current - self.intersect

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def changed_recursive(self):
        changes = set()
        for o in self.intersect:
            if self.past_dict[o] != self.current_dict[o]:
                if isinstance(self.past_dict[o], dict) and isinstance(self.current_dict[o], dict):
                    inner_diff = DictDiffer(self.current_dict[o], self.past_dict[o])
                    changes |= set(o + "." + inner for inner in inner_diff.differences_recursive())
                elif isinstance(self.past_dict[o], list) and isinstance(self.current_dict[o], list):
                    print "grrr"
                    past_list_as_dict = zip(iter(self.past_dict[o]), self.past_dict[o])
                    current_list_as_dict = zip(iter(self.current_dict[o]), self.current_dict[o])
                    inner_diff = DictDiffer(current_list_as_dict, past_list_as_dict)
                    changes |= set(o + "." + inner for inner in inner_diff.differences_recursive())
                else:
                    changes.add(o + ", " + type(self.past_dict[o]).__name__ + ", " + type(self.current_dict[o]).__name__)

        return changes

    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])
