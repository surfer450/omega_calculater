from operators import Operator, CreateOperator
from typing import List


def is_operator(operator: str) -> bool:
    """
    this function finds if a string is an operator
    :param operator: a string to find if is operator
    :return: true if operator, false otherwise
    """
    all_operators = ["+", "-", "*", "/", "^", "@", "$", "&", "%", "~", "!"]
    return operator in all_operators


def is_expression_valid(math_expr: str) -> bool:
    """
    this function finds if a string is valid, contains only valid symbols
    :param math_expr: a string to find if is valid
    :return: true if valid, else false
    """
    for symbol in math_expr:
        if not (is_operator(symbol) or symbol.isnumeric() or symbol == " "):
            print("Unrecognised symbol in your expression [{0}]".format(symbol))
            return False
    return True


def is_priority_higher(first_operator: Operator, second_operator: Operator) -> bool:
    """
    this function finds if first operator priority is bigger
    :param first_operator: first operator as operator obj
    :param second_operator: second operator as operator obj
    :return: true if first operator priority is bigger, else false
    """
    return first_operator.get_priority() > second_operator.get_priority()


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
        operands_lst_for_operator.append(operand_list.pop(len(operand_list) - 1))
    operand_list.append(temp_operator_obj.calculate(operands_lst_for_operator))
    operator_list.pop(len(operator_list) - 1)


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
            operand_list.append(float(symbol))

        elif is_operator(symbol):
            operator_obj = CreateOperator.get_operator(symbol)
            while len(operator_list) > 0 and is_priority_higher(operator_list[-1], operator_obj):
                execute_last_operator_in_operator_list(operator_list, operand_list)
            operator_list.append(operator_obj)

        symbol_index += 1

    while len(operator_list) > 0:
        execute_last_operator_in_operator_list(operator_list, operand_list)

    return operand_list[0]


def main():
    math_expression = input("Enter expression: ")
    if is_expression_valid(math_expression):
        print(calculate_math_expression(math_expression))


if __name__ == "__main__":
    main()