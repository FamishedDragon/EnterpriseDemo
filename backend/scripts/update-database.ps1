# Stop the script if a command fails.
$ErrorActionPreference = "Stop"

Write-Host "========================================"
Write-Host "      Database Migration Tool"
Write-Host "========================================"
Write-Host ""

# Ensure the script is running from the backend directory.
$backendDirectory = Split-Path -Parent $PSScriptRoot
Set-Location $backendDirectory

# Prompt for the migration message.
do {
    $migrationMessage = Read-Host "Enter migration message"

    if ([string]::IsNullOrWhiteSpace($migrationMessage)) {
        Write-Host "Migration message cannot be empty." -ForegroundColor Yellow
    }
} while ([string]::IsNullOrWhiteSpace($migrationMessage))

Write-Host ""
Write-Host "Creating migration: $migrationMessage" -ForegroundColor Cyan
Write-Host ""

# Find migration files before generating the new migration.
$versionsDirectory = Join-Path $backendDirectory "alembic\versions"

$filesBefore = @(
    Get-ChildItem -Path $versionsDirectory -Filter "*.py" -File |
    Select-Object -ExpandProperty FullName
)

# Generate the migration.
uv run alembic revision --autogenerate -m $migrationMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Migration generation failed." -ForegroundColor Red
    exit 1
}

# Find the newly generated migration file.
$filesAfter = @(
    Get-ChildItem -Path $versionsDirectory -Filter "*.py" -File |
    Select-Object -ExpandProperty FullName
)

$newFiles = $filesAfter | Where-Object {
    $_ -notin $filesBefore
}

if ($newFiles.Count -ne 1) {
    Write-Host ""
    Write-Host "Could not identify exactly one new migration file." -ForegroundColor Red
    Write-Host "Inspect the alembic/versions directory manually."
    exit 1
}

$migrationFile = $newFiles[0]

Write-Host ""
Write-Host "========================================"
Write-Host " Generated Migration"
Write-Host "========================================"
Write-Host ""

# Display the generated migration for inspection.
Get-Content -Path $migrationFile

Write-Host ""
Write-Host "========================================"
Write-Host " Migration Review"
Write-Host "========================================"
Write-Host ""

Write-Host "Migration file:"
Write-Host $migrationFile
Write-Host ""

$confirmation = Read-Host "Apply this migration with 'alembic upgrade head'? (Y/N)"

if ($confirmation -notmatch "^[Yy]$") {
    Write-Host ""
    Write-Host "Migration was generated but NOT applied." -ForegroundColor Yellow
    Write-Host "Review or edit the migration file before applying it."
    exit 0
}

Write-Host ""
Write-Host "Applying migration..." -ForegroundColor Cyan
Write-Host ""

uv run alembic upgrade head

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Migration application failed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Migration applied successfully." -ForegroundColor Green