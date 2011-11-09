# tree.io makefile

# Alexander Berezovskiy <letoosh@gmail.com>

all: .ve

.ve:
		python manage.py update_ve
		./bin/patch

install:
		python manage.py installdb

clean:
		rm -fr .ve

