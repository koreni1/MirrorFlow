@echo off
chcp 65001 >nul
title MirrorFlow Server
echo 🚀 Запуск MirrorFlow Server
echo.

cd /d "C:\Users\User\Desktop\MirrorFlow\"
echo Убедитесь, что установлены зависимости:
echo pip install numpy mss
echo.

python server.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка запуска сервера!
    echo Проверьте: 
    echo 1. Установлен ли Python?
    echo 2. Запущен ли файл server.py?
    echo 3. Установлены ли зависимости?
)

pause