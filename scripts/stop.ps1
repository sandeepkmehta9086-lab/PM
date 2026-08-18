$ErrorActionPreference = "Stop"

Set-Location "$(Split-Path -Parent $MyInvocation.MyCommand.Path)\.."
Write-Host "Stopping backend via Docker Compose..."
docker-compose down