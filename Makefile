export PYTHONPATH=$PYTHONPATH:$(PWD)

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	find ./** -type f -name requirements.txt -execdir $(PWD)/venv/bin/pip install -Ur requirements.txt \;
	touch venv/bin/activate
