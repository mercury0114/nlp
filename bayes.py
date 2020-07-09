from utils import extract_tokens

ALL = '_all_'
HAM = 'ham'
SPAM = 'spam'

class Bayes(object):
    init_count = 1
    counts = {HAM: {}, SPAM: {}}
    total_counts = {HAM: 0, SPAM: 0}

    def __init__(self, init_count):
        self.init_count = init_count

    def count(self, token, given_token, given_label):
        if not given_token in self.counts[given_label]:
            self.counts[given_label][given_token] = {ALL: self.init_count}
        if not token in self.counts[given_label][given_token]:
            self.counts[given_label][given_token][token] = 1
        return self.counts[given_label][given_token][token] / self.counts[
            given_label][given_token][ALL]

    def train(self, messages, labels):
        for sms, label in zip(messages, labels):
            tokens = extract_tokens(sms)
            for index in range(len(tokens) - 1):
                self.count(tokens[index + 1], tokens[index], label)
                self.counts[label][tokens[index]][tokens[index + 1]] += 1
