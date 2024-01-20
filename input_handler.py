from operators import CreateOperator
from typing import List, Tuple


class MathSyntaxError(SyntaxError):
    """
    this is a class for a syntax error in a math expression
    """

    def __init__(self, msg: str):
        """
        this is a constructor for syntax error in a math expression
        :param msg: a message error to give
        """
        SyntaxError.__init__(self, msg)


class InputReceiver:
    """
    this class is responsible for getting input form the user
    """

    @staticmethod
    def get_math_expression() -> str:
        """
        this function get an input math expression
        :return: the math expression
        """
        print("Omega Calculator\n"
              "-----------------")
        math_expression = input("Enter expression: ")
        return math_expression


class InputParser:
    @staticmethod
    def remove_spaces(math_expression: str) -> str:
        """
        this function gets a string math expression and remove all spaces and tabs from it
        :param math_expression: the string to change
        :return: the new math expression after removing spaces
        """
        return (math_expression.replace(" ", "")).replace("\t", "")

    @staticmethod
    def replace_multiple_subtraction(math_expr: List[str], index: int) -> Tuple[List[str], int]:
        """
        this function replace multiple minuses from a math expression
        with one operator: + for even amount of binary -,
        nothing for even amount of unary -, + for uneven amount of binary -,
        | for uneven amount of unary -
        :param math_expr: expression to change
        :param index: index to replace from
        :return: new math expression
        """
        amount_removed = InputParser.remove_multiple_subtraction(math_expr, index)
        if InputValidator.is_minus_unary(math_expr[index - 1], index):
            if amount_removed % 2 != 0:
                math_expr.insert(index, "|")

        else:
            math_expr.insert(index, "-")
            if amount_removed % 2 == 0:
                math_expr.insert(index + 1, "|")
                index += 1

        return math_expr, index

    @staticmethod
    def remove_multiple_subtraction(math_expr: List[str], beg_index) -> int:
        """
        this function remove all multiple minus signs from a certain index
        :param math_expr: expression to remove from
        :param beg_index: index to start from
        :return: amount of minuses removed
        """

        amount_of_minus = 0
        last_symbol = math_expr[beg_index - 1]

        while math_expr[beg_index] == '-':
            if InputValidator.is_minus_unary(last_symbol, beg_index):
                if CreateOperator.is_operator(math_expr[beg_index + 1]) and math_expr[beg_index + 1] not in ["-", "("]:
                    raise MathSyntaxError("illegal use of operator [-] ")
            last_symbol = math_expr.pop(beg_index)
            amount_of_minus += 1

        return amount_of_minus

    @staticmethod
    def find_number(expression: List[str], beg_index: int) -> List[str]:
        """
        this function finds a number from a starting index inside a list and replace it into one element
        :param expression: an expression to find the number from
        :param beg_index: index to start from
        :return: a tuple containing the new list
        """
        str_num = ""
        while beg_index < len(expression) and (expression[beg_index].isnumeric() or expression[beg_index] == "."):
            str_num += expression[beg_index]
            expression.pop(beg_index)
        expression.insert(beg_index, str_num)
        return expression

    @staticmethod
    def parse_math_expression(math_expression: str) -> List[str]:
        """
        this function gets a math expression and parse it turning it into a string the calculater can calculate
        :param math_expression: str to parse
        :return: math expression after parsing it
        """
        math_expression = list(InputParser.remove_spaces(math_expression))
        symbol_index = 0
        while symbol_index < len(math_expression):
            symbol = math_expression[symbol_index]
            if symbol == "-":
                math_expression, symbol_index = InputParser.replace_multiple_subtraction(math_expression, symbol_index)
            if symbol.isnumeric():
                math_expression = InputParser.find_number(math_expression, symbol_index)
            symbol_index += 1
        print(math_expression)
        return math_expression


