#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install system dependencies for Pillow (only on Render)
if [ "$RENDER" = "true" ]; then
    apt-get update && apt-get install -y \
        libjpeg-dev \
        zlib1g-dev \
        libpng-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libopenjp2-7-dev \
        libtiff5-dev
fi

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate