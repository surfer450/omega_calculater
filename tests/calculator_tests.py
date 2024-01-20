import pytest
import calculater
from input_handler import InputParser, MathSyntaxError, InputValidator


class TestCalculator:
    def setup_method(self, method):
        print(f"Setting up {method}")

    def teardown_method(self, method):
        print(f"Tearing down {method}\n")

    # simple syntax errors tests
    @pytest.mark.parametrize("math_expression",
                             ["3^*2",
                              "sagy bar joseph",
                              "",
                              " ",
                              "\t"])
    def test_syntax(self, math_expression):
        with pytest.raises(MathSyntaxError):
            math_expression = InputParser.parse_math_expression(math_expression)
            InputValidator.validate_math_expression(math_expression)
            calculater.calculate_math_expression(math_expression)

    # simple operators tests
    @pytest.mark.parametrize("math_expression, result",
                             [("5.5+2.5", 8),
                              ("10-10", 0),
                              ("20*20", 400),
                              ("999/3", 333),
                              ("15^2", 225),
                              ("44@-24", 10),
                              ("10.4$-10.2", 10.4),
                              ("10.2&-10.4", -10.4),
                              ("15%4", 3),
                              ("~6.5+5", -1.5),
                              ("6!/5!", 6),
                              ("4*2!+3", 11),
                              ("~4^2", 16),
                              ("4/2^2*10", 10),
                              ("1.1+2.1*3.1-2.2", 5.41),
                              ("32#!", 120)])
    def test_simple_expressions(self, math_expression, result):
        math_expression = InputParser.parse_math_expression(math_expression)
        InputValidator.validate_math_expression(math_expression)
        assert calculater.calculate_math_expression(math_expression) == result

    # complicated expressions tests
    @pytest.mark.parametrize("math_expression, result",
                             [("(2!^-2) @ ((~2+---2) * 5+40)", 10.125),
                              ("~ ( ( - ( 1 0 0 ^ 0 . 5 ) ) $ - 9 ) ^  0 . 5^ 4 / 9", 9),
                              ("~(-1^-1)! & 0 - (---3!/---3) *-2.5", 5),
                              ("((-5)^(2))%4   /   (--4!)/(-2^-2/6)", -1),
                              ("(-52#^2+1)/10*((-5)/-2)^10%2", -4.8),
                              ("3!!/72+(0^2-10) + -(9.5@-11.5)^0/2", 0.5),
                              ("(1!-2)*(3/4^5%6)@7$8&9+~(10##)", -9),
                              ("1-( ~ - 2 - ( - 1 ! -   - (~--2^--3)+3)*3)", -19),
                              ("    (((1@2@3.5/10)+0.75)*5)!/-12      ", -10),
                              ("((4))+~-(2!)! + (1@(5$4.99)*2)^2 ", 42),
                              ("~((36^0.5)! /16 /-9)!# * 10!##", 27),
                              ("((((~0!)-(1))^5!!)/10000 * 52.5463) & 102.23/10.24562", 0),
                              ("( ((((((2+1)*2)!)/5))) )^0.5 --- (((5)!*2+10)*10)^0.5 ", -38),
                              ("(10%111#^5.9234024) + ~-----2! + -10@32 + -6^2 +~2^4 + 6+~--3", 69),
                              ("(10-3! + (4)! - (100/(4!+1)))!## ", 11),
                              ("(((10$-10)&-10   @   ((5&-5)$5)) % ((5$-5)&-5   @   ((2.5&-2.5)$2.5)))!", 1),
                              ("(~---( 1 2 3 4 5 6 7 8 9 ###%2)! @ ~-2!)^2*3+0.25 ", 7),
                              ("((((11.11#+22.22#)#!^2)*2)%10)                *2", 4),
                              ("(1234.56789#%7^-10)##   @   (12#+~-----2!)", 6),
                              ("((((((((~-3!!^~-3!)#/5) ^ 100)#!#) + ~-(5&2$4)!#)%7 / 10 ) ^ 2 * 1000) % 3)! + "
                               "~-------((((((((~-3!!^~-3!)#/5) ^ 100)#!#) + ~-(5&2$4)!#)%7 / 10 ) ^ 2 * 1000) % "
                               "3)!", 2)])
    def test_complicated_expressions(self, math_expression, result):
        math_expression = InputParser.parse_math_expression(math_expression)
        InputValidator.validate_math_expression(math_expression)
        assert calculater.calculate_math_expression(math_expression) == result
