from operators import CreateOperator
from typing import List


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
    def change_all_subtractions_from_expression(math_expr: str):
        """
        this function removes multiple minuses from a math expression
        and replace them with one operator: + for even amount of binary -,
        nothing for even amount of unary -, + for uneven amount of binary -,
        | for uneven amount of unary -
        :param math_expr: expression to change
        :return: new math expression
        """
        index, length, math_expr = 0, len(math_expr), list(math_expr)
        while index < len(math_expr):
            if math_expr[index] == "-":
                amount_removed = InputParser.remove_multiple_subtraction(math_expr, index)

                if InputValidator.is_minus_unary(math_expr[index-1], index):
                    if amount_removed % 2 != 0:
                        math_expr.insert(index, "|")
                else:
                    math_expr.insert(index, "-")
                    if amount_removed % 2 == 0:
                        math_expr.insert(index+1, "|")
                        index += 1

            index += 1
        print(math_expr)
        math_expr = ''.join(math_expr)
        return math_expr

    @staticmethod
    def remove_multiple_subtraction(math_expr: List[str], beg_index) -> int:
        """
        this function remove all multiple minus signs from a certain index
        :param math_expr: expression to remove from
        :param beg_index: index to start from
        :return: amount of minuses removed
        """

        amount_of_minus = 0
        while math_expr[beg_index] == '-':
            amount_of_minus += 1
            math_expr.remove('-')
        return amount_of_minus

    @staticmethod
    def parse_math_expression(math_expression: str) -> str:
        """
        this function gets a math expression and parse it turning it into a string the calculater can calculate
        :param math_expression: str to parse
        :return: math expression after parsing it
        """
        math_expression = InputParser.remove_spaces(math_expression)
        math_expression = InputParser.change_all_subtractions_from_expression(math_expression)
        return math_expression


class InputValidator:
    @staticmethod
    def is_operator(operator: str) -> bool:
        """
        this function finds if a string is an operator
        :param operator: a string to find if is operator
        :return: true if operator, false otherwise
        """
        all_operators = ["+", "-", "*", "/", "^", "@", "$", "&", "%", "~", "!", "(", "|"]
        return operator in all_operators

    @staticmethod
    def is_minus_unary(last_symbol: str, index: int) -> bool:
        """
        this function gets an index of a minus operator and what symbol is before him and checks if it is unary or not
        :param last_symbol: symbol before minus in math expression
        :param index: index to check
        :return: true if unary, else false
        """
        return index == 0 or InputValidator.is_operator(last_symbol)

    @staticmethod
    def is_valid_symbol(symbol: str) -> bool:
        """
        this function check if a symbol is valid to appear inside a math expression
        :param symbol: a symbol to check
        :return: true if valid, else false
        """
        return InputValidator.is_operator(symbol) or symbol.isnumeric() or symbol == ")" or symbol == "."

    @staticmethod
    def is_open_bracket_legal(expr: str, open_bracket_index: int) -> bool:
        """
        this function checks if an open bracket is legal(there is operator before him)
        :param expr: expression to check
        :param open_bracket_index: the index to check in
        :return: true if bracket legal, else false
        """
        return ((open_bracket_index == 0 or InputValidator.is_operator(expr[open_bracket_index - 1])
                 or expr[open_bracket_index - 1] == "(") and expr[open_bracket_index + 1] != ")")

    @staticmethod
    def is_close_bracket_legal(expr: str, close_bracket_index: int) -> bool:
        """
        this function checks if a close bracket is legal(there is operator after him)
        :param expr: expression to check
        :param close_bracket_index: the index to check in
        :return: true if bracket legal, else false
        """
        return (close_bracket_index == len(expr) - 1 or InputValidator.is_operator(expr[close_bracket_index + 1])
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
                    (math_expr[operator_index + 1].isnumeric()
                     or math_expr[operator_index + 1] == "(" or math_expr[operator_index + 1] == "|"
                        or math_expr[operator_index] == "|" and math_expr[operator_index + 1] == "~")):
                if operator_index == 0:
                    return True
                elif InputValidator.is_operator(math_expr[operator_index - 1]):
                    return True
            return False

        else:
            if operator_index != 0 and (math_expr[operator_index - 1].isnumeric()
                                        or math_expr[operator_index - 1] == ")"
                                        or CreateOperator.get_operator(math_expr[operator_index - 1]).get_position() == 1):
                if operator_index == len(math_expr) - 1:
                    return True
                elif InputValidator.is_operator(math_expr[operator_index + 1]) or math_expr[operator_index + 1] == ")":
                    return True
            return False

    @staticmethod
    def is_amount_of_brackets_legal(math_expression: str) -> bool:
        """
        this function check is amount of ( is equals to amount of ) in a math expression
        :param math_expression: string to check if amount of bracket is legal
        :return: true if legal, else false
        """
        return math_expression.count("(") == math_expression.count(")")

    @staticmethod
    def validate_math_expression(math_expr: str):
        """
        this function finds if a string is valid with no math syntax error, if there are it raise syntax error
        :param math_expr: a string to find if is valid
        :return:
        """
        symbol_index = 0
        count_brackets = 0

        if not InputValidator.is_amount_of_brackets_legal(math_expr):
            raise SyntaxError("the amount of [(] and [)] is not the same!")

        for symbol in math_expr:
            if not InputValidator.is_valid_symbol(symbol):
                raise SyntaxError("Unrecognised symbol in your expression [{0}]")

            if symbol == "." and not InputValidator.is_point_legal(math_expr, symbol_index):
                raise SyntaxError("you used the point '.' symbol incorrectly in your expression")

            if symbol == "(":
                count_brackets += 1
                if not InputValidator.is_open_bracket_legal(math_expr, symbol_index):
                    raise SyntaxError("your syntax was wrong!!")

            if symbol == ")":
                count_brackets += -1
                if not InputValidator.is_close_bracket_legal(math_expr, symbol_index):
                    raise SyntaxError("your syntax was wrong!!")

            if count_brackets < 0:
                raise SyntaxError("your use of brackets was wrong!")

            if InputValidator.is_operator(symbol):
                operator = CreateOperator.get_operator(symbol)
                if (operator.get_number_of_operands() == 1
                        and not InputValidator.is_operator_unary_valid(symbol_index, math_expr)):
                    raise SyntaxError("you used the unary operator [{0}] in your expression in the wrong way".format(symbol))
            symbol_index += 1

