import basic_predictors
import bayes_predictors

X = [line.strip() for line in open("train/X_train.txt")]
y = [line.strip() for line in open("train/y_train.txt")]

basic_predictors.AlwaysHamPredictor().print_accuracy(X, y)
basic_predictors.SimplePredictor().print_accuracy(X, y)

# 46 is the best found hyperparameter
bayes = bayes_predictors.MonogramsPredictor(46)
to = 4000
bayes.train(X[:to], y[:to])
bayes.print_accuracy(X[to:], y[to:])

