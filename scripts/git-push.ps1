# git push via local Clash proxy (port 7890)
# Usage: .\scripts\git-push.ps1
#        .\scripts\git-push.ps1 origin master
param(
    [string]$Remote = "origin",
    [string]$Branch = ""
)

$Proxy = "http://127.0.0.1:7890"
$Socks = "socks5://127.0.0.1:7890"

if (-not $Branch) {
    $Branch = (git rev-parse --abbrev-ref HEAD).Trim()
}

function Invoke-GitPush {
    param([string[]]$ExtraArgs)
    & git @ExtraArgs push $Remote $Branch
    return $LASTEXITCODE
}

Write-Host ">> git push $Remote $Branch"

# 1) schannel + HTTP proxy（与 curl 一致，Windows 优先）
$env:HTTP_PROXY = $Proxy
$env:HTTPS_PROXY = $Proxy
$code = Invoke-GitPush @(
    "-c", "http.sslBackend=schannel",
    "-c", "http.proxy=$Proxy",
    "-c", "https.proxy=$Proxy",
    "-c", "http.version=HTTP/1.1"
)
if ($code -eq 0) { Write-Host "Push OK."; exit 0 }

Write-Host ">> retry: socks5 7890"
$code = Invoke-GitPush @(
    "-c", "http.sslBackend=schannel",
    "-c", "http.proxy=$Socks",
    "-c", "https.proxy=$Socks"
)
if ($code -eq 0) { Write-Host "Push OK."; exit 0 }

Write-Host ">> retry: socks5 7891"
$Socks791 = "socks5://127.0.0.1:7891"
$code = Invoke-GitPush @(
    "-c", "http.sslBackend=schannel",
    "-c", "http.proxy=$Socks791",
    "-c", "https.proxy=$Socks791"
)
if ($code -eq 0) { Write-Host "Push OK."; exit 0 }

Write-Host "Push failed. Try: Clash TUN on + unset git proxy, or use SSH (see below)."
exit 1
