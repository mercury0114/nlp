from utils import ExtractTokens

ALL = '_all_'
HAM = 'ham'
SPAM = 'spam'

class Bayes:
    init_count = 1
    counts = {HAM: {}, SPAM : {}}
    total_counts = {HAM : 0, SPAM : 0}

    def __init__(self, init_count):
        self.init_count = init_count

    def Count(self, token, given_token, given_label):
        if not given_token in self.counts[given_label]:
            self.counts[given_label][given_token] = {ALL : self.init_count}
        if not token in self.counts[given_label][given_token]:
            self.counts[given_label][given_token][token] = 1
        return self.counts[given_label][given_token][token] / self.counts[given_label][given_token][ALL]


    def Train(self, messages, labels):
        for sms, label in zip(messages, labels):
            tokens = ExtractTokens(sms)
            for t in range(len(tokens)-1):
                self.Count(tokens[t+1], tokens[t], label)
                self.counts[label][tokens[t]][tokens[t+1]] += 1
