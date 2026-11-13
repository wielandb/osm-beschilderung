@echo off
cd /d "%~dp0.."
python scripts/sort-values.py %* || exit /b 1
python scripts/generate-readme.py || exit /b 1
python scripts/generate-taginfo.py || exit /b 1
