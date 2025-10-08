# Facebook Scraper Project Cleanup Script
# Removes all unimportant files and organizes the project structure

Write-Host "🧹 Facebook Scraper Project Cleanup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Navigate to script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "`n📂 Current directory: $(Get-Location)" -ForegroundColor Yellow

# Remove duplicate and backup files
Write-Host "`n🗑️  Removing duplicate and backup files..." -ForegroundColor Yellow
$FilesToRemove = @(
    "base copy.py",
    "organize_project_fixed.ps1", 
    "auto_cleanup.ps1",
    "auto_cleanup_fixed.ps1",
    "PROJECT_README.md"
)

foreach ($file in $FilesToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "   ✅ Removed: $file" -ForegroundColor Green
    }
}

# Remove any remaining Odoo/Docker files
Write-Host "`n🗑️  Removing Odoo and Docker remnants..." -ForegroundColor Yellow
$OdooDockerFiles = @(
    "ir_model_access.csv",
    "*.xml",
    "*odoo*",
    "*dashboard*", 
    "*docker*",
    "Dockerfile*",
    "docker-compose*",
    "Makefile"
)

foreach ($pattern in $OdooDockerFiles) {
    Get-ChildItem -Path . -Name $pattern -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {
        Remove-Item $_ -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "   ✅ Removed: $_" -ForegroundColor Green
    }
}

# Clean up cache and temporary files
Write-Host "`n🧹 Cleaning cache and temporary files..." -ForegroundColor Yellow
if (Test-Path "__pycache__") {
    Remove-Item "__pycache__" -Recurse -Force
    Write-Host "   ✅ Removed: __pycache__" -ForegroundColor Green
}

Get-ChildItem -Path . -Name "*.pyc" -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item $_ -Force
    Write-Host "   ✅ Removed: $_" -ForegroundColor Green
}

Get-ChildItem -Path . -Name "*.pyo" -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item $_ -Force  
    Write-Host "   ✅ Removed: $_" -ForegroundColor Green
}

# Clean up logs directory
Write-Host "`n📋 Cleaning logs directory..." -ForegroundColor Yellow
if (Test-Path "logs") {
    $logCount = (Get-ChildItem "logs" -ErrorAction SilentlyContinue | Measure-Object).Count
    if ($logCount -gt 0) {
        Remove-Item "logs\*" -Force -ErrorAction SilentlyContinue
        Write-Host "   ✅ Cleaned $logCount log files" -ForegroundColor Green
    }
} else {
    New-Item -ItemType Directory -Name "logs" -Force | Out-Null
    Write-Host "   ✅ Created logs directory" -ForegroundColor Green
}

# Clean up old data files (keep recent ones)
Write-Host "`n📊 Cleaning old data files..." -ForegroundColor Yellow
if (Test-Path "data") {
    # Remove files older than 7 days
    $oldFiles = Get-ChildItem "data\*.json" -ErrorAction SilentlyContinue | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)}
    $oldCount = ($oldFiles | Measure-Object).Count
    
    if ($oldCount -gt 0) {
        $oldFiles | Remove-Item -Force
        Write-Host "   ✅ Removed $oldCount old data files (>7 days)" -ForegroundColor Green
    }
    
    # Remove test files
    $testFiles = Get-ChildItem "data\test_*", "data\engagement_test_*" -ErrorAction SilentlyContinue
    $testCount = ($testFiles | Measure-Object).Count
    
    if ($testCount -gt 0) {
        $testFiles | Remove-Item -Force
        Write-Host "   ✅ Removed $testCount test files" -ForegroundColor Green
    }
    
    # Ensure cache directory exists
    if (!(Test-Path "data\cache")) {
        New-Item -ItemType Directory -Path "data\cache" -Force | Out-Null
        Write-Host "   ✅ Created data\cache directory" -ForegroundColor Green
    }
} else {
    New-Item -ItemType Directory -Name "data" -Force | Out-Null
    New-Item -ItemType Directory -Path "data\cache" -Force | Out-Null
    Write-Host "   ✅ Created data and cache directories" -ForegroundColor Green
}

# Remove large log files
Write-Host "`n📄 Removing large log files..." -ForegroundColor Yellow
$logFiles = Get-ChildItem "*.log" -ErrorAction SilentlyContinue
foreach ($logFile in $logFiles) {
    Remove-Item $logFile -Force
    Write-Host "   ✅ Removed: $($logFile.Name)" -ForegroundColor Green
}

# Ensure screenshots directory exists
if (!(Test-Path "screenshots")) {
    New-Item -ItemType Directory -Name "screenshots" -Force | Out-Null
    Write-Host "   ✅ Created screenshots directory" -ForegroundColor Green
}

# Remove empty directories
Write-Host "`n📁 Removing empty directories..." -ForegroundColor Yellow
Get-ChildItem -Directory -Recurse | Where-Object {
    (Get-ChildItem $_.FullName -Recurse -Force | Measure-Object).Count -eq 0
} | ForEach-Object {
    Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue
    Write-Host "   ✅ Removed empty directory: $($_.Name)" -ForegroundColor Green
}

# Create .gitignore if it doesn't exist
if (!(Test-Path ".gitignore")) {
    Write-Host "`n📝 Creating .gitignore file..." -ForegroundColor Yellow
    @"
# Environment variables
.env

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Virtual environment
venv/
env/

# Data and logs
data/*.json
logs/*.log
facebook_scraper.log

# Screenshots
screenshots/*.png
screenshots/*.jpg

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "   ✅ Created .gitignore file" -ForegroundColor Green
}

Write-Host "`n✨ Cleanup completed successfully!" -ForegroundColor Green
Write-Host "`n📁 Final Project Structure:" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan

# Show final clean structure
Get-ChildItem -Name | Sort-Object | ForEach-Object {
    if (Test-Path $_ -PathType Container) {
        $itemCount = (Get-ChildItem $_ -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host "📁 $_/ ($itemCount items)" -ForegroundColor Blue
    } else {
        $size = [math]::Round((Get-Item $_).Length / 1KB, 1)
        Write-Host "📄 $_ ($size KB)" -ForegroundColor White
    }
}

Write-Host "`n🎉 Your Facebook scraper project is now clean and organized!" -ForegroundColor Green
Write-Host "📖 Check the new README.md for updated documentation." -ForegroundColor Yellow
