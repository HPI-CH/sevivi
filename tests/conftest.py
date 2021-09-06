import os

import pytest


@pytest.fixture(scope="function")
def run_in_repo_root(request):
    if os.getcwd().endswith("tests"):
        os.chdir("..")
    yield
    os.chdir(request.config.invocation_dir)
