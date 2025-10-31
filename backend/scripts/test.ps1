Param(
  [string]$ApiBaseUrl = "http://localhost:8000/api/v1"
)

Write-Host "Running backend tests against $ApiBaseUrl" -ForegroundColor Cyan

$env:API_BASE_URL = $ApiBaseUrl
pytest -q

if ($LASTEXITCODE -eq 0) {
  Write-Host "All tests passed" -ForegroundColor Green
} else {
  Write-Host "Tests failed with exit code $LASTEXITCODE" -ForegroundColor Red
  exit $LASTEXITCODE
}