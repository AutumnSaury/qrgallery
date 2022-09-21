import sys, os

# 用于关闭函数内print
class Silence:
    def __enter__(self):
        self._ostdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, _, __, ___):
        sys.stdout.close()
        sys.stdout = self._ostdout