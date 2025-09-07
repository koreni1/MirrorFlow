@echo off
chcp 65001 >nul
title MirrorFlow Launcher
echo 🎮 MIRRORFLOW - СИСТЕМА УДАЛЕННОГО ДЕМОНСТРИРОВАНИЯ ЭКРАНА
echo ========================================================
echo.
echo 1 - Запустить СЕРВЕР (захват экрана)
echo 2 - Запустить КЛИЕНТ (просмотр экрана)
echo 3 - Установить зависимости
echo 4 - Выход
echo.

choice /c 1234 /n /m "Выберите действие: "

if %errorlevel% equ 1 (
    start server.bat
) else if %errorlevel% equ 2 (
    start client.bat
) else if %errorlevel% equ 3 (
    start install_deps.bat
) else if %errorlevel% equ 4 (
    exit
)