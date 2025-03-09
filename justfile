project := file_stem(justfile_dir())
venv-name := ".venv"
venv-path := join(justfile_dir(), venv-name)
pip-cmd := shell('if [ -x "$(command -v uv)" ]; then echo "uv pip"; else echo "pip"; fi')

# ==============================================================================
# DJANGO RECIPES
# ==============================================================================

# Launch development server
runserver: check-venv postgres
    ./manage.py runserver

# Launch Django interactive shell
sh: check-venv postgres
    ./manage.py shell

alias mm := makemigrations
# Make Django migrations
makemigrations: check-venv postgres
    ./manage.py makemigrations
    
alias m := migrate
# Apply Django migrations
migrate: check-venv postgres
    ./manage.py migrate

alias c := check
# Check if Django project is correct
check: check-venv postgres
    ./manage.py check

# Add a new app and install it on settings.py
startapp app: check-venv postgres
    #!/usr/bin/env bash
    python manage.py startapp {{ app }}
    APP_CLASS={{ app }}
    APP_CONFIG="{{ app }}.apps.${APP_CLASS^}Config"
    perl -0pi -e "s/(INSTALLED_APPS *= *\[)(.*?)(\])/\1\2    '$APP_CONFIG',\n\3/smg" ./main/settings.py
    echo "✔ {{ app }} installed & added to settings.INSTALLED_APPS"

# ==============================================================================
# VIRTUALENV RECIPES
# ==============================================================================

# Create a Python virtualenv
create-venv:
    #!/usr/bin/env bash
    if [ ! -d {{ venv-name }} ]
    then
        if [ -x "$(command -v uv)" ]
        then
            uv venv --seed
        else
            python -m venv {{ venv-name }} --prompt {{ project }}
        fi
    fi

# Check if Python virtualenv is activated
[private]
[no-exit-message]
check-venv: create-venv
    #!/usr/bin/env bash
    if [ "$VIRTUAL_ENV" != "{{ venv-path }}" ]; then
        echo Project virtualenv: {{ venv-path }}
        echo Active virtualenv: $VIRTUAL_ENV
        echo
        echo You must activate the right virtualenv!
        exit 1
    fi

alias i := install-reqs
# Install project requirements
install-reqs: check-venv
    {{ pip-cmd }} install -r requirements.txt

# ==============================================================================
# DJANGO AUX RECIPES
# ==============================================================================

# Setup a Django project
setup: install-reqs && migrate create-su
    #!/usr/bin/env bash
    django-admin startproject main .
    sed -i -E "s/(TIME_ZONE).*/\1 = 'Atlantic\/Canary'/" ./main/settings.py
    echo "✔ Fixed TIME_ZONE='Atlantic/Canary' and LANGUAGE_CODE='es-es'"

# Create a superuser (or update it if already exists)
create-su username="admin" password="admin" email="admin@example.com": postgres
    #!/usr/bin/env bash
    ./manage.py shell -c '
    from django.contrib.auth.models import User
    user, _ = User.objects.get_or_create(username="{{ username }}")
    user.email = "{{ email }}"
    user.set_password("{{ password }}") 
    user.is_superuser = True
    user.is_staff = True
    user.save()
    ' 
    echo "✔ Created superuser → {{ username }}:{{ password }}"

# https://medium.com/@mustahibmajgaonkar/how-to-reset-django-migrations-6787b2a1e723
# https://stackoverflow.com/a/76300128
# Remove migrations and database. Reset DB artefacts.
[confirm("⚠️ All migrations and database will be removed. Continue? [yN]:")]
reset-db: postgres && create-su
    #!/usr/bin/env bash
    find . -path "*/migrations/*.py" ! -path "./.venv/*" ! -name "__init__.py" -delete
    find . -path "*/migrations/*.pyc" ! -path "./.venv/*" -delete
    psql << EOF
        DROP DATABASE peqes;
        CREATE DATABASE peqes;
        GRANT ALL PRIVILEGES ON DATABASE peqes TO peqes_user;
        \c peqes
        GRANT ALL ON SCHEMA public TO peqes_user;
    EOF
    ./manage.py makemigrations
    ./manage.py migrate
    echo

# Launch worker for Redis Queue (RQ)
rq: check-venv redis
    ./manage.py rqworker

# ==============================================================================
# MISC RECIPES
# ==============================================================================

# Deploy project to production
deploy:
    #!/usr/bin/env bash
    source .venv/bin/activate
    git pull
    pip install -r requirements.txt
    npm install
    python manage.py migrate
    python manage.py collectstatic --no-input
    supervisorctl restart peqes

# Enable testing with pytest inside VSCode
enable-vscode-pytest:
    #!/usr/bin/env bash
    mkdir -p .vscode
    cat << EOF > .vscode/settings.json
    {
      "python.testing.pytestArgs": ["tests"],
      "python.testing.unittestEnabled": false,
      "python.testing.pytestEnabled": true
    }
    EOF

# Start postgresql server
[private]
postgres:
    #!/usr/bin/env bash
    if [[ $(grep -i postgres $(find . -name settings.py)) ]]; then
        if   [[ $OSTYPE == "linux-gnu"* ]]; then
            pgrep -x postgres &> /dev/null || sudo service postgresql start
        elif [[ $OSTYPE == "darwin"* ]]; then
            pgrep -x postgres &> /dev/null || (open /Applications/Postgres.app && sleep 2)
        fi
    fi

# Start redis server
[private]
redis:
    #!/usr/bin/env bash
    if [[ $(grep -i redis $(find . -name settings.py)) ]]; then
        if   [[ $OSTYPE == "linux-gnu"* ]]; then
            pgrep -x redis &> /dev/null || sudo service redis start
        elif [[ $OSTYPE == "darwin"* ]]; then
            pgrep -x Redis &> /dev/null || (open /Applications/Redis.app && sleep 2)
        fi
    fi
