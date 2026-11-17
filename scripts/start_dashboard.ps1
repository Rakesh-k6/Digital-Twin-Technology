# CityLink - Start React Interactive Dashboard
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Starting CityLink React Monitoring Dashboard " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$dashboardDir = Join-Path $scriptDir "..\dashboard"
Set-Location $dashboardDir

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dashboard npm dependencies..." -ForegroundColor Yellow
    npm install
}

Write-Host "`nLaunching Vite React Dev Server on http://localhost:3000 ..." -ForegroundColor Green
npm run dev
