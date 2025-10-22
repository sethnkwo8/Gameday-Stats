#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Load your data.json automatically (ignore errors if data already exists)
if [ -f "data.json" ]; then
    echo "Loading initial data from data.json..."
    python manage.py loaddata data.json || echo "⚠️  Skipped loading data (might already exist)"
else
    echo "⚠️  No data.json file found — skipping data load"
fi