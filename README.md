# PDF Compressor

Una aplicación de escritorio desarrollada en Python para comprimir archivos PDF reduciendo el tamaño de las imágenes contenidas y optimizando la estructura del documento.

## 📋 Características

- **Interfaz gráfica intuitiva** desarrollada con Tkinter
- **Compresión efectiva** de archivos PDF
- **Control de calidad** de imágenes configurable
- **Progreso en tiempo real** durante la compresión
- **Estadísticas detalladas** de compresión alcanzada
- **Optimización automática** de imágenes grandes
- **Manejo robusto de errores**

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/AGRDIGITALBUSSINES/pdf-compressor.git
   cd pdf-compressor
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación:**
   ```bash
   python main.py
   ```

## 🎯 Uso

1. **Ejecuta la aplicación** con `python main.py`
2. **Selecciona un archivo PDF** haciendo clic en "Buscar..."
3. **Configura los parámetros:**
   - **Tamaño objetivo:** El tamaño deseado en MB
   - **Calidad de imágenes:** 1-100 (menor valor = mayor compresión)
4. **Haz clic en "Comprimir PDF"**
5. **Observa el progreso** en la barra de estado
6. **¡Listo!** El archivo comprimido se guardará automáticamente

## ⚙️ Configuración Recomendada

| Tipo de Documento | Calidad Recomendada | Resultado Esperado |
|-------------------|--------------------|--------------------|
| Documentos de archivo | 30-40 | Máxima compresión |
| Documentos generales | 50-60 | Balance calidad/tamaño |
| Presentaciones importantes | 70-80 | Alta calidad |

## 🔧 Dependencias

- **PyMuPDF (fitz)**: Manipulación de archivos PDF
- **Pillow (PIL)**: Procesamiento y compresión de imágenes
- **Tkinter**: Interfaz gráfica (incluido con Python)

## 📊 Resultados Típicos

- **Reducción promedio:** 60-80% del tamaño original
- **PDFs con muchas imágenes:** hasta 90% de reducción
- **Mantiene legibilidad** del texto
- **Preserva estructura** del documento

## 🛠️ Desarrollo

### Estructura del proyecto

```
pdf-compressor/
├── src/
│   └── pdf_compressor.py      # Código principal de la aplicación
├── main.py                    # Punto de entrada
├── requirements.txt           # Dependencias Python
├── README.md                  # Este archivo
└── .github/
    └── copilot-instructions.md # Instrucciones para desarrollo
```

### Ejecutar en modo desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**AGR Digital Business**
- Website: [agrdb.com](https://agrdb.com)
- Email: contacto@agrdigitalbusiness.com

## ⭐ Soporte

Si encuentras útil este proyecto, ¡no olvides darle una estrella! ⭐

Para reportar bugs o solicitar nuevas características, por favor abre un [issue](https://github.com/AGRDIGITALBUSSINES/pdf-compressor/issues).

---

**¡Gracias por usar PDF Compressor!** 🚀
