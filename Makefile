ifeq ($(OS), Windows_NT)
	PYTHON=python
	PIP=pip
	DIR=Scripts
else
	PYTHON=python3
	PIP=pip3
	DIR=bin
endif

savetools.so : CTools/savetools.c
	gcc -fPIE -shared -o CTools/savetools.so CTools/savetools.c -Wall 
	$(PYTHON) -m virtualenv .

install : savetools.so
	$(PIP) install -r requirements.txt
