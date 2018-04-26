from abc import ABCMeta, abstractmethod
import random


class Mutation(metaclass=ABCMeta):

    def __init__(self, push_spawner):
        self.push_spawner = push_spawner

    @abstractmethod
    def mutate(self, parent):
        ...


class AdditionMutation(Mutation):

    def __init__(self, push_spawner, rate=0.09):
        super().__init__(push_spawner)
        self.rate = rate

    def mutate(self, parent):
        child = []
        for atom in parent:
            if random.random() < self.rate:
                new_atom = self.push_spawner.random_program_of_size(1)[0]
                if random.random() < 0.5:
                    child.append(new_atom)
                    child.append(atom)
                else:
                    child.append(atom)
                    child.append(new_atom)
            else:
                child.append(atom)
        return child


class DeletionMutation(Mutation):

    def __init__(self, push_spawner, rate=0.0826):
        super().__init__(push_spawner)
        self.rate = rate

    def mutate(self, parent):
        child = []
        for atom in parent:
            if random.random() > self.rate:
                child.append(atom)
        if len(child) == 0:
            return parent
        return child


class UMADMutation(Mutation):

    def __init__(self,
                 push_spawner,
                 addition_rate=0.09,
                 deletion_rate=0.0826):
        super().__init__(push_spawner)
        self._add_mut = AdditionMutation(push_spawner, addition_rate)
        self._del_mut = DeletionMutation(push_spawner, deletion_rate)

    def mutate(self, parent):
        return self._del_mut.mutate(self._add_mut.mutate(parent))
