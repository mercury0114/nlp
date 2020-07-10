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

    def get_accuracy(self, messages, labels):
        predicted = numpy.array(self.predict(messages))
        return (numpy.array(labels) == predicted).sum() / len(labels)

    def print_accuracy(self, messages, labels):
        predicted = numpy.array(self.predict(messages))
        print("{} accuracy: {}".format(self.name, self.get_accuracy(messages, labels)))
