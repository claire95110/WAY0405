@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 当前目录: %CD%
echo 目标远程: https://github.com/claire95110/WAY0405.git
echo.

REM 空仓库（未初始化 README）应直接 push；仅当 push 失败时再尝试合并远程
git push -u origin main
if errorlevel 1 (
  echo.
  echo 首次 push 失败，尝试 pull 合并后再 push...
  git pull origin main --allow-unrelated-histories --no-edit
  if errorlevel 1 (
    echo.
    echo 若仍失败，且确定要用本机覆盖远程，可手动执行:
    echo   git push -u origin main --force
    pause
    exit /b 1
  )
  git push -u origin main
  if errorlevel 1 (
    echo push 仍失败，请检查登录与网络。
    pause
    exit /b 1
  )
)

echo.
echo 完成。仓库: https://github.com/claire95110/WAY0405
echo 请确认网页上存在 assets 文件夹后再在 Vercel 关联本仓库部署。
pause
