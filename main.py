import sys
from lox import Lox

def main():
    lox = Lox()

    if len(sys.argv) > 2:
        print("Usage: plox [script]")
        exit(64)
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()



if __name__ == "__main__":
    main()
