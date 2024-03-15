## installation OS
sudo apt install pipx

## installation PiP
pipx install poetry

## installation Official
curl -sSL https://install.python-poetry.org | python3 -

curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -

poetry completions bash >> ~/.bash_completion

poetry config virtualenvs.create false --local
------------------------------------------------
## Install project
poetry install

## see poetry configuration
poetry config --list

## update configuration
poetry config virtualenvs.path /path/to/cache/directory/virtualenvs
poetry config virtualenvs.create false --local

poetry config installer.max-workers = 4




-----------------------------------------------
git init
poetry init

poetry self add poetry-multiproject-plugin
poetry self add poetry-polylith-plugin

# thirdparty library
poetry add 
poetry poly check --directory projects/my-project

## managing environments
# Simple Python version management
curl https://pyenv.run | bash

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc

pyenv install --list
# install specific
pyenv install 3.11.7
# set specific version
pyenv global 3.8.3


# install specific python version
pyenv install 3.9.8

pyenv local 3.9.8  # Activate Python 3.9 for the current project
poetry install


# create workspace
poetry poly create workspace --name my_namespace --theme loose

# create virtualenv
poetry install

# create component
poetry poly create component --name parser

# run test
poetry run pytest

## Synchronizing dependencies
poetry install --sync

The --sync option can be combined with any dependency groups related options to synchronize the environment with specific groups. Note that extras are separate. Any extras not selected for install are always removed, regardless of --sync

```
poetry install --without dev --sync
poetry install --with docs --sync
poetry install --only dev
```

Layering optional groups
When you omit the --sync option, you can install any subset of optional groups without removing those that are already installed. This is very useful, for example, in multi-stage Docker builds, where you run poetry install multiple times in different build stages.

## compiple code
poetry install --compile

poetry install --extras "mysql pgsql"
poetry install -E mysql -E pgsql
poetry install --all-extras

