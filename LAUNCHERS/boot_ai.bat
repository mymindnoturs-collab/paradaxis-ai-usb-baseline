@echo off
REM PAIGOS_AI_USB_V1 boot - resolve substrate then run AI dispatch self-test
setlocal
set DRIVE=%~d0
set AI_ROOT=%DRIVE%\PAIGOS_AI_USB_V1

if not defined PARADAXIS_SUBSTRATE (
  REM Try same drive
  if exist %DRIVE%\PAIGOS_BAUT_USB_V1\PRODUCTS\CPython.exe (
    set PARADAXIS_SUBSTRATE=%DRIVE%\PAIGOS_BAUT_USB_V1
  ) else (
    echo ERROR: PARADAXIS_SUBSTRATE not set + no PAIGOS_BAUT_USB_V1 on %DRIVE%
    echo Set env: PARADAXIS_SUBSTRATE=^<path to PAIGOS_BAUT_USB_V1^>
    pause
    exit /b 1
  )
)

echo === PAIGOS_AI_USB_V1 ===
echo SUBSTRATE: %PARADAXIS_SUBSTRATE%
echo AI_ROOT:   %AI_ROOT%

set CPYTHON=%PARADAXIS_SUBSTRATE%\PRODUCTS\CPython.exe

echo --- AI dispatch self-test ---
"%CPYTHON%" "%AI_ROOT%\AI_LAYER\dispatch.py" --self-test

echo === AI layer ready. Compose more via AI_LAYER/*.py ===
pause
