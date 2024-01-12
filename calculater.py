from operators import Operator, OpenBracket, CreateOperator
from typing import List, Tuple
from input_handler import InputReceiver, InputParser, InputValidator


def is_priority_higher(first_operator: Operator, second_operator: Operator) -> bool:
    """
    this function finds if first operator priority is bigger
    :param first_operator: first operator as operator obj
    :param second_operator: second operator as operator obj
    :return: true if first operator priority is bigger, else false
    """
    return first_operator.get_priority() >= second_operator.get_priority()


def execute_last_operator_in_operator_list(operator_list: List[Operator], operand_list: List[float]):
    """
    this function execute the last operator in operator list created by the calculate_math_expression function
    :param operator_list: the list of operators in the math expression
    :param operand_list: the list of operands in the math expression
    :return: None
    """

    temp_operator_obj = operator_list[-1]
    operands_lst_for_operator = []
    for i in range(temp_operator_obj.get_number_of_operands()):
        operands_lst_for_operator.insert(0, operand_list.pop(len(operand_list) - 1))
    operand_list.append(temp_operator_obj.calculate(operands_lst_for_operator))
    operator_list.pop(len(operator_list) - 1)


def find_number(expression: str, beg_index: int) -> Tuple[float, int]:
    """
    this function finds a number from a starting index inside a string
    :param expression: an expression to find the number from
    :param beg_index: index to start from
    :return: a tuple containing the number in the string and its end index
    """
    end_index = beg_index
    while end_index < len(expression) and (expression[end_index].isnumeric() or expression[end_index] == "."):
        end_index += 1
    temp_operand = float(expression[beg_index:end_index])
    end_index -= 1
    return temp_operand, end_index


def is_output_valid(operand_list: List[float]):
    if len(operand_list) != 1:
        print("your syntax was wrong!")
        exit(1)

    if isinstance(operand_list[0], complex):
        print("you got a complex number!")
        exit(1)


def calculate_math_expression(math_expr: str) -> float | None:
    """
    this function calculates math expressions as strings
    :param math_expr: math expression as string
    :return: the answer of the math expression if succeeded, else None
    """
    operand_list = []
    operator_list = []
    symbol_index = 0

    while symbol_index < len(math_expr):
        symbol = math_expr[symbol_index]

        if symbol.isnumeric():
            operand, new_index = find_number(math_expr, symbol_index)
            operand_list.append(operand)
            symbol_index = new_index
            symbol = math_expr[symbol_index]

        if InputValidator.is_operator(symbol):
            operator_obj = CreateOperator.get_operator(symbol)
            if (symbol_index != 0 and symbol == "|" and InputValidator.is_operator(math_expr[symbol_index-1])
                    and math_expr[symbol_index-1] != "("):
                operator_obj.set_priority(7)
            while (len(operator_list) > 0 and is_priority_higher(operator_list[-1], operator_obj)
                   and type(operator_obj) is not OpenBracket):
                execute_last_operator_in_operator_list(operator_list, operand_list)
            operator_list.append(operator_obj)

        symbol_index += 1

        if symbol == ")":
            while type(operator_list[-1]) is not OpenBracket:
                execute_last_operator_in_operator_list(operator_list, operand_list)
            operator_list.pop(len(operator_list) - 1)

    while len(operator_list) > 0:
        execute_last_operator_in_operator_list(operator_list, operand_list)

    is_output_valid(operand_list)
    return operand_list[0]


def main():
    try:
        math_expression = InputReceiver.get_math_expression()
        math_expression = InputParser.parse_math_expression(math_expression)
        InputValidator.validate_math_expression(math_expression)
        answer = calculate_math_expression(math_expression)
        print(answer)

    except EOFError:
        print("entered eof!")

    except SyntaxError as se:
        print("syntax error: " + se.msg)

    except IndexError:
        print("your use of operators was wrong!")

    except ZeroDivisionError:
        print("cant divide by zero!")

    except OverflowError:
        print("number too big!")

    except ValueError:
        print("you used the point '.' symbol incorrectly in your expression")


if __name__ == "__main__":
    main()
