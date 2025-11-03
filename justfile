project := file_stem(justfile_dir())

# ==============================================================================
# DJANGO RECIPES
# ==============================================================================

# Launch development server
[macos]
run: postgres
    uv run ./manage.py runserver

# Run program in production mode
[linux]
run: postgres
    uv run gunicorn -b unix:/tmp/peqes.sock main.wsgi:application

# Launch Django interactive shell
sh: postgres
    uv run ./manage.py shell

alias mm := makemigrations
# Make Django migrations
makemigrations: postgres
    uv run ./manage.py makemigrations
    
alias m := migrate
# Apply Django migrations
migrate: postgres
    uv run ./manage.py migrate

alias c := check
# Check if Django project is correct
check: postgres
    uv run ./manage.py check

# Add a new app and install it on settings.py
startapp app: postgres
    #!/usr/bin/env bash
    uv run ./manage.py startapp {{ app }}
    APP_CLASS={{ app }}
    APP_CONFIG="{{ app }}.apps.${APP_CLASS^}Config"
    perl -0pi -e "s/(INSTALLED_APPS *= *\[)(.*?)(\])/\1\2    '$APP_CONFIG',\n\3/smg" ./main/settings.py
    echo "✔ {{ app }} installed & added to settings.INSTALLED_APPS"

# ==============================================================================
# UV RECIPES
# ==============================================================================

# Sync uv
[macos]
sync:
    uv sync --no-group prod

# Sync uv
[linux]
sync:
    uv sync --no-dev --group prod

# ==============================================================================
# DJANGO AUX RECIPES
# ==============================================================================

# Setup a Django project
setup: sync && migrate create-su
    #!/usr/bin/env bash
    django-admin startproject main .
    sed -i -E "s/(TIME_ZONE).*/\1 = 'Atlantic\/Canary'/" ./main/settings.py
    echo "✔ Fixed TIME_ZONE='Atlantic/Canary' and LANGUAGE_CODE='es-es'"

# Create a superuser (or update it if already exists)
create-su username="admin" password="admin" email="admin@example.com": postgres
    #!/usr/bin/env bash
    uv run ./manage.py shell -c '
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
    uv run ./manage.py makemigrations
    uv run ./manage.py migrate
    echo

# Launch worker for Redis Queue (RQ)
rq: redis
    uv run ./manage.py rqworker

# ==============================================================================
# MISC RECIPES
# ==============================================================================

# Deploy project to production
deploy:
    #!/usr/bin/env bash
    git pull
    just sync
    npm install
    uv run python manage.py migrate
    uv run python manage.py collectstatic --no-input
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

# Generate random secret key
[group('production')]
secret-key:
    #!/usr/bin/env bash
    uv run manage.py shell -v0 -c '
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    '
