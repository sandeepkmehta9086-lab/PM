$ErrorActionPreference = "Stop"

Set-Location "$(Split-Path -Parent $MyInvocation.MyCommand.Path)\.."
Write-Host "Starting backend via Docker Compose..."
docker-compose up --build