# Heroku Deployment Preparation Script
# Run this script to prepare your ATM system for Heroku deployment

Write-Host "🚀 Preparing ATM System for Heroku Deployment..." -ForegroundColor Green

# Check if required files exist
$requiredFiles = @("app.py", "requirements.txt", "Procfile")
$missingFiles = @()

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "❌ Missing required files: $($missingFiles -join ', ')" -ForegroundColor Red
    exit 1
}

Write-Host "✅ All required files found!" -ForegroundColor Green

# Check if Git is installed
try {
    $gitVersion = git --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Git found!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Git not found" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Git not found" -ForegroundColor Yellow
}

# Check if Heroku CLI is installed
try {
    $herokuVersion = heroku --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Heroku CLI found!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Heroku CLI not found" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Heroku CLI not found" -ForegroundColor Yellow
}

# Display next steps
Write-Host "`n🚀 Quick Start for Heroku:" -ForegroundColor Cyan
Write-Host "1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli" -ForegroundColor White
Write-Host "2. Login: heroku login" -ForegroundColor White
Write-Host "3. Initialize git: git init" -ForegroundColor White
Write-Host "4. Add files: git add ." -ForegroundColor White
Write-Host "5. Commit: git commit -m 'Initial commit'" -ForegroundColor White
Write-Host "6. Create app: heroku create atm-system-app" -ForegroundColor White
Write-Host "7. Deploy: git push heroku main" -ForegroundColor White
Write-Host "8. Open app: heroku open" -ForegroundColor White

Write-Host "`n📖 For detailed instructions, see: HEROKU_DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host "🔗 Quick start: https://devcenter.heroku.com/" -ForegroundColor Cyan

Write-Host "`n✅ Project ready for Heroku deployment!" -ForegroundColor Green
