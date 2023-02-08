# to enable parent directory imports
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest


# Mark the test root directory
TEST_DIR = os.path.dirname(os.path.abspath(__file__))


# Context to retain objects passed between steps
class Context:
    foo = None


@pytest.fixture()
def foo_bar():
    return None
