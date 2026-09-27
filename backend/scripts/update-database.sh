#!/usr/bin/env bash

set -euo pipefail

echo "========================================"
echo "      Database Migration Tool"
echo "========================================"
echo

# Move to the backend directory.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

cd "$BACKEND_DIR"

# Prompt for a migration message.
while true; do
    read -r -p "Enter migration message: " MIGRATION_MESSAGE

    if [[ -n "${MIGRATION_MESSAGE// }" ]]; then
        break
    fi

    echo "Migration message cannot be empty."
done

echo
echo "Creating migration: $MIGRATION_MESSAGE"
echo

VERSIONS_DIR="alembic/versions"

# Capture existing migration files.
BEFORE_FILES="$(find "$VERSIONS_DIR" -maxdepth 1 -type f -name "*.py" -print | sort)"

# Generate the migration.
uv run alembic revision --autogenerate -m "$MIGRATION_MESSAGE"

# Capture migration files after generation.
AFTER_FILES="$(find "$VERSIONS_DIR" -maxdepth 1 -type f -name "*.py" -print | sort)"

# Identify the newly created file.
NEW_FILES="$(comm -13 \
    <(printf '%s\n' "$BEFORE_FILES") \
    <(printf '%s\n' "$AFTER_FILES"))"

NEW_FILE_COUNT="$(printf '%s\n' "$NEW_FILES" | sed '/^$/d' | wc -l)"

if [[ "$NEW_FILE_COUNT" -ne 1 ]]; then
    echo
    echo "Could not identify exactly one new migration file."
    echo "Inspect the alembic/versions directory manually."
    exit 1
fi

MIGRATION_FILE="$NEW_FILES"

echo
echo "========================================"
echo " Generated Migration"
echo "========================================"
echo

cat "$MIGRATION_FILE"

echo
echo "========================================"
echo " Migration Review"
echo "========================================"
echo

echo "Migration file: $MIGRATION_FILE"
echo

read -r -p "Apply this migration with 'alembic upgrade head'? (Y/N): " CONFIRMATION

if [[ ! "$CONFIRMATION" =~ ^[Yy]$ ]]; then
    echo
    echo "Migration was generated but NOT applied."
    echo "Review or edit the migration file before applying it."
    exit 0
fi

echo
echo "Applying migration..."
echo

uv run alembic upgrade head

echo
echo "Migration applied successfully."