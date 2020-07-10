import decimal
import predictor
import re

_ALL = '_all_'


def _long_number(token):
    try:
        d = decimal.Decimal(token)
        return d > 99 or d < -99 or d.as_tuple().exponent < 0
    except decimal.InvalidOperation:
        return False


def _extract_tokens(original_sms):
    sms = original_sms.lower()
    tokens = re.findall(
        r'[+-]*[\d]*\.*[\d]+|[a-z]+(?:[-\'][a-z]+)+|[a-z]+|[!$£]', sms)
    return ["_start_"] + [
        "_number_" if _long_number(token) else token for token in tokens
    ] + ["_stop_"]


class MonogramsPredictor(predictor.Interface):
    name = "Bayes-monograms-predictor"

    def __init__(self, min_count):
        self.min_count = min_count
        self.counts = {predictor.HAM: {_ALL: 1}, predictor.SPAM: {_ALL: 1}}
        self.total = {predictor.HAM: 0, predictor.SPAM: 0}

    def add_if_absent(self, token):
        if not token in self.counts[predictor.SPAM]:
            self.counts[predictor.SPAM][token] = 0
        if not token in self.counts[predictor.HAM]:
            self.counts[predictor.HAM][token] = 0

    def train(self, messages, labels):
        for sms, label in zip(messages, labels):
            self.total[label] += 1
            for token in _extract_tokens(sms):
                self.add_if_absent(token)
                self.counts[label][token] += 1
                self.counts[label][_ALL] += 1

    def predict_one(self, sms):
        ham_score = self.total[predictor.HAM]
        spam_score = self.total[predictor.SPAM]
        for token in _extract_tokens(sms):
            self.add_if_absent(token)
            if (self.counts[predictor.HAM][token] >= self.min_count
                    or self.counts[predictor.SPAM][token] >= self.min_count):
                ham_score *= (self.counts[predictor.HAM][token] *
                              self.counts[predictor.SPAM][_ALL])
                spam_score *= (self.counts[predictor.SPAM][token] *
                               self.counts[predictor.HAM][_ALL])
        return predictor.HAM if ham_score >= spam_score else predictor.SPAM


# TODO(mariusl): not working well, improve it
class BigramsPredictor(predictor.Interface):
    name = "Bayes-bigrams"

    def __init__(self, init_count):
        self.init_count = init_count
        self.counts = {predictor.HAM: {}, predictor.SPAM: {}}
        self.total_counts = {predictor.HAM: 0, predictor.SPAM: 0}

    def count(self, given_label, given_token, token):
        if not given_token in self.counts[given_label]:
            self.counts[given_label][given_token] = {_ALL: self.init_count}
        if not token in self.counts[given_label][given_token]:
            self.counts[given_label][given_token][token] = 1
        return self.counts[given_label][given_token][token] / self.counts[
            given_label][given_token][_ALL]

    def train(self, messages, labels):
        for sms, label in zip(messages, labels):
            self.total_counts[label] += 1
            tokens = utils.extract_tokens(sms)
            for index in range(len(tokens) - 1):
                self.count(label, tokens[index], tokens[index + 1])
                self.counts[label][tokens[index]][_ALL] += 1
                self.counts[label][tokens[index]][tokens[index + 1]] += 1

    def predict_one(self, sms):
        tokens = extract_tokens(sms)
        ham_prob = self.total_counts[predictor.HAM] / (
            self.total_counts[HAM] + self.total_counts[predictor.SPAM])
        spam_prob = self.total_counts[predictor.SPAM] / (
            self.total_counts[predictor.HAM] +
            self.total_counts[predictor.SPAM])
        for index in range(len(tokens) - 1):
            ham_prob *= self.count('ham', tokens[index], tokens[index + 1])
            spam_prob *= self.count('spam', tokens[index], tokens[index + 1])
        return predictor.HAM if ham_prob >= spam_prob else predictor.SPAM
