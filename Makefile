ifeq ($(OS), Windows_NT)
	PYTHON=python
	PIP=pip
	DIR=Scripts
else
	PYTHON=python3
	PIP=pip3
	DIR=bin
endif

savetools.so : Package/CTools/savetools.c
	gcc -fPIE -shared -o Package/CTools/savetools.so Package/CTools/savetools.c -Wall 
	$(PYTHON) -m venv .

install :
	$(PIP) install -r requirements.txt
