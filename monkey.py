import _Repl.repl as repl
import _Repl.exec as exec
import sys

def main():
    if len(sys.argv) == 1:
        repl.start()
    else:
        exec.start(sys.argv[1])

if __name__ == "__main__":
    main()