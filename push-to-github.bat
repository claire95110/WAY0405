@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 当前目录: %CD%
echo.

REM 若远程只有创建仓库时的 README，先合并再推送：
git pull origin main --allow-unrelated-histories --no-edit
if errorlevel 1 (
  echo.
  echo [提示] pull 失败时，若你确定要用本机项目完全覆盖 GitHub 上的内容，可改用：
  echo   git push -u origin main --force
  echo.
  pause
  exit /b 1
)

git push -u origin main
if errorlevel 1 (
  echo.
  echo push 失败请检查：GitHub 登录、Personal Access Token，或网络。
  pause
  exit /b 1
)

echo.
echo 完成。仓库: https://github.com/claire95110/WAY-
pause