class InputValidator:

    @staticmethod
    def is_minus_unary(last_symbol: str, index: int) -> bool:
        """
        this function gets an index of a minus operator and what symbol is before him and checks if it is unary or not
        :param last_symbol: symbol before minus in math expression
        :param index: index to check
        :return: true if unary, else false
        """
        return index == 0 or (CreateOperator.is_operator(last_symbol) and CreateOperator.get_operator(
            last_symbol).get_number_of_operands() != 1) or last_symbol in ["~", "-"]

    @staticmethod
    def is_valid_symbol(symbol: str) -> bool:
        """
        this function check if a symbol is valid to appear inside a math expression
        :param symbol: a symbol to check
        :return: true if valid, else false
        """
        return CreateOperator.is_operator(symbol) or symbol.isnumeric() or symbol == ")" or symbol == "."

    @staticmethod
    def is_open_bracket_legal(expr: List[str], open_bracket_index: int) -> bool:
        """
        this function checks if an open bracket is legal(there is operator before him)
        :param expr: expression to check
        :param open_bracket_index: the index to check in
        :return: true if bracket legal, else false
        """
        return ((open_bracket_index == 0 or CreateOperator.is_operator(expr[open_bracket_index - 1])
                 or expr[open_bracket_index - 1] == "("))

    @staticmethod
    def is_close_bracket_legal(expr: List[str], close_bracket_index: int) -> bool:
        """
        this function checks if a close bracket is legal(there is operator after him)
        :param expr: expression to check
        :param close_bracket_index: the index to check in
        :return: true if bracket legal, else false
        """
        return (close_bracket_index == len(expr) - 1 or CreateOperator.is_operator(expr[close_bracket_index + 1])
                or expr[close_bracket_index + 1] == ")")

    @staticmethod
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

    @staticmethod
    def is_operator_unary_left_valid(operator_index: int, math_expr: List[str]):
        """
        this function gets an index of str left unary operator in a math expression and check if it is in a valid position
        :param operator_index: the index of the unary str
        :param math_expr: the math expression to check
        :return: true if unary is in valid position, else false
        """
        if operator_index != len(math_expr) - 1:
            symbol, symbol_after = math_expr[operator_index], math_expr[operator_index+1]
            if symbol_after.replace(".", "").isnumeric() or symbol_after in ["(", "|"] or (symbol == "~" and symbol_after == "|"):
                if operator_index == 0:
                    return True
                symbol_before = math_expr[operator_index-1]
                if CreateOperator.is_operator(symbol_before):
                    return True
        return False

    @staticmethod
    def is_operator_unary_right_valid(operator_index: int, math_expr: List[str]):
        """
        this function gets an index of str right unary operator in a math expression and check if it is in a valid position
        :param operator_index: the index of the unary str
        :param math_expr: the math expression to check
        :return: true if unary is in valid position, else false
        """
        if operator_index != 0:
            symbol, symbol_before = math_expr[operator_index], math_expr[operator_index-1]
            if symbol_before.replace(".", "").isnumeric() or symbol_before == ")" or CreateOperator.get_operator(symbol_before).get_position() == 1:
                if operator_index == len(math_expr) - 1:
                    return True
                symbol_after = math_expr[operator_index+1]
                if CreateOperator.is_operator(symbol_after) or math_expr[operator_index + 1] == ")":
                    return True
        return False

    @staticmethod
    def is_operator_unary_valid(operator_index: int, math_expr: List[str]) -> bool:
        """
        this function gets an index of str unary operator in a math expression and check if it is in a valid position
        :param operator_index: the index of the unary str
        :param math_expr: the math expression to check
        :return: true if unary is in valid position, else false
        """
        operator = CreateOperator.get_operator(math_expr[operator_index])
        if operator.get_position() == -1:
            return InputValidator.is_operator_unary_left_valid(operator_index, math_expr)
        else:
            return InputValidator.is_operator_unary_right_valid(operator_index, math_expr)

    @staticmethod
    def is_amount_of_brackets_legal(math_expression: List[str]) -> bool:
        """
        this function check is amount of ( is equals to amount of ) in a math expression
        :param math_expression: string to check if amount of bracket is legal
        :return: true if legal, else false
        """
        return math_expression.count("(") == math_expression.count(")")

    @staticmethod
    def validate_whole_expression(math_expr: List[str]):
        """
        validate the whole math expression before looping through it and raise en exception if there was a problem
        :param math_expr: the math expression to check
        :return:
        """
        if not math_expr:
            raise MathSyntaxError("you entered nothing to calculate!")

        if not InputValidator.is_amount_of_brackets_legal(math_expr):
            raise MathSyntaxError("the amount of [(] and [)] is not the same!")

    @staticmethod
    def validate_element_in_expression(math_expr: List[str], element_index: int, count_brackets: int):
        """
        validate each element in math expression: operand or operator, raise exception if there was a problem
        :param math_expr: math expression to check the element in
        :param element_index: the element index
        :param count_brackets: counter of bracket from function
        :return: new counter of bracket if there was no error
        """
        element = math_expr[element_index]

        if element == "(" and math_expr[element_index + 1] == ")":
            raise MathSyntaxError("you entered empty brackets [()]")

        if element == "(" and not InputValidator.is_open_bracket_legal(math_expr, element_index):
            raise MathSyntaxError("you are missing an operator before bracket[(]")

        if element == "(":
            count_brackets += 1

        if element == ")" and not InputValidator.is_close_bracket_legal(math_expr, element_index):
            raise MathSyntaxError("you are missing an operator after bracket[)]")

        if element == ")":
            count_brackets += -1

        if (CreateOperator.is_operator(element) and CreateOperator.get_operator(element).get_number_of_operands() == 1
                and not InputValidator.is_operator_unary_valid(element_index, math_expr)):
            raise MathSyntaxError("you used the unary operator [{0}] in your expression in the wrong way".format(element))

        if count_brackets < 0:
            raise MathSyntaxError("your use of brackets was wrong!")

        return count_brackets

    @staticmethod
    def validate_symbol_in_element(element: str, symbol_index: int):
        """
        validate each symbol in an element in the math expression, raise an exception if there was a problem
        :param element: element in math expression: number or operand as string
        :param symbol_index: the symbol index in the element
        :return: None
        """
        symbol = element[symbol_index]

        if not InputValidator.is_valid_symbol(symbol):
            raise MathSyntaxError("Unrecognised symbol in your expression [{0}]".format(symbol))

        if symbol == "." and not InputValidator.is_point_legal(element, symbol_index):
            raise MathSyntaxError("you used the point '.' symbol incorrectly in your expression")

    @staticmethod
    def validate_math_expression(math_expr: List[str]):
        """
        this function finds if a math expression is valid with no math syntax error, if there are it raise syntax error
        :param math_expr: a list math expression to find if is valid
        :return: None
        """
        element_index = 0
        count_brackets = 0
        InputValidator.validate_whole_expression(math_expr)

        for element in math_expr:
            symbol_index = 0
            for symbol in element:
                InputValidator.validate_symbol_in_element(element, symbol_index)
                symbol_index += 1

            count_brackets = InputValidator.validate_element_in_expression(math_expr, element_index, count_brackets)
            element_index += 1
