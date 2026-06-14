param(
  [switch]$NoBuild,
  [switch]$NoBridge,
  [switch]$NoOpen,
  [int]$WebPort = 8765
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$RuntimeDir = Join-Path $Root '.siteon-runtime'

function Resolve-CommandPath($Name) {
  $command = Get-Command $Name -ErrorAction SilentlyContinue
  if (-not $command) {
    throw "$Name command was not found. Install Node.js or add it to PATH."
  }
  return $command.Source
}

function Quote-Arg($Value) {
  $text = [string]$Value
  if ($text -match '[\s"]') {
    return '"' + ($text -replace '"', '\"') + '"'
  }
  return $text
}

function Test-HttpOk($Url) {
  try {
    $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 1
    return ($response.StatusCode -ge 200 -and $response.StatusCode -lt 300)
  } catch {
    return $false
  }
}

function Test-PortOpen($Port) {
  $client = [System.Net.Sockets.TcpClient]::new()
  try {
    $iar = $client.BeginConnect('127.0.0.1', $Port, $null, $null)
    if (-not $iar.AsyncWaitHandle.WaitOne(150)) { return $false }
    $client.EndConnect($iar)
    return $true
  } catch {
    return $false
  } finally {
    $client.Close()
  }
}

function Get-FreePort($StartPort) {
  for ($port = $StartPort; $port -le ($StartPort + 30); $port++) {
    if (-not (Test-PortOpen $port)) { return $port }
  }
  throw "No free local web port found from $StartPort to $($StartPort + 30)."
}

function Wait-HttpOk($Url, $Label) {
  for ($i = 0; $i -lt 40; $i++) {
    if (Test-HttpOk $Url) { return }
    Start-Sleep -Milliseconds 250
  }
  throw "$Label did not become ready: $Url"
}

function Start-HiddenNode($NodePath, $ScriptPath, $Arguments, $LogPrefix) {
  New-Item -ItemType Directory -Force -Path $RuntimeDir | Out-Null
  $stdout = Join-Path $RuntimeDir "$LogPrefix.out.log"
  $stderr = Join-Path $RuntimeDir "$LogPrefix.err.log"
  $allArgs = @((Quote-Arg $ScriptPath)) + $Arguments
  return Start-Process `
    -FilePath $NodePath `
    -ArgumentList ($allArgs -join ' ') `
    -WorkingDirectory $Root `
    -WindowStyle Hidden `
    -RedirectStandardOutput $stdout `
    -RedirectStandardError $stderr `
    -PassThru
}

Set-Location $Root
$node = Resolve-CommandPath 'node'

if (-not $NoBuild) {
  & $node (Join-Path $Root 'tools/build-builder.mjs')
}

if (-not $NoBridge) {
  $bridgeHealth = 'http://127.0.0.1:4627/health'
  if (-not (Test-HttpOk $bridgeHealth)) {
    Start-HiddenNode $node (Join-Path $Root 'tools/siteon-ai-cli-bridge.mjs') @() 'ai-bridge' | Out-Null
    Wait-HttpOk $bridgeHealth 'AI CLI bridge'
  }
}

$webHealth = "http://127.0.0.1:$WebPort/siteon-health"
if (-not (Test-HttpOk $webHealth)) {
  if (Test-PortOpen $WebPort) {
    $WebPort = Get-FreePort ($WebPort + 1)
    $webHealth = "http://127.0.0.1:$WebPort/siteon-health"
  }
  Start-HiddenNode $node (Join-Path $Root 'tools/siteon-static-server.mjs') @('--port', [string]$WebPort) 'web-server' | Out-Null
  Wait-HttpOk $webHealth 'SiteOn web server'
}

$builderUrl = "http://127.0.0.1:$WebPort/"

if (-not $NoOpen) {
  $chromeCandidates = @(
    @(
      "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
      "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
    ) | Where-Object { $_ -and (Test-Path $_) }
  )

  if ($chromeCandidates.Count -gt 0) {
    Start-Process -FilePath $chromeCandidates[0] -ArgumentList $builderUrl
  } else {
    Start-Process $builderUrl
  }
}

Write-Host "SiteOn builder is ready: $builderUrl"
Write-Host "AI CLI bridge: http://127.0.0.1:4627/health"
