from .plushi import (
    type_to_plushi_type,
    plushi_instruction_set,
    run_on_dataset)
from .spawn import RandomPushSpawner
from .mutation import UMADMutation
from .annealing import Annealer
from .evolution import Evolver

from sklearn.base import BaseEstimator


class ProgramSynthesizer(BaseEstimator):

    def __init__(self, *, arity, metric, min_or_max='min', types='all',
                 search_method='annealing',
                 verbose=0):
        self.verbose = verbose
        self.metric = metric
        self.min_or_max = min_or_max
        instruction_set = plushi_instruction_set(arity, types)

        if search_method == 'annealing':
            self.mutation = UMADMutation(RandomPushSpawner(instruction_set))
            self.searcher = Annealer(2000, 1, self.mutation, verbose=self.verbose)
        elif search_method == 'evolution':
            self.mutation = UMADMutation(RandomPushSpawner(instruction_set))
            self.searcher = Evolver(100, 100, self.mutation, verbose=self.verbose)
        else:
            self.searcher = search_method

    def fit(self, X, y):
        self._fit_program = self.searcher.search(X, y, self.metric, self.min_or_max)
        self._fit_program_outputs = [type_to_plushi_type(y.dtype)]

    def predict(self, X):
        return run_on_dataset(self._fit_program,
                              self._fit_program_outputs,
                              X).flatten()
