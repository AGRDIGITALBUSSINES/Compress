@echo off
echo ==========================================
echo  Creando ejecutable de PDF Compressor
echo ==========================================
echo.

REM Activar el entorno virtual
call .venv\Scripts\activate.bat

REM Limpiar builds anteriores
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo Generando ejecutable...
echo.

REM Crear el ejecutable con PyInstaller
pyinstaller --onefile ^
    --windowed ^
    --name "PDF_Compressor" ^
    --add-data "src;src" ^
    --distpath "release" ^
    --workpath "build" ^
    --specpath "build" ^
    main.py

echo.
if exist "release\PDF_Compressor.exe" (
    echo ==========================================
    echo  ✅ Ejecutable creado exitosamente!
    echo  📁 Ubicacion: release\PDF_Compressor.exe
    echo  📦 Tamaño: 
    for %%A in (release\PDF_Compressor.exe) do echo     %%~zA bytes
    echo ==========================================
    echo.
    echo ¿Deseas abrir la carpeta de release? (s/n)
    set /p choice=
    if /i "%choice%"=="s" start explorer "release"
) else (
    echo ❌ Error: No se pudo crear el ejecutable
    pause
)

echo.
echo Presiona cualquier tecla para salir...
pause > nul