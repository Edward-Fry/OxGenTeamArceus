make_venv:
	python3 -m venv venv

install:
	pip install -r requirements.txt

server:
	uvicorn main:app --reload