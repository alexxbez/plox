from scanner import *
from token import *

class Lox: 
    had_error = False
    def __init__(self):
        pass

    def run_file(self, file: str):
        with open(file) as f:
            content = f.read() 
            self.run(content)

            if Lox.had_error:
                exit(65)


    def run_prompt(self):
        while True:
            print("> ", flush=True, end="")
            try:
                content = input()
                self.run(content)
                Lox.had_error = False
            except EOFError:
                break

    def run(self, source: str): 
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        # print tokens
        for token in tokens:
            print(f"{token}")

    @staticmethod
    def error(line: int, message: str):
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        Lox.had_error = True
