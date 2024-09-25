import os

from invoke import task

PATHS_TO_FORMAT = "."
REQUIRMENTS_PATH = "src/environment"
NOTEBOOKS_PATH = "src/Notebooks"


@task
def format(c):
    c.run(f"isort --profile black {PATHS_TO_FORMAT}")
    c.run(f"black {PATHS_TO_FORMAT}")


@task
def formatcheck(c):
    c.run(f"isort --profile black {PATHS_TO_FORMAT} -c")
    c.run(f"black --check {PATHS_TO_FORMAT}")


@task
def update(c):
    # c.run(f"pip-compile {REQUIRMENTS_PATH}/requirements.in")
    # c.run(f"pip-compile {REQUIRMENTS_PATH}/dev-requirements.in")
    c.run(f"pip3 install -r {REQUIRMENTS_PATH}/requirements.txt")
    # c.run(f"pip3 install -r {REQUIRMENTS_PATH}/dev-requirements.txt")


NOTEBOOKS_PATH = "src/notebooks"


def clear_notebook_outputs(notebook_path, c):
    c.run(
        f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace {notebook_path}"
    )


@task
def clearnotebooks(c):
    root = NOTEBOOKS_PATH
    for file in os.listdir(root):
        if file.endswith(".ipynb"):
            notebook_path = os.path.join(root, file)
            clear_notebook_outputs(notebook_path, c)
            print(f"Cleared outputs for {notebook_path}")


@task
def test(c):
    c.run("pytest")
    c.run("pytest -s src/tests/test_fv_completion.py")


@task(pre=[format])
def precommit(c):
    print("Running all pre-commit tasks...")
