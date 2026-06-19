$env:PYTHONIOENCODING='utf-8'
Write-Host "ThessCinema — εκκίνηση server..." -ForegroundColor Green

# Kill any stale server on port 8765
Get-Process -Name "python*" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -match "8765"
} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep 1

# Start server in background
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = "python"
$psi.Arguments = "-m uvicorn main:app --host 0.0.0.0 --port 8765"
$psi.WorkingDirectory = $PSScriptRoot
$psi.UseShellExecute = $false
$psi.CreateNoWindow = $true
$psi.EnvironmentVariables["PYTHONIOENCODING"] = "utf-8"
$p = [System.Diagnostics.Process]::Start($psi)
Start-Sleep 2

Write-Host "Server τρέχει στο http://localhost:8765" -ForegroundColor Cyan
Start-Process "http://localhost:8765"

Write-Host "Πάτησε Ctrl+C για τερματισμό" -ForegroundColor Gray

# Wait so window stays open
try {
    while ($true) { Start-Sleep 10 }
} finally {
    $p.Kill()
}
