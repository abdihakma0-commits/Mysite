#!/usr/bin/env bash
# Exit on error
set -o errexit

# Print Python version for debugging
python --version

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create static directory if it doesn't exist
mkdir -p static

# Clear old static files
rm -rf staticfiles
rm -f staticfiles.json

# Collect static files
python manage.py collectstatic --no-input --clear

# Apply database migrations
python manage.py migrate

echo "✅ Build completed successfully!"