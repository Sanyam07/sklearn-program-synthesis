import random
from string import ascii_letters, digits


class RandomPushSpawner:

    def __init__(self,
                 instruction_set,
                 min_length=50,
                 max_length=200,
                 pct_integer=0.05,
                 pct_float=0.05,
                 pct_string=0.05,
                 pct_boolean=0.05,
                 pct_other=0.0,
                 other_atoms=None,
                 min_integer=int(-1e5),
                 max_integer=int(1e5),
                 min_float=-1.0,
                 max_float=1.0,
                 max_string_length=50,
                 valid_string_chars=ascii_letters + digits):
        self.instruction_set = instruction_set
        self.min_length = min_length
        self.max_length = max_length
        self.pct_integer = pct_integer
        self.pct_float = pct_float
        self.pct_string = pct_string
        self.pct_boolean = pct_boolean
        self.pct_other = pct_other
        self.other_atoms = other_atoms
        self.min_integer = min_integer
        self.max_integer = max_integer
        self.min_float = min_float
        self.max_float = max_float
        self.max_string_length = max_string_length
        self.valid_string_chars = valid_string_chars

    def _rand_integer(self):
        return random.randint(self.min_integer, self.max_integer)

    def _rand_float(self):
        return random.uniform(self.min_float, self.max_float)

    def _rand_string(self):
        string_length = random.randint(0, self.max_string_length)
        return ''.join([random.choice(self.valid_string_chars) for _ in range(string_length)])

    def _rand_bool(self):
        return random.choice([True, False])

    def _rand_other(self):
        if self.other_atoms is None:
            return None
        return random.choice(self.other_atoms)

    def _rand_instruction(self):
        return random.choice(self.instruction_set)['name']

    def _rand_atom(self, c_dist):
        c_probs = [0] + list(c_dist.values()) + [1]
        r = random.random()
        left = 0
        right = len(c_probs) - 1
        while True:
            if right < left:
                return -1
            center = (left + right) // 2
            if c_probs[center] < r and c_probs[center + 1] < r:
                left = center + 1
            elif c_probs[center] > r and c_probs[center + 1] > r:
                right = center - 1
            else:
                atom_type = list(c_dist.keys())[center]
                if atom_type == 'integer':
                    return self._rand_integer()
                elif atom_type == 'float':
                    return self._rand_float()
                elif atom_type == 'boolean':
                    return self._rand_bool()
                elif atom_type == 'string':
                    return self._rand_string()
                elif atom_type == 'other':
                    return self._rand_other()
                elif atom_type == 'instruction':
                    return self._rand_instruction()
                else:
                    raise ValueError("Unknown atom type: " + atom_type)

    def random_program_of_size(self, size):
        dist = {
            'integer': self.pct_integer,
            'float': self.pct_float,
            'boolean': self.pct_boolean,
            'string': self.pct_string,
            'other': self.pct_other
        }

        sum_of_literal_probs = sum(dist.values())
        if sum_of_literal_probs > 1.0:
            raise ValueError("Sum of literal probabilities must be <= 1.")

        dist['instruction'] = 1 - sum_of_literal_probs

        # Cumlitive distribution
        c_dist = {}
        c_prob = 0.0
        for k, v in dist.items():
            if v > 0.0:
                c_prob += v
                c_dist[k] = c_prob

        program = [self._rand_atom(c_dist) for _ in range(size)]
        return program

    def random_program(self):
        program_length = random.randint(self.min_length, self.max_length)
        return self.random_program_of_size(program_length)

    def random_population(self, n):
        return [self.random_program() for _ in range(n)]


if __name__ == '__main__':
    rps = RandomPushSpawner([{'name': 'plushi:foo'}, {'name': 'plushi:bar'}])
    pop = rps.random_population(10)
    print(pop)
