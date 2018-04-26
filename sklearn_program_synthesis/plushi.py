import time
import json
import requests
from subprocess import Popen

import numpy as np


PLUSHI_PORT = 8075


def type_to_plushi_type(typ) -> str:
    """Returns a string denoting the Push type version of given python/numpy
    type.
    Parameters
    ----------
    typ: A python or numpy type.
    Returns
    -------
    A string with a ``_`` as the first char. This is how Pysh types are denoted
    throughout the entire package. If there is no appropriate Pysh type,
    returns False.
    Examples
    --------
    >>> type_to_pysh_type(int)
    'integer'
    """
    if typ in (bool, np.bool_):
        return 'boolean'
    elif typ in (np.int64, int):
        return 'integer'
    elif typ in (float, np.float, np.float64):
        return 'float'
    elif typ in (str, bytes):
        return 'string'
    else:
        raise ValueError("Could not find matching plushi type for: " + str(typ))


def plushi_request(request_body):
    # print()
    # print(request_body)
    r = requests.post("http://localhost:{port}/".format(port=PLUSHI_PORT),
                      json=json.dumps(request_body))
    return r.json()


def start_plushi():
    p = Popen(['java', '-jar', 'plushi-standalone.jar', '-s', '-p', str(PLUSHI_PORT)])
    for attempt in range(5):
        try:
            plushi_request({"action": "types"})
            break
        except requests.exceptions.ConnectionError:
            time.sleep(2)
    return p


def plushi_instruction_set(arity, types):
    instr_dicts = plushi_request({
        'action': 'instructions',
        'arity': arity
    })
    instruction_set = []
    for instr in instr_dicts:
        if instr['input-types'] == 'STATE' or instr['output-types'] == 'STATE':
            instruction_set.append(instr)
        else:
            i_types = instr['input-types'] + instr['output-types']
            if any(x in i_types for x in types):
                instruction_set.append(instr)
    return instruction_set


def run_on_dataset(program, output_types, X):
    request_body = {
        'action': 'run',
        'code': program,
        'arity': X.shape[1],
        'output-types': output_types,
        'dataset': X.tolist()
    }
    y_hat = np.array(plushi_request(request_body))
    return y_hat
