# 在本机启动静态网站，便于手机通过 http 访问（不要用 file:// 打开 index.html）
# 用法：右键「使用 PowerShell 运行」，或在项目目录执行: .\serve-for-mobile.ps1
param(
    [int]$Port = 8765
)

Set-Location $PSScriptRoot
$py = $null
foreach ($name in @('python', 'py', 'python3')) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) { $py = $cmd.Source; break }
}
if (-not $py) {
    Write-Host "未检测到 Python。请安装 Python 3，或安装 Node 后使用: npx --yes serve . -l $Port" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "站点根目录: $PSScriptRoot" -ForegroundColor Cyan
Write-Host "端口: $Port" -ForegroundColor Cyan
Write-Host ""
Write-Host "【同一 Wi-Fi 下】在手机浏览器打开下面任意链接：" -ForegroundColor Green
Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } |
    ForEach-Object { Write-Host ("  http://{0}:{1}/index.html" -f $_.IPAddress, $Port) }
Write-Host ""
Write-Host "若 Windows 防火墙弹出提示，请允许专用网络访问。" -ForegroundColor Yellow
Write-Host "停止服务: 在本窗口按 Ctrl+C" -ForegroundColor DarkGray
Write-Host ""
Write-Host "【手机用流量 / 不在同一网络】需要公网隧道，另开一个 PowerShell 窗口执行：" -ForegroundColor Magenta
Write-Host "  cd `"$PSScriptRoot`"" -ForegroundColor Gray
Write-Host "  npx --yes localtunnel --port $Port" -ForegroundColor Gray
Write-Host "（首次需安装 Node.js；localtunnel 给出的 https 链接可在手机打开，有时需点一次 Continue）" -ForegroundColor DarkGray
Write-Host ""

& $py -m http.server $Port
