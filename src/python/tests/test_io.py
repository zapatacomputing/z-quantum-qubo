import pytest
import dimod
from dimod.serialization.json import DimodEncoder, DimodDecoder
from zquantum.qubo.io import read_qubo_from_json, write_qubo_to_json
import json
from io import StringIO

def test_qubo_io():
    qubo = dimod.BinaryQuadraticModel({0: 1, 1: 2, 2: 3}, {(0,0): 0.5, (0,1): 0.7, (0,2): 0.9}, offset=0, vartype=dimod.BINARY)
    output_file = StringIO()

    save_qubo(qubo, output_file)
    # Move to the beginning of the file
    output_file.seek(0)
    new_qubo = load_qubo(output_file)

    assert qubo == new_qubo
