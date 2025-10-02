#!/usr/bin/env python3
"""
Script para crear ejecutable de PDF Compressor
"""
import os
import sys
import subprocess
import shutil

def create_executable():
    print("=" * 50)
    print("  Creando ejecutable de PDF Compressor")
    print("=" * 50)
    print()
    
    # Limpiar builds anteriores
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("🗑️  Limpiando build anterior...")
    
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        print("🗑️  Limpiando dist anterior...")
    
    if os.path.exists("release"):
        shutil.rmtree("release")
        print("🗑️  Limpiando release anterior...")
    
    print("\n📦 Generando ejecutable...")
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",           # Un solo archivo ejecutable
        "--windowed",          # Sin ventana de consola
        "--name", "PDF_Compressor",
        "--distpath", "release",
        "--workpath", "build",
        "--specpath", "build",
        "main.py"
    ]
    
    try:
        # Ejecutar PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Verificar si se creó el ejecutable
        exe_path = os.path.join("release", "PDF_Compressor.exe")
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path)
            size_mb = file_size / (1024 * 1024)
            
            print("\n" + "=" * 50)
            print("  ✅ Ejecutable creado exitosamente!")
            print(f"  📁 Ubicación: {exe_path}")
            print(f"  📦 Tamaño: {size_mb:.1f} MB")
            print("=" * 50)
            
            return True
        else:
            print("❌ Error: No se encontró el ejecutable generado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear ejecutable: {e}")
        print(f"Output: {e.output}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    if create_executable():
        print("\n🎉 ¡Proceso completado!")
        print("💡 Ahora puedes distribuir el archivo PDF_Compressor.exe")
        print("   sin necesidad de instalar Python en otras PCs.")
    else:
        print("\n❌ No se pudo completar el proceso.")
        sys.exit(1)