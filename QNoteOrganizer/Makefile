UIFILES := $(wildcard *.ui)
PYFILES := $(UIFILES:.ui=.py)
PYUIC = python /usr/lib/python2.7/dist-packages/PyQt4/uic/pyuic.py

all: $(PYFILES)

%.py: %.ui
	$(PYUIC) $< --output $@
