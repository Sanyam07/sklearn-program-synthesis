# sklearn-program-synthesis

Machine learning algorithms implemented in Sci-kit learn Estimators for the
purposes of program synthesis (aka automatic programming). Programs are
expressed in the Push language and executed using the Plushi interpreter.


## Search/ML Algorithms

1. Genetic programming
2. Simmulated annealing


## Example Usage

The below Python snippet attempts to evolve the ReLU function, and prints
the best program found throughout evolution and its training MSE.

```py
from sklearn.metrics import mean_squared_error
from sklearn_program_synthesis.estimators import ProgramSynthesizer

X = np.arange(-2, 2, 0.1).reshape(-1, 1)
y = np.array([[x if x > 0 else 0 for x in X]]).flatten()

prog_synth = ProgramSynthesizer(arity=X.shape[1],
                                metric=mean_squared_error,
                                min_or_max="min",
                                types=['exec', 'float'],
                                search_method="evolution",
                                verbose=2)

prog_synth.fit(X, y)
y_hat_train = prog_synth.predict(X)

print(prog_synth._fit_program)
print(mean_squared_error(y, y_hat_train))
```


## Run Benchmarks

To run the benchmark, you will need a Plushi standalone .jar (see next section).

```
pip install -r requirements.pip
java -jar plushi-standalone.jar --start
python run_benchmarks.py [problem name] [search method]
```

| Problem/Dataset   | Type           |
|-------------------|----------------|
| `relu`            | regression     |
| `iris`            | classification |
| `diabetes`        | regression     |

| Search Method       | Argument    |
|---------------------|-------------|
| Genetic Programming | `evoltuion` |
| Simulated annealing | `annealing` |

## Plushi

Plushi is an embeddable, language agnostic Push language interpreter. This repo
requires the use of a standalone .jar file. You can read more about the project
on its GitHub page.

https://github.com/erp12/plushi
