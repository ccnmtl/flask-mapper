export PIPENV_VENV_IN_PROJECT = true
VE ?= ./.venv
PY_SENTINAL ?= $(VE)/sentinal
PIPFILE ?= Pipfile
PY_VERSION ?= 3.6
TOPLEVEL ?= flask_mapper.py
export FLASK_APP = flask_mapper/flask_mapper/$(TOPLEVEL)

$(PY_SENTINAL): $(PIPFILE) $(VE) 
	rm -rf $(VE)
	pipenv install
	touch $@

$(VE):
	pipenv --python $(PY_VERSION)

bash: $(PY_SENTINAL)
	pipenv shell

python: $(PY_SENITNAL)
	pipenv run python

shell: $(PY_SENTINAL)
	pipenv run flask shell

runserver: $(PY_SENTINAL)
	pipenv run flask run

runserver-external: $(PY_SENTINAL)
	pipenv run flask run --host=0.0.0.0

credentials:
	pipenv run python flask_mapper/flask_mapper/sheets.py

clean:
	rm -rf $(VE)

.PHONY: clean shell init
