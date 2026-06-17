from simple_math import SimpleMath
import pytest

@pytest.fixture
def simple_math():
    return SimpleMath()

def test_square_math(simple_math):
    assert simple_math.square(2) == 4


def test_cube_math(simple_math):
    assert simple_math.cube(-3) == -27