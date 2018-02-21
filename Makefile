export PIPENV_VENV_IN_PROJECT = true
VE ?= ./.venv
PY_SENTINAL ?= $(VE)/sentinal
PIPFILE ?= Pipfile
PY_VERSION ?= 3.6

$(PY_SENTINAL): $(PIPFILE) $(VE) 
	rm -rf $(VE)
	pipenv install
	touch $@

$(VE):
	pipenv --python $(PY_VERSION)

shell: $(PY_SENTINAL)
	pipenv shell

clean:
	rm -rf $(VE)

.PHONY: clean shell init
