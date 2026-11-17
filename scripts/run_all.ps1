# CityLink - Unified Launcher Script
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   CITYLINK: Cyber-Physical Smart City Digital Twin " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$root = Join-Path $scriptDir ".."

# 1. Run quick verification test
Write-Host "`n[STEP 1/3] Running Backend Verification Test..." -ForegroundColor Yellow
python "$root\scripts\test_backend.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Backend tests reported an issue. Please verify environment." -ForegroundColor Red
    exit 1
}

# 2. Launch Backend in new window
Write-Host "`n[STEP 2/3] Launching FastAPI Backend on http://localhost:8000 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", "$root\scripts\start_backend.ps1"

# 3. Launch Dashboard in new window
Write-Host "`n[STEP 3/3] Launching React Monitoring Dashboard on http://localhost:3000 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", "$root\scripts\start_dashboard.ps1"

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "   All systems successfully initiated!" -ForegroundColor Cyan
Write-Host "   - REST API Docs:       http://localhost:8000/docs" -ForegroundColor White
Write-Host "   - Live WebSocket:      ws://localhost:8000/ws/live" -ForegroundColor White
Write-Host "   - React Dashboard:     http://localhost:3000" -ForegroundColor White
Write-Host "   - Unity 3D Project:    $root\unity\CityLinkUnity" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan
