
class SetOperationsHandler():
    def __init__(self):
        pass
    def perform_set_operations(self, verb, other_verbs, op, verb_dict):

        verb_set = set(verb_dict.get(verb, []))

        for other_verb in other_verbs:

            other_verb_set = set(verb_dict.get(other_verb, []))
            if op == 'sum':
                verb_set = verb_set.union(other_verb_set)
            elif op == 'intersection':
                verb_set = verb_set.intersection(other_verb_set)
            elif op == 'difference':
                verb_set = verb_set.difference(other_verb_set)

        return verb_set