from calculator_without import Calculator
import pytest

calc = Calculator()

def test_sum_impacts_state():
    assert calc.sum(5, 5) == 10
    assert calc.last_result == 10

def test_check_initial_state():
    assert calc.last_result == 0

def test_sum_positive_numbers():
    assert calc.sum(5, 4) == 9

def test_sum_negative_numbers():
    assert calc.sum(-6, -10) == -16

def test_sum_positive_and_negative():
    assert calc.sum(-6, 6) == 0

def test_sum_floats():
    res = calc.sum(5.6, 4.3)
    assert round(res, 1) == 9.9

def test_sum_with_zero():
    assert calc.sum(10, 0) == 10

def test_division():
    assert calc.div(10, 2) == 5

def test_division_by_zero():
    with pytest.raises(ArithmeticError, match="На ноль делить нельзя"):
        calc.div(10, 0)

@pytest.mark.ich_ser_gut
def test_avg_empty_list():
    assert calc.avg([]) == 0

def test_avg_list():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 5]
    assert calc.avg(numbers) == 5

@pytest.mark.xfail(reason="Метод в процессе разработки")
def test_sum_positive_nums():
    res = Calculator().sum(4, 5)
    assert res == 9