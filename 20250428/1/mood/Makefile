.DEFAULT_GOAL := html

html:
	sphinx-build -b html docs/source docs/build/html

extract-strings:
	pybabel extract \
		-o server/locale/messages.pot \
		server/

init-ru:
	pybabel init \
		-i server/locale/messages.pot \
		-d server/locale \
		-l ru \
		-D messages

update-translations:
	pybabel update \
		-i server/locale/messages.pot \
		-d server/locale \
		-D messages

compile-translations:
	pybabel compile \
		-d server/locale \
		-D messages

i18n: extract-strings update-translations compile-translations

test: i18n
	pytest tests/

clean:
	python clean.py

.PHONY: html clean test i18n extract-strings init-ru update-translations compile-translations
