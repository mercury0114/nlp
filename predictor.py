import abc
import numpy

HAM = 'ham'
SPAM = 'spam'

class Interface(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def name(self):
        pass

    @abc.abstractmethod
    def predict_one(self, sms):
        pass

    def predict(self, messages):
        return [self.predict_one(sms) for sms in messages]

    def accuracy(self, predicted, labels):
        return (labels == predicted).sum() / len(labels)

    def sensitivity(self, predicted, labels):
        return ((labels == predicted) * (labels == SPAM)).sum() / (labels == SPAM).sum()

    def print_statistics(self, messages, labels_list):
        predicted = numpy.array(self.predict(messages))
        labels = numpy.array(labels_list)
        print(self.name + " statistics")
        print("accuracy: {}".format(self.accuracy(predicted, labels)))
        print("sensitivity: {}".format(self.sensitivity(predicted, labels)))
        print()
