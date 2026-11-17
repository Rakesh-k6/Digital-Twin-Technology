# CityLink - Start FastAPI Backend Server
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Starting CityLink Cyber-Physical Backend Server (FastAPI) " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$backendDir = Join-Path $scriptDir "..\backend"
Set-Location $backendDir

Write-Host "Checking python dependencies..." -ForegroundColor Yellow
python -m pip install fastapi uvicorn websockets pydantic numpy pandas networkx

Write-Host "`nLaunching FastAPI Server on http://localhost:8000 ..." -ForegroundColor Green
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
