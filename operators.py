from typing import List


class MathArithmeticError(ArithmeticError):
    """
    this is a class for an arithmetic error in a math expression
    """
    def __init__(self, msg: str):
        """
        this is a constructor for arithmetic error in a math expression
        :param msg: a message error to give
        """
        ArithmeticError.__init__(self, msg)
        self.msg = msg


class Operator:

    def __init__(self, priority: float, position: int, number_of_operands: int, symbol: str):
        """
        this is a constructor for a basic class representing an operator
        :param priority: the priority of the operator in math expression
        :param position: where is the operator positioned: 0 -between two operand,
        -1 - in the left of an operand, 1- in the right of am operand
        :param number_of_operands: number of operands this operator works on
        :param symbol: the character representing the operator
        """
        self.priority = priority
        self.position = position
        self.number_of_operands = number_of_operands
        self.symbol = symbol

    def get_priority(self) -> float:
        """
        get the priority of the operator
        :return: the int priority
        """
        return self.priority

    def get_position(self) -> int:
        """
        get the position of the operator
        :return: the int position
        """
        return self.position

    def get_number_of_operands(self) -> int:
        """
        get the number of operands this operator works on
        :return: the int number of operands
        """
        return self.number_of_operands

    def get_symbol(self) -> str:
        """
        get the symbol of the operator
        :return: the string symbol
        """
        return self.symbol

    def set_priority(self, priority: float):
        """
        set the priority of the operand
        :param priority: new priority
        :return: None
        """
        self.priority = priority

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get operands and execute the operator on them
        :param list_of_operands: list of operands in the expression
        :return: the number after the execution of the operator
        """
        pass


class Addition(Operator):
    def __init__(self):
        """
        this is a constructor for addition: +
        """
        Operator.__init__(self, 1, 0, 2, "+")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get two operands and add them
        :param list_of_operands: list of operands in the expression
        :return: the addition of the numbers
        """
        return list_of_operands[0] + list_of_operands[1]


class Subtraction(Operator):
    def __init__(self):
        """
        this is a constructor for subtraction: -
        """
        Operator.__init__(self, 1, 0, 2, "-")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get two operands and subtract them
        :param list_of_operands: list of operands in the expression
        :return: the subtraction of the numbers
        """
        return list_of_operands[0] - list_of_operands[1]


class Multiplication(Operator):
    def __init__(self):
        """
        this is a constructor for multiplication: *
        """
        Operator.__init__(self, 2, 0, 2, "*")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get two operands and multiply them
        :param list_of_operands: list of operands in the expression
        :return: the multiplication of the numbers
        """

        answer = list_of_operands[0] * list_of_operands[1]
        if answer == -0:
            answer = 0
        return answer


class Division(Operator):
    def __init__(self):
        """
        this is a constructor for division: /
        """
        Operator.__init__(self, 2, 0, 2, "/")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get two operands and dived them
        :param list_of_operands: list of operands in the expression
        :return: the division of the numbers
        """
        if list_of_operands[1] == 0:
            raise MathArithmeticError("an operand was divide by zero!")
        return list_of_operands[0] / list_of_operands[1]


class Exponentiation(Operator):
    def __init__(self):
        """
        this is a constructor for exponentiation: ^
        """
        Operator.__init__(self, 3, 0, 2, "^")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get two operands and execute exponentiation on them
        :param list_of_operands: list of operands in the expression
        :return: the number after the execution of the operator
        """
        answer = list_of_operands[0] ** list_of_operands[1]
        if isinstance(answer, complex):
            raise MathArithmeticError("you got a complex number!")
        return answer


class Average(Operator):
    def __init__(self):
        """
        this is a constructor for average: @
        """
        Operator.__init__(self, 5, 0, 2, "@")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get two operands and find the average of them
        :param list_of_operands: list of operands in the expression
        :return: the average of the numbers
        """
        return (list_of_operands[0] + list_of_operands[1]) / 2


class Maximum(Operator):
    def __init__(self):
        """
        this is a constructor for maximum: $
        """
        Operator.__init__(self, 5, 0, 2, "$")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get two operands and find the bigger one
        :param list_of_operands: list of operands in the expression
        :return: the bigger number
        """
        if list_of_operands[0] > list_of_operands[1]:
            return list_of_operands[0]
        return list_of_operands[1]


class Minimum(Operator):
    def __init__(self):
        """
        this is a constructor for minimum: &
        """
        Operator.__init__(self, 5, 0, 2, "&")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get two operands and find the smaller one
        :param list_of_operands: list of operands in the expression
        :return: the smaller number
        """
        if list_of_operands[0] < list_of_operands[1]:
            return list_of_operands[0]
        return list_of_operands[1]


class Modulo(Operator):
    def __init__(self):
        """
        this is a constructor for modulo: %
        """
        Operator.__init__(self, 4, 0, 2, "%")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get two operands and find the remnant after division
        :param list_of_operands: list of operands in the expression
        :return: the remnant after division
        """
        return list_of_operands[0] % list_of_operands[1]


class Negation(Operator):
    def __init__(self):
        """
        this is a constructor for negation: ~
        """
        Operator.__init__(self, 6, -1, 1, "~")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get operand and change its sign
        :param list_of_operands: list of operands in the expression
        :return: the operand with the opposite sign
        """
        answer = list_of_operands[0] * -1
        if answer == -0:
            answer = 0
        return answer


class Factorial(Operator):
    def __init__(self):
        """
        this is a constructor for factorial: !
        """
        Operator.__init__(self, 6, 1, 1, "!")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get operand and find its factorial
        :param list_of_operands: list of operands in the expression
        :return: the factorial of the operand
        """
        if int(list_of_operands[0]) != list_of_operands[0]:
            raise MathArithmeticError("you cant do factorial on a decimal number!")

        if int(list_of_operands[0]) < 0:
            raise MathArithmeticError("you cant do factorial on a negative number!")

        answer = 1
        for number in range(1, int(list_of_operands[0]) + 1):
            answer *= number
        return float(answer)


class OpenBracket(Operator):
    def __init__(self):
        """
        this is a constructor for open bracket: (
        """
        Operator.__init__(self, 0, 0, 0, "(")


class MinUnary(Operator):
    def __init__(self):
        """
        this is a constructor for minus unary: |
        """
        Operator.__init__(self, 2.5, -1, 1, "|")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get operand and change its sign
        :param list_of_operands: list of operands in the expression
        :return: the operand with the opposite sign
        """
        answer = list_of_operands[0] * -1
        if answer == -0:
            answer = 0
        return answer


class Hashtag(Operator):
    def __init__(self):
        """
        this is a constructor for hashtag unary: #
        """
        Operator.__init__(self, 6, 1, 1, "#")

    def calculate(self, list_of_operands: List[float]) -> float:
        """
        this function get operand and change its sign
        :param list_of_operands: list of operands in the expression
        :return: the operand with the opposite sign
        """
        if list_of_operands[0] < 0:
            raise MathArithmeticError("hashtag can't operate on negative number!")

        temp_list = str(list_of_operands[0])
        sum_of_digits = 0
        for digit in temp_list:
            if digit.isnumeric():
                sum_of_digits += int(digit)
        return sum_of_digits


class CreateOperator:
    """
    this class is used for creating an operator object by a given string operator
    """

    @staticmethod
    def get_operator(str_operator: str, ) -> Operator:
        operators_dict = {"+": Addition, "-": Subtraction, "*": Multiplication, "/": Division, "^": Exponentiation,
                          "@": Average, "$": Maximum, "&": Minimum, "%": Modulo, "~": Negation, "!": Factorial,
                          "(": OpenBracket, "|": MinUnary, "#": Hashtag}
        return operators_dict[str_operator]()

    @staticmethod
    def is_operator(operator: str) -> bool:
        """
        this function finds if a string is an operator
        :param operator: a string to find if is operator
        :return: true if operator, false otherwise
        """
        all_operators = ["+", "-", "*", "/", "^", "@", "$", "&", "%", "~", "!", "(", "|", "#"]
        return operator in all_operators

    @staticmethod
    def change_operator_priority(math_expr: List[str], symbol_index: int, operator_obj: Operator):
        symbol = math_expr[symbol_index]
        if symbol == "|":
            if (symbol_index != 0 and CreateOperator.is_operator(math_expr[symbol_index - 1])
                    and math_expr[symbol_index - 1] != "("):
                operator_obj.set_priority(7)
