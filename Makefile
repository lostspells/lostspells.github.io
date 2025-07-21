.PHONY: build

prepare:
	python3 -m venv _plots/venv
	_plots/venv/bin/python -m pip install --upgrade pip
	_plots/venv/bin/python -m pip install -r _plots/requirements.txt
	bundle install

build:
	_plots/venv/bin/python _plots/bokeh_plot.py
	bundle exec jekyll build