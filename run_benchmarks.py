import sys
import numpy as np
from sklearn import datasets, metrics

from sklearn_program_synthesis.estimators import ProgramSynthesizer


benchmark_name = sys.argv[1]
if benchmark_name == 'relu':
    X = np.arange(-10, 10, 0.1).reshape(-1, 1)
    y = np.array([[x if x > 0 else 0 for x in X]]).flatten()
    metric = metrics.mean_squared_error
    min_or_max = 'min'
    push_types = ['exec', 'float']
elif benchmark_name == 'iris':
    X, y = datasets.load_iris(return_X_y=True)
    metric = metrics.accuracy_score
    min_or_max = 'max'
    push_types = ['code', 'exec', 'float', 'integer']
elif benchmark_name == 'diabetes':
    X, y = datasets.load_diabetes(return_X_y=True)
    metric = metrics.mean_squared_error
    min_or_max = 'min'
    push_types = ['code', 'exec', 'float']


prog_synth = ProgramSynthesizer(arity=X.shape[1],
                                metric=metric,
                                min_or_max=min_or_max,
                                types=push_types,
                                verbose=2)
prog_synth.fit(X, y)
y_hat_train = prog_synth.predict(X)

print(y_hat_train)
print()
print(metric(y, y_hat_train))
