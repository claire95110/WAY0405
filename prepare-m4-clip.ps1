#Requires -Version 5.1
<#
.SYNOPSIS
  Clip BV1mmXQBdEMK ~24s-42s (18s), optional Catbox upload and patch index.html.
  Run on your PC with network (ffmpeg required; yt-dlp optional for URL mode).

.EXAMPLE
  .\prepare-m4-clip.ps1 -InputVideo "D:\downloads\full.mp4"
.EXAMPLE
  .\prepare-m4-clip.ps1 -InputVideo "D:\full.mp4" -UploadCatbox -PatchIndexHtml
#>
param(
  [string] $InputVideo,
  [switch] $UploadCatbox,
  [switch] $PatchIndexHtml,
  [string] $UserHash = "",
  [string] $BilibiliUrl = "https://www.bilibili.com/video/BV1mmXQBdEMK/"
)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$assetsPath = Join-Path $root "assets"
if (-not (Test-Path -LiteralPath $assetsPath)) { throw "Assets folder not found: $assetsPath" }
$assetsDir = Get-Item -LiteralPath $assetsPath
$outFile = Join-Path $assetsDir.FullName "BV1mmXQBdEMK-24-42.mp4"

function Test-Cmd($name) {
  return [bool](Get-Command $name -ErrorAction SilentlyContinue)
}

if ($InputVideo) {
  if (-not (Test-Path -LiteralPath $InputVideo)) { throw "Input file not found: $InputVideo" }
  if (-not (Test-Cmd "ffmpeg")) { throw "ffmpeg not in PATH. Try: winget install Gyan.FFmpeg" }
  & ffmpeg -hide_banner -y -ss 24 -i $InputVideo -t 18 -c copy $outFile
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Stream copy failed, re-encoding..."
    & ffmpeg -hide_banner -y -ss 24 -i $InputVideo -t 18 -c:v libx264 -crf 20 -preset fast -c:a aac -b:a 128k $outFile
  }
} else {
  $ytdlp = $null
  if (Test-Cmd "yt-dlp") { $ytdlp = "yt-dlp" }
  elseif (Test-Path (Join-Path $root ".tools\yt-dlp.exe")) { $ytdlp = (Join-Path $root ".tools\yt-dlp.exe") }
  if (-not $ytdlp) {
    throw "Pass -InputVideo, or install yt-dlp (pip / .tools\yt-dlp.exe) and ffmpeg in PATH."
  }
  if (-not (Test-Cmd "ffmpeg")) { throw "yt-dlp section download needs ffmpeg in PATH." }
  Remove-Item -LiteralPath $outFile -Force -ErrorAction SilentlyContinue
  & $ytdlp --download-sections "*0:24-0:42" -f "bv*+ba/b" --merge-output-format mp4 -o $outFile $BilibiliUrl
}

if (-not (Test-Path -LiteralPath $outFile)) { throw "Output not created: $outFile" }
Write-Host "OK: $outFile"

if (-not $UploadCatbox) { return }

$curl = "curl.exe"
if (-not (Test-Cmd $curl)) { throw "curl.exe not found." }

$argList = @("-s", "-S", "-F", "reqtype=fileupload", "-F", "fileToUpload=@$outFile")
if ($UserHash) { $argList += @("-F", "userhash=$UserHash") }
$argList += "https://catbox.moe/user/api.php"

$resp = & $curl @argList
if (-not $resp -or $resp -notmatch "^https://files\.catbox\.moe/") {
  throw "Catbox upload failed. Response: $resp"
}
Write-Host "Catbox: $resp"

if (-not $PatchIndexHtml) { return }

$indexPath = Join-Path $root "index.html"
$utf8 = New-Object System.Text.UTF8Encoding $false
$html = [System.IO.File]::ReadAllText($indexPath, $utf8)
$oldMp4 = "https://files.catbox.moe/你的文件码.mp4"
if ($html.IndexOf($oldMp4, [StringComparison]::Ordinal) -lt 0) {
  Write-Warning "Placeholder not found in index.html. Set first <source> src to: $resp"
  return
}
$html = $html.Replace($oldMp4, $resp.Trim())
[System.IO.File]::WriteAllText($indexPath, $html, $utf8)
Write-Host "Patched index.html (Catbox MP4)."
