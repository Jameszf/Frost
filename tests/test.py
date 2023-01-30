import unittest


if __name__ == "__main__":
    result = unittest.TestResult()
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner()
    suite = loader.discover("./")
    runner.run(suite)
