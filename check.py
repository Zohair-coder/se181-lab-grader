import re
import colorama


class Homework:
    def __init__(self, txtfile):
        colorama.init(autoreset=True)
        with open(txtfile, "r") as f:
            self.answer = f.read()
        self.tokens = self.answer.split()
        self.total_marks = 10
        self.function_definitions = self.get_function_definitions()

    def get_function_definitions(self):
        regex = (
            r"(?:public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(?:\w+) *\([^\)]*\) *(?:\{?|[^;])\n")
        function_definitions = re.findall(
            regex, self.answer, re.MULTILINE)
        return function_definitions

    def check_all(self):
        points_to_deduct = 0
        print()
        if not self.is_lowercase_function_definition():
            print("-2: Check if the function definitions are lowercase")
            points_to_deduct += 2

        if self.is_test_in_function_definition():
            print("-2: Check if test is in function definition")
            points_to_deduct += 2

        if not self.is_at_test_before_each_test():
            print("-1: Check if @Test is before each test")
            if self.total_marks - points_to_deduct > 1:
                points_to_deduct += 1

        if self.is_array_equals_in_answer():
            print("-1: Check if you forgot to remove the array equals method")
            points_to_deduct += 1

        if not self.is_import_assertion_present():
            print("Not importing asserts")
            points_to_deduct = 9

        print()

        points_scored = self.total_marks - points_to_deduct

        if points_scored != self.total_marks:
            print(colorama.Fore.RED +
                  "You scored {}/{}".format(points_scored, self.total_marks))
        else:
            print(colorama.Fore.GREEN +
                  "You scored {}/{}".format(points_scored, self.total_marks))
        print()

    def is_lowercase_function_definition(self):
        for function in self.function_definitions:
            if "setup" in function.lower():
                continue
            if function.lower() != function:
                return False
        return True

    def is_test_in_function_definition(self):
        for function in self.function_definitions:
            if "test" in function.lower():
                return True
        return False

    def is_at_test_before_each_test(self):
        regex = (
            r"@(Test|BeforeEach)\s+(?:public|protected|private|static|\s) +[\w\<\>\[\]]+\s+(?:\w+) *\([^\)]*\) *(?:\{?|[^;])\n")
        at_function_definitions = re.findall(
            regex, self.answer, re.MULTILINE)
        if len(at_function_definitions) != len(self.function_definitions):
            return False
        return True

    def is_array_equals_in_answer(self):
        regex = r"array_?equals\("
        if re.search(regex, self.answer, re.IGNORECASE):
            return True
        return False

    def is_import_assertion_present(self):
        regex = r"import[\sA-Za-z\.]+Assert"
        if re.search(regex, self.answer):
            return True
        return False


if __name__ == "__main__":
    hw1 = Homework("answer.txt")
    hw1.check_all()
