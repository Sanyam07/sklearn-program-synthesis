import numpy as np
import random

from .plushi import type_to_plushi_type, run_on_dataset


class Evolver:

    def __init__(self, n_steps, population_size, mutation, penalty=1e3, verbose=0):
        self.n_steps = n_steps
        self.population_size = population_size
        self.mutation = mutation
        self.penalty = penalty
        self.verbose = verbose

        self.population = None
        self.best = None
        self.best_error = None

    def _init_population(self):
        return [self.mutation.push_spawner.random_program() for _ in range(self.population_size)]

    def _evaluate_program(self, program, X, y, metric, min_or_max):
        output_types = [type_to_plushi_type(y.dtype)]
        y_hat = run_on_dataset(program, output_types, X).flatten()

        error = 0
        error_vector = []
        valid_y_hat = []
        valid_y = []
        for i in range(len(y_hat)):
            if y_hat[i] == 'NO-STACK-ITEM':
                p = -self.penalty if min_or_max is 'max' else self.penalty
                error += p
                error_vector.append(p)
            else:
                valid_y_hat.append(float(y_hat[i]))
                valid_y.append(float(y[i]))
                err = abs(float(y_hat[i]) - float(y[i]))
                error_vector.append(-err if min_or_max is 'max' else err)

        if len(valid_y) > 0:
            error += metric(valid_y, valid_y_hat)

        if self.best is None or (min_or_max == 'max' and error > self.best_error):
            self.best = program
            self.best_error = error
        elif self.best is None or (min_or_max == 'min' and error < self.best_error):
            self.best = program
            self.best_error = error
        elif self.best_error == error and len(program) < len(self.best):
            # Favor smaller programs for better generalization
            self.best = program
            self.best_error = error

        return (error, np.array(error_vector))

    def _evaluate_population(self, X, y, metric, min_or_max):
        self._errors = []
        self._error_vectors = []
        for program in self.population:
            error, error_vector = self._evaluate_program(program, X, y, metric, min_or_max)
            self._errors.append(error)
            self._error_vectors.append(error_vector)
        self._errors = np.array(self._errors)
        self._error_vectors = np.array(self._error_vectors)

    def _select_parent(self, min_or_max):
        """For now, only the epsilon lexicase selection algorithm is implemented.
        """
        mad = np.vectorize(lambda a: np.median(np.abs(a - np.median(a))))
        epsilon = np.apply_along_axis(mad, 0, self._errors)

        candidates = self.population[:]
        error_vectors = np.copy(self._error_vectors)
        cases = list(range(error_vectors.shape[1]))
        random.shuffle(cases)

        while len(cases) > 0 and len(candidates) > 1:
            case = cases[0]
            errors_this_case = error_vectors[:, case]
            best_val_for_case = np.max(errors_this_case) if min_or_max == 'max' else np.min(errors_this_case)
            max_passing_error = best_val_for_case + epsilon[case]
            mask = [error_vectors[i, case] <= max_passing_error for i in range(error_vectors.shape[0])]
            candidates = [candidates[i] for i in range(len(candidates)) if mask[i]]
            error_vectors = np.array([error_vectors[i] for i in range(error_vectors.shape[0]) if mask[i]])
            cases.pop(0)
        return random.choice(candidates)

    def search(self, X, y, metric, min_or_max='min'):
        self.population = self._init_population()
        self._evaluate_population(X, y, metric, min_or_max)

        for generation in range(self.n_steps):

            if self.verbose > 0:
                print("Generation:", generation,
                      "Error:", round(self.best_error, 6))

            next_population = []
            for i in range(self.population_size):
                parent = self._select_parent(min_or_max)
                child = self.mutation.mutate(parent)
                next_population.append(child)
            self.population = next_population
            self._evaluate_population(X, y, metric, min_or_max)

            if self.best_error == 0:
                break

        return self.best
