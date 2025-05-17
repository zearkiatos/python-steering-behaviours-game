activate:
	if pyenv virtualenvs --bare | grep -q "localenv"; then \
        echo "Python 🐍 environment was activated"; \
    else \
        echo "The folder environment doesn't exist"; \
		pyenv virtualenv 3.11.7 localenv \
        echo "The environment folder was created and the python 🐍 environment was activated"; \
    fi
	pyenv local localenv
	
run:
	python3 main.py

install:
	pip3 install -r requirements.txt