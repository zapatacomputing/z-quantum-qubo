# z-quantum-qubo

## What is it?

`z-quantum-qubo` is a library with functions for manipulating Quadratic Unconstrained Binary Optimization problems (QUBO) used for  [Orquestra](https://www.zapatacomputing.com/orquestra/) – the platform developed by [Zapata Computing](https://www.zapatacomputing.com) for performing computations on quantum computers.
It's mostly a wrapper around the [`dimod`](https://docs.ocean.dwavesys.com/projects/dimod/en/latest/index.html) package.


## Usage

### Workflow
In order to use `z-quantum-qubo` in your workflow, you need to add it as an `import` in your Orquestra workflow:

```yaml
imports:
- name: z-quantum-qubo
  type: git
  parameters:
    repository: "git@github.com:zapatacomputing/z-quantum-qubo.git"
    branch: "master"
```

and then add it in the `imports` argument of your `step`:

```yaml
- name: my-step
  config:
    runtime:
      language: python3
      imports: [z-quantum-qubo]
```

Once that is done you can:
- use any `z-quantum-qubo` function by specifying its name and path as follows:
```yaml
- name: generate-random-qubo
  config:
    runtime:
      language: python3
      imports: [z-quantum-qubo]
      parameters:
        file: z-quantum-qubo/steps/utils.py
        function: generate_random_qubo
```
- use tasks which import `zquantum.qubo` in the python code (see below)

### Python

Here's an example of how to use methods from `z-quantum-qubo` in a python task:

```python
from zquantum.qubo import generate_random_qubo
qubo = generate_random_qubo(10)
```

Even though it's intended to be used with Orquestra, `z-quantum-qubo` can be also used as a standalone Python module.
To install it, you just need to run `pip install -e .` from the main directory.

## Development and Contribution

- If you'd like to report a bug/issue please create a new issue in this repository.
- If you'd like to contribute, please create a pull request.

### Running tests

Unit tests for this project can be run using `pytest .` from the main directory.
