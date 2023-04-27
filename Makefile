# https://www.gnu.org/software/make/manual/make.html
include .env.dev
export

include *.make

VERSION := $(shell cat VERSION)
PROJECT := $(shell basename $(CURDIR))

# PYTHON := /usr/bin/python3
# PYTHON := /media/mohsen/ssd500/compilers/py3_10_7/bin/python3.10
PYTHON := /home/mohsen/compiler/python/3.11.2/bin/python3.11

DOCKER := /usr/bin/docker 

PATH := $(VIRTUAL_ENV)/bin:$(PATH)
PY :=  $(VIRTUAL_ENV)/bin/python

ENV_NAME := $(shell $(PYTHON) -c 'import sys;print(f"env_{sys.platform}_{sys.version_info.major}.{sys.version_info.minor}")')

# SRC := pkg# just for this template
SRC := $(PROJECT)# for a python package
DIST := dist
BUILD := build
# PY_FILES = $(shell find $(SRC) -type f -name '*.py')
PY_FILES := $(shell find $(SRC) -type f -name '*.py' | grep -v '^.*\/test_.*\.py$$')
PY_FILES_TEST := $(shell find $(SRC) -type f -name 'test_*.py')

PYTHONPATH := $(SRC):$(PYTHONPATH)

ifeq ($(SSL), true)
PROTOCOL := HTTPS
else
PROTOCOL := HTTP
endif
URL := $(PROTOCOL)://$(HOST):$(PORT)

.PHONY: env test all dev clean dev pyserve gen-commands $(SRC) $(DIST) $(BUILD) py.make

.DEFAULT_GOAL := test

.ONESHELL:

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

env: .gitignore exclude.lst .dockerignore
		$(PYTHON) -m venv $(ENV_NAME)
		@echo $(ENV_NAME) >> .gitignore
		@echo $(ENV_NAME) >> exclude.lst
		@echo $(ENV_NAME) >> .dockerignore

check:
		$(PY) -m ensurepip --default-pip
		$(PY) -m pip install --upgrade pip setuptools wheel

test:
		@echo $(PATH)
		$(PY) --version
		$(PY) -m pip --version

pi: 
		$(PY) -m pip install $(filter-out $@,$(MAKECMDGOALS))
		$(PY) -m pip freeze > requirements.txt

piu:
		$(PY) -m pip install --upgrade $(filter-out $@,$(MAKECMDGOALS))
		$(PY) -m pip freeze > requirements.txt

pireq:
		make piu black isort pylint mypy

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


pkg-publish-test: .pypirc
		twine upload --config-file .pypirc -r testpypi dist/*  --verbose 


pkg-publish: .pypirc
		twine upload  dist/* --verbose  

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

pylint-dev:
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

script-upgrade:
		./scripts/upgrade_dependencies.sh


temp-rm:
		rm py.make

gen-commands: temp-rm
		$(foreach file,$(PY_FILES),$(shell echo "\n$(subst /,-,$(subst $(SRC)/,,$(basename $(file)))):\n\t\t$(PY) $(file)" >> py.make))
