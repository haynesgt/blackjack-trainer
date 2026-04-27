param(
    [string]$Service = "blackjack-trainer",
    [string]$Region = "us-central1",
    [string]$Project = "",
    [switch]$NoAllowUnauthenticated
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    throw "gcloud CLI is required. Install it and run 'gcloud auth login' first."
}

$projectArgs = @()
if ($Project) {
    $projectArgs = @("--project", $Project)
}

$authArgs = @("--allow-unauthenticated")
if ($NoAllowUnauthenticated) {
    $authArgs = @("--no-allow-unauthenticated")
}

Write-Host "Deploying '$Service' to Cloud Run in region '$Region'..."

& gcloud run deploy $Service `
    --source . `
    --platform managed `
    --region $Region `
    @projectArgs `
    @authArgs
