from operators import MathArithmeticError
from input_handler import InputReceiver, InputParser, InputValidator, MathSyntaxError
from calc_engine import Calc


def main():
    try:
        math_expression = InputReceiver.get_math_expression()
        math_expression = InputParser.parse_math_expression(math_expression)
        InputValidator.validate_math_expression(math_expression)
        answer = Calc.calculate_math_expression(math_expression)
        print(answer)

    except EOFError:
        print("Eof Error: entered eof!")

    except MathArithmeticError as mae:
        print("Math Arithmetic Error: " + mae.msg)

    except MathSyntaxError as mse:
        print("Math Syntax Error: " + mse.msg)

    except OverflowError:
        print("Over flow Error: number too big!")

    except ZeroDivisionError:
        print("Zero Division Error: can't dived by zero")

    except KeyboardInterrupt:
        print("\nyou finished the program!")

    print("-----------------")


if __name__ == "__main__":
    main()
