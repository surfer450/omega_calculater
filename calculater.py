from operators import Operator, CreateOperator, OpenBracket
from typing import List, Tuple


def is_operator(operator: str) -> bool:
    """
    this function finds if a string is an operator
    :param operator: a string to find if is operator
    :return: true if operator, false otherwise
    """
    all_operators = ["+", "-", "*", "/", "^", "@", "$", "&", "%", "~", "!", "("]
    return operator in all_operators


def is_valid_symbol(symbol: str) -> bool:
    """
    this function check if a symbol is valid to appear inside a math expression
    :param symbol: a symbol to check
    :return: true if valid, else false
    """
    return is_operator(symbol) or symbol.isnumeric() or symbol == ")" or symbol == "."


def is_open_bracket_legal(expr: str, open_bracket_index: int) -> bool:
    """
    this function checks if an open bracket is legal(there is operator before him)
    :param expr: expression to check
    :param open_bracket_index: the index to check in
    :return: true if bracket legal, else false
    """
    return ((open_bracket_index == 0 or is_operator(expr[open_bracket_index - 1])) and
            expr[open_bracket_index + 1] != ")")


def is_close_bracket_legal(expr: str, close_bracket_index: int) -> bool:
    """
    this function checks if a close bracket is legal(there is operator after him)
    :param expr: expression to check
    :param close_bracket_index: the index to check in
    :return: true if bracket legal, else false
    """
    return close_bracket_index == len(expr) - 1 or is_operator(expr[close_bracket_index + 1])


def is_point_legal(expr: str, point_index: int) -> bool:
    """
    this function checks if a point in the expression is a legal point
    :param expr: the expression to check
    :param point_index: the index of the point to check
    :return:
    """
    if not (point_index == 0 or point_index == len(expr) - 1):
        if expr[point_index - 1].isnumeric() and expr[point_index + 1].isnumeric():
            return True
    return False


def is_operator_unary_valid(operator_index: int, math_expr: str) -> bool:
    """
    this function gets an index of str unary operator in a math expression and check if it is in a valid position
    :param operator_index: the index of the unary str
    :param math_expr: the math expression to check
    :return: true if unary is in valid position, else false
    """
    operator = CreateOperator.get_operator(math_expr[operator_index])
    if operator.get_position() == -1:
        if (operator_index != len(math_expr) - 1 and
                (math_expr[operator_index + 1].isnumeric() or math_expr[operator_index + 1] == "(")):
            if operator_index == 0:
                return True
            elif is_operator(math_expr[operator_index - 1]):
                return True
        return False

    else:
        if operator_index != 0 and (math_expr[operator_index - 1].isnumeric() or math_expr[operator_index - 1] == ")"):
            if operator_index == len(math_expr) - 1:
                return True
            elif is_operator(math_expr[operator_index + 1]) or math_expr[operator_index + 1] == ")":
                return True
        return False


def is_expression_valid(math_expr: str) -> bool:
    """
    this function finds if a string is valid, contains only valid symbols
    :param math_expr: a string to find if is valid
    :return: true if valid, else false
    """
    symbol_index = 0
    for symbol in math_expr:

        if not is_valid_symbol(symbol):
            print("Unrecognised symbol in your expression [{0}]".format(symbol))
            return False

        if symbol == "." and not is_point_legal(math_expr, symbol_index):
            print("you used the point '.' symbol incorrectly in your expression")
            return False

        if symbol == "(" and not is_open_bracket_legal(math_expr, symbol_index):
            print("your syntax was wrong!!")
            return False

        if symbol == ")" and not is_close_bracket_legal(math_expr, symbol_index):
            print("your syntax was wrong!!")
            return False

        if is_operator(symbol):
            operator = CreateOperator.get_operator(symbol)
            if operator.get_number_of_operands() == 1 and not is_operator_unary_valid(symbol_index, math_expr):
                print("you used the unary operator [{0}] in your expression in the wrong way".format(symbol))
                return False

        symbol_index += 1

    return True


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
    try:
        end_index = beg_index
        while end_index < len(expression) and (expression[end_index].isnumeric() or expression[end_index] == "."):
            end_index += 1
        temp_operand = float(expression[beg_index:end_index])
        end_index -= 1
        return temp_operand, end_index
    except ValueError:
        print("you used the point '.' symbol incorrectly in your expression")
        exit(1)


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
    try:
        while symbol_index < len(math_expr):
            symbol = math_expr[symbol_index]

            if symbol.isnumeric():
                operand, new_index = find_number(math_expr, symbol_index)
                operand_list.append(operand)
                symbol_index = new_index
                symbol = math_expr[symbol_index]

            if is_operator(symbol):
                operator_obj = CreateOperator.get_operator(symbol)
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

    except IndexError:
        print("your syntax was wrong!")
        exit(1)

    except ZeroDivisionError:
        print("cant divide by zero!")
        exit(1)

    except OverflowError:
        print("number too big!")
        exit(1)

    is_output_valid(operand_list)

    return operand_list[0]


def get_math_expression() -> str:
    """
    this function get an input math expression
    :return: the math expression
    """
    try:
        math_expression = input("Enter expression: ")
        return math_expression
    except EOFError:
        print("entered eof!")
        exit(1)


def main():
    math_expression = get_math_expression()
    math_expression = math_expression.replace(" ", "")
    math_expression = math_expression.replace("\t", "")
    if math_expression.count("(") != math_expression.count(")"):
        print("amount of '( is not equals to amount of ')")
        exit(1)
    if is_expression_valid(math_expression):
        print(calculate_math_expression(math_expression))


if __name__ == "__main__":
    main()
