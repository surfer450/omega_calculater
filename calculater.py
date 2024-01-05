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


def is_priority_bigger(first_operator: str, second_operator: str) -> bool:
    """
    this function finds if first operator priority is bigger
    :param first_operator: first operator as string
    :param second_operator: second operator as string
    :return: true if first operator priority is bigger, else false
    """
    power_dict = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "@": 5, "$": 5, "&": 5, "%": 4, "~": 6, "!": 6}
    return power_dict[first_operator] > power_dict[second_operator]


def calculate_math_expression(math_expr: str):
    """
    this function calculates math expressions as strings
    :param math_expr: math expression as string
    :return: the answer of the math expression if succeeded, else None
    """
    operand_list = []
    operator_list = []

    for symbol in math_expr:
        if symbol.isnumeric():
            operand_list.append(float(symbol))

        elif is_operator(symbol):
            operator_list.append(symbol)


def main():
    math_expression = input("Enter expression: ")
    if is_expression_valid(math_expression):
        calculate_math_expression(math_expression)


if __name__ == "__main__":
    main()