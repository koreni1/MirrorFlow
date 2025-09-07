@echo off
chcp 65001 >nul
title Установка зависимостей MirrorFlow
echo 📦 Установка необходимых пакетов...
echo.

echo Устанавливаем pygame...
pip install pygame

echo Устанавливаем numpy...
pip install numpy

echo Устанавливаем mss...
pip install mss

echo.
echo ✅ Все зависимости установлены!
echo Теперь можно запустить server.bat и client.bat
pause