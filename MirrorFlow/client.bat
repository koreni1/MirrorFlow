@echo off
chcp 65001 >nul
title MirrorFlow Client
echo 📱 Запуск MirrorFlow Client
echo.

cd /d "C:\Users\User\Desktop\MirrorFlow\"
echo Убедитесь, что установлены зависимости:
echo pip install pygame numpy
echo.

python client.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка запуска клиента!
    echo Проверьте: 
    echo 1. Установлен ли Python?
    echo 2. Запущен ли сервер на указанном IP?
    echo 3. Установлены ли зависимости?
)

pause