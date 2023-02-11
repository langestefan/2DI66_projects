import pytest
import sys, os

# to enable parent directory imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Mark the test root directory
TEST_DIR = os.path.dirname(os.path.abspath(__file__))


# Context to retain objects passed between steps
class Context:
    foo = None


@pytest.fixture()
def foo_bar():
    return None
