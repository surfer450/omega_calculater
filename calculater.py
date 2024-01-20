from operators import Operator, OpenBracket, CreateOperator, MathArithmeticError
from typing import List
from input_handler import InputReceiver, InputParser, InputValidator, MathSyntaxError

BRACKET_STATE, END_STATE, PRIORITY_STATE = 0, 1, 2


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
    try:
        temp_operator_obj = operator_list[-1]
        operands_lst_for_operator = []

        for i in range(temp_operator_obj.get_number_of_operands()):
            operands_lst_for_operator.insert(0, operand_list.pop(len(operand_list) - 1))
        operand_list.append(round(temp_operator_obj.calculate(operands_lst_for_operator), 8))
        operator_list.pop(len(operator_list) - 1)

    except IndexError:
        raise MathSyntaxError("you used the operator [{0}] incorrectly!".format(operator_list[-1].get_symbol()))


def is_output_valid(operand_list: List[float]):
    """
    checks if output is valid(only one operand)
    :param operand_list: list contains the output
    :return: None
    """
    if len(operand_list) != 1:
        raise MathSyntaxError("your syntax was wrong!!!")


def activate_operators(operator_list: List[Operator], operand_list: List[float], state: int,
                       operator_obj: Operator | None):
    """
    the function activate a list of operators in 3 different states: end of expression, higher priority, end of brackets
    :param operator_list: operator list to activate
    :param operand_list: operand list to activate the operators on
    :param state: the state to activate the operators in
    :param operator_obj: last operator found
    :return: None
    """
    if state == BRACKET_STATE:
        while type(operator_list[-1]) is not OpenBracket:
            execute_last_operator_in_operator_list(operator_list, operand_list)
        operator_list.pop(len(operator_list) - 1)

    elif state == END_STATE:
        while len(operator_list) > 0:
            execute_last_operator_in_operator_list(operator_list, operand_list)

    elif state == PRIORITY_STATE:
        while (len(operator_list) > 0 and is_priority_higher(operator_list[-1], operator_obj)
               and type(operator_obj) is not OpenBracket):
            execute_last_operator_in_operator_list(operator_list, operand_list)


def calculate_math_expression(math_expr: List[str]) -> float:
    """
    this function calculates math expressions
    :param math_expr: math expression as list
    :return: the answer of the math expression if succeeded
    """
    operand_list = []
    operator_list = []
    symbol_index = 0

    while symbol_index < len(math_expr):
        symbol = math_expr[symbol_index]
        if symbol.replace(".", "").isnumeric():
            operand_list.append(float(symbol))

        elif CreateOperator.is_operator(symbol):
            operator_obj = CreateOperator.get_operator(symbol)
            CreateOperator.change_operator_priority(math_expr, symbol_index, operator_obj)
            activate_operators(operator_list, operand_list, PRIORITY_STATE, operator_obj)
            operator_list.append(operator_obj)

        symbol_index += 1
        if symbol == ")":
            activate_operators(operator_list, operand_list, BRACKET_STATE, None)

    activate_operators(operator_list, operand_list, END_STATE, None)
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
        print("Eof Error: entered eof!")

    except MathArithmeticError as mae:
        print("Math Arithmetic Error: " + mae.msg)

    except MathSyntaxError as mse:
        print("Math Syntax Error: " + mse.msg)

    except OverflowError:
        print("Over flow Error: number too big!")

    except KeyboardInterrupt:
        print("\nyou finished the program!")

    print("-----------------")


if __name__ == "__main__":
    main()
