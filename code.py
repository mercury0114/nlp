from bayes import Bayes
from utils import make_vector, display

X = [line.strip() for line in open("train/X_train.txt")]
y = [line.strip() for line in open("train/y_train.txt")]

totalCorrect = 0
for i in range(len(y)):
    v = make_vector(X[i])
    correct = (y[i] == 'spam') if (sum(v) >= 2) else (y[i] == 'ham')
    totalCorrect += correct
    if (not correct):
        display(X[i], y[i], v)

print("Minimum accuracy: ", sum([s == 'ham' for s in y]) / len(y))
print("Best accuracy: ", 0.9742822966507177)
print("Current accuracy: ", totalCorrect / len(y))



bayes = Bayes(4)
bayes.train(X, y)
