SHELL := /bin/bash

clean:
	rm -rf venv
	find -iname "*.pyc" -delete

init:
	pip3 install -U virtualenv

venv: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip3 install -Ur requirements.txt
	touch venv/bin/activate

follow:
	. venv/bin/activate; venv/bin/python do.py --username $(INSTAGRAM_USERNAME) --password $(INSTAGRAM_PASSWORD) --file $(INSTAGRAM_USERNAME).json --tag $(INSTAGRAM_TAG) --no $(INSTAGRAM_NO)

unfollow:
	. venv/bin/activate; venv/bin/python do.py --username $(INSTAGRAM_USERNAME) --password $(INSTAGRAM_PASSWORD)  --file $(INSTAGRAM_USERNAME).json --unfollow --days $(INSTAGRAM_DAYS)
