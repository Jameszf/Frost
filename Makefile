
main:
	-mypy frost/main.py
	python3 -m frost.main

test:
	python3 -m tests.test

typecheck:
	mypy frost/main.py
