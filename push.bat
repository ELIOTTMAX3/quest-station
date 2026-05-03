@echo off
echo.
echo ==============================
echo   Quest Station — Push GitHub
echo ==============================
echo.

cd /d "%~dp0"

git add .
git commit -m "Mise à jour Quest Station"
git push

echo.
echo ✅ Mis en ligne sur GitHub Pages !
echo    https://eliottmax3.github.io/quest-station/
echo.
pause
