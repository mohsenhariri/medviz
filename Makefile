# https://www.gnu.org/software/make/manual/make.html

PYTHON := /home/mohsen/compiler/python/3.11.2/bin/python3.11
DOCKER := /usr/bin/docker 

PATH := $(VIRTUAL_ENV)/bin:$(PATH)
PY :=  $(VIRTUAL_ENV)/bin/python


include .env.dev
export

SRC := pkg
DIST := dist
BUILD := build

PYTHONPATH := $(SRC):$(PYTHONPATH)


.PHONY: env test all dev clean dev pyserve $(SRC) $(DIST) $(BUILD)
.DEFAULT_GOAL := test
.ONESHELL:

ifeq ($(SSL), true)
PROTOCOL := HTTPS
else
PROTOCOL := HTTP
endif
URL := $(PROTOCOL)://$(HOST):$(PORT)

%: # https://www.gnu.org/software/make/manual/make.html#Automatic-Variables 
		@:
		
cert: # HTTPS server
		if [ ! -d "./certs" ]; then mkdir ./certs; fi
		if [ -f "./certs/openssl.conf" ] ; then \
		openssl req -x509 -new -config ./certs/openssl.conf -out ./certs/cert.pem -keyout ./certs/key.pem ;  else \
		openssl req -x509 -nodes -newkey rsa:4096 -out ./certs/cert.pem -keyout ./certs/key.pem -sha256 -days 365 ;fi

docker-up:
		$(DOCKER) compose -p $(PROJECT) --env-file ./config/.env.docker -f ./config/compose.yaml up -d

docker-down:
		$(DOCKER) compose -p $(PROJECT) -f ./config/compose.yaml down

docker-build:
		$(DOCKER) build -t $(USER)/$(PROJECT):$(VERSION) .

docker-run:
		 $(DOCKER) container run --name $(PROJECT) -it  $(USER)/$(PROJECT):$(VERSION) /bin/bash

clean:
		rm -rf ./$(DIST)/* ./$(BUILD)/*

clcache: 
		rm -r ./__pycache__

env: 
		$(PYTHON) -m venv env

check:
		$(PY) -m ensurepip --default-pip
		$(PY) -m pip install --upgrade pip setuptools wheel

test:
		echo $(PATH)
		$(PY) --version
		$(PY) -m pip --version

test-os:
		$(PY) -c 'import sys;print(sys.platform)'

pi: 
		$(PY) -m pip install $(filter-out $@,$(MAKECMDGOALS))
		$(PY) -m pip freeze > requirements.txt

piu:
		$(PY) -m pip install --upgrade $(filter-out $@,$(MAKECMDGOALS))
		$(PY) -m pip freeze > requirements.txt

pia: requirements.txt
		$(PY) -m pip install -r requirements.txt


pkg-build: clean
		$(PY) -m pip install --upgrade build
		$(PY) -m build

pkg-install-editable:
		$(PY) -m pip install -e .

pkg-install:
		$(PY) -m pip install .

pkg-check:
		$(PY) -m pip install --upgrade twine
		twine check dist/*

pkg-publish-test:
		twine upload --config-file .pypirc.test -r testpypi dist/*  --verbose 

pkg-publish:
		twine upload --config-file .pypirc dist/* --verbose  

pkg-flit-init:
		$(PY) -m pip install --upgrade flit
		if [ -f "pyproject.toml" ] ; then mv pyproject.toml pyproject.backup ;  fi
		flit init

pkg-flit-build:
		flit build

# pkg-flit-check:
# 		flit install 

pkg-flit-publish-test:
		flit publish --repository testpypi

pkg-flit-publish:
		flit publish

pkg-poetry-init:
		if [ ! -d "./.poetry" ]; then mkdir ./poetry; fi
		wget -P ./.poetry https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py
		export POETRY_HOME=./.poetry && python ./.poetry/get-poetry.py --no-modify-path
		if [ -f "pyproject.toml" ] ; then mv pyproject.toml pyproject.backup ;  fi
		./.poetry/bin/poetry init

pkg-poetry-build:
		poetry build

pkg-poetry-publish-test:
		poetry publish --repository testpypi

pkg-poetry-publish:
		poetry publish

pylint:
		pylint --rcfile .pylintrc.dev $(SRC)

pylint-prod:
		pylint --rcfile .pylintrc.prod $(SRC)

format:
		black $(SRC)

sort:
		isort $(SRC)
		
type:
		mypy

type-prod:
		mypy --config-file .mypy.ini.prod

g-commit: format type pylint
		git commit -m "$(filter-out $@,$(MAKECMDGOALS))"

g-log:
		git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

unittest:
		$(PY) -m unittest $(SRC)/test_*.py


script-upgrade:
		./scripts/upgrade_dependencies.sh
