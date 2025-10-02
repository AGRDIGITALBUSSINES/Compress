#!/usr/bin/env python3
"""
PDF Compressor Application
==========================

A GUI application for compressing PDF files by reducing image quality
and optimizing file structure.

Author: AGR Digital Business
License: MIT
"""

import fitz  # PyMuPDF
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from PIL import Image
import io

def compress_pdf(input_path, output_path, target_size_mb=15, quality=50, progress_callback=None):
    """
    Comprime un PDF reduciendo significativamente el tamaño mediante múltiples técnicas.
    - input_path: ruta del PDF original
    - output_path: ruta donde se guardará el PDF comprimido
    - target_size_mb: tamaño objetivo en MB
    - quality: calidad de imágenes (1-100, donde 50 es un buen balance)
    - progress_callback: función para actualizar el progreso
    """
    try:
        if progress_callback:
            progress_callback("Abriendo PDF...", 5)

        # Abrir PDF original
        pdf_document = fitz.open(input_path)
        total_pages = len(pdf_document)
        
        # Crear un nuevo documento PDF para la salida
        new_pdf = fitz.open()
        
        if progress_callback:
            progress_callback(f"Procesando {total_pages} páginas...", 10)

        # Procesar cada página
        for page_num in range(total_pages):
            if progress_callback:
                progress = 10 + (page_num / total_pages) * 70
                progress_callback(f"Procesando página {page_num + 1}/{total_pages}", progress)
            
            # Obtener la página original
            original_page = pdf_document[page_num]
            
            # Crear una nueva página en el documento de salida
            new_page = new_pdf.new_page(width=original_page.rect.width, 
                                       height=original_page.rect.height)
            
            # Obtener y comprimir imágenes de la página
            image_list = original_page.get_images(full=True)
            
            # Copiar el contenido de texto primero
            text_dict = original_page.get_text("dict")
            
            # Recrear el contenido sin imágenes primero
            for block in text_dict["blocks"]:
                if "lines" in block:  # Es un bloque de texto
                    for line in block["lines"]:
                        for span in line["spans"]:
                            # Insertar texto con formato
                            try:
                                text = span["text"]
                                if text.strip():
                                    font_size = span["size"]
                                    bbox = fitz.Rect(span["bbox"])
                                    new_page.insert_text(bbox.tl, text, fontsize=font_size)
                            except:
                                continue
            
            # Procesar y comprimir imágenes
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    
                    # Extraer imagen original
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Comprimir imagen usando PIL
                    compressed_image_bytes = compress_image(image_bytes, quality)
                    
                    if compressed_image_bytes:
                        # Obtener información de posición de la imagen
                        image_bbox = original_page.get_image_bbox(img)
                        
                        # Insertar imagen comprimida en la nueva página
                        new_page.insert_image(image_bbox, stream=compressed_image_bytes)
                    
                except Exception as e:
                    # Si hay error con una imagen, intentar insertar la original
                    try:
                        image_bbox = original_page.get_image_bbox(img)
                        new_page.insert_image(image_bbox, stream=image_bytes)
                    except:
                        continue
        
        if progress_callback:
            progress_callback("Optimizando documento final...", 85)

        # Guardar el documento comprimido con máxima compresión
        new_pdf.save(output_path,
                    deflate=True,          # Compresión deflate
                    garbage=4,             # Máximo nivel de limpieza
                    clean=True)            # Limpiar contenido
        
        # Cerrar documentos
        new_pdf.close()
        pdf_document.close()
        
        if progress_callback:
            progress_callback("Verificando resultado...", 95)

        # Verificar tamaños
        original_size_mb = os.path.getsize(input_path) / (1024 * 1024)
        compressed_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        compression_ratio = (1 - compressed_size_mb / original_size_mb) * 100
        
        message = f"✅ Compresión completada!\n"
        message += f"Tamaño original: {original_size_mb:.2f} MB\n"
        message += f"Tamaño comprimido: {compressed_size_mb:.2f} MB\n"
        message += f"Reducción: {compression_ratio:.1f}%"
        
        if compressed_size_mb <= target_size_mb:
            message += f"\n🎯 Objetivo de {target_size_mb} MB alcanzado!"
        else:
            message += f"\n⚠️ Objetivo: {target_size_mb} MB (puedes reducir más la calidad)"
        
        if progress_callback:
            progress_callback(message, 100)
        
        return True, message
        
    except Exception as e:
        error_msg = f"❌ Error al comprimir: {str(e)}"
        if progress_callback:
            progress_callback(error_msg, 100)
        return False, error_msg

def compress_image(image_bytes, quality=50):
    """
    Comprime una imagen usando PIL manteniendo un balance entre calidad y tamaño.
    """
    try:
        # Abrir imagen con PIL
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convertir a RGB si es necesario (para JPEG)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Crear fondo blanco para transparencias
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionar si la imagen es muy grande
        max_dimension = 1200  # píxeles
        if max(image.size) > max_dimension:
            image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
        
        # Comprimir imagen
        output_buffer = io.BytesIO()
        
        # Usar JPEG con calidad especificada
        image.save(output_buffer, 
                  format='JPEG', 
                  quality=quality,
                  optimize=True,
                  progressive=True)
        
        compressed_bytes = output_buffer.getvalue()
        output_buffer.close()
        
        # Solo devolver si realmente se comprimió
        if len(compressed_bytes) < len(image_bytes):
            return compressed_bytes
        else:
            # Si no se comprimió, intentar con menor calidad
            if quality > 30:
                return compress_image(image_bytes, quality - 20)
            else:
                return compressed_bytes
    
    except Exception as e:
        return None

class PDFCompressorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresor de PDF - AGR Digital Business")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.target_size = tk.DoubleVar(value=15.0)
        self.image_quality = tk.IntVar(value=50)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Título
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill="x", padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📄 Compresor de PDF", 
                              font=("Arial", 16, "bold"), 
                              fg="white", bg="#2c3e50")
        title_label.pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Selección de archivo de entrada
        input_frame = tk.LabelFrame(main_frame, text="📂 Archivo PDF a comprimir", 
                                   font=("Arial", 10, "bold"), padx=10, pady=10)
        input_frame.pack(fill="x", pady=(0, 15))
        
        tk.Entry(input_frame, textvariable=self.input_file, width=50, 
                state="readonly").pack(side="left", padx=(0, 10))
        tk.Button(input_frame, text="Buscar...", command=self.select_input_file,
                 bg="#3498db", fg="white", font=("Arial", 9, "bold")).pack(side="right")
        
        # Configuración
        config_frame = tk.LabelFrame(main_frame, text="⚙️ Configuración", 
                                    font=("Arial", 10, "bold"), padx=10, pady=10)
        config_frame.pack(fill="x", pady=(0, 15))
        
        # Tamaño objetivo
        size_frame = tk.Frame(config_frame)
        size_frame.pack(fill="x", pady=(0, 10))
        tk.Label(size_frame, text="Tamaño objetivo (MB):", 
                font=("Arial", 9)).pack(side="left")
        tk.Spinbox(size_frame, from_=1, to=100, textvariable=self.target_size, 
                  width=10, font=("Arial", 9)).pack(side="right")
        
        # Calidad de imágenes
        quality_frame = tk.Frame(config_frame)
        quality_frame.pack(fill="x")
        tk.Label(quality_frame, text="Calidad imágenes (1-100):", 
                font=("Arial", 9)).pack(side="left")
        quality_spinbox = tk.Spinbox(quality_frame, from_=1, to=100, 
                                   textvariable=self.image_quality, 
                                   width=10, font=("Arial", 9))
        quality_spinbox.pack(side="right")
        
        # Etiqueta de ayuda para calidad
        help_frame = tk.Frame(config_frame)
        help_frame.pack(fill="x", pady=(5, 0))
        tk.Label(help_frame, text="💡 Menor calidad = mayor compresión (recomendado: 30-70)", 
                font=("Arial", 8), fg="#7f8c8d").pack()
        
        # Progreso
        progress_frame = tk.LabelFrame(main_frame, text="📊 Progreso", 
                                      font=("Arial", 10, "bold"), padx=10, pady=10)
        progress_frame.pack(fill="x", pady=(0, 15))
        
        self.progress_var = tk.StringVar(value="Esperando archivo...")
        self.progress_label = tk.Label(progress_frame, textvariable=self.progress_var, 
                                      font=("Arial", 9))
        self.progress_label.pack(pady=(0, 5))
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode="determinate")
        self.progress_bar.pack(fill="x")
        
        # Botones
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 10))
        
        self.compress_button = tk.Button(button_frame, text="🔄 Comprimir PDF", 
                                        command=self.compress_pdf_thread,
                                        bg="#27ae60", fg="white", 
                                        font=("Arial", 12, "bold"), 
                                        height=2, state="disabled")
        self.compress_button.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        tk.Button(button_frame, text="📁 Abrir carpeta", 
                 command=self.open_output_folder,
                 bg="#f39c12", fg="white", 
                 font=("Arial", 12, "bold"), height=2).pack(side="right", padx=(5, 0))
        
        # Información
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill="x")
        
        info_text = "💡 Selecciona un archivo PDF y ajusta la configuración para comenzar la compresión."
        tk.Label(info_frame, text=info_text, font=("Arial", 8), 
                fg="#7f8c8d", wraplength=550, justify="center").pack()
    
    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            self.input_file.set(file_path)
            # Generar nombre de archivo de salida
            base_name = os.path.splitext(file_path)[0]
            output_path = f"{base_name}_comprimido.pdf"
            self.output_file.set(output_path)
            
            self.compress_button.config(state="normal")
            self.progress_var.set("Archivo seleccionado. Listo para comprimir.")
            
            # Mostrar información del archivo
            try:
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                self.progress_var.set(f"Archivo seleccionado: {size_mb:.2f} MB")
            except:
                pass
    
    def update_progress(self, message, progress):
        self.progress_var.set(message)
        self.progress_bar['value'] = progress
        self.root.update_idletasks()
    
    def compress_pdf_thread(self):
        # Ejecutar compresión en un hilo separado para no bloquear la UI
        self.compress_button.config(state="disabled")
        threading.Thread(target=self.compress_pdf_async, daemon=True).start()
    
    def compress_pdf_async(self):
        input_path = self.input_file.get()
        output_path = self.output_file.get()
        target_size = self.target_size.get()
        quality = self.image_quality.get()
        
        if not input_path:
            messagebox.showerror("Error", "Por favor selecciona un archivo PDF.")
            self.compress_button.config(state="normal")
            return
        
        # Ejecutar compresión
        success, message = compress_pdf(input_path, output_path, target_size, quality, 
                                       self.update_progress)
        
        # Mostrar resultado
        if success:
            result = messagebox.askyesno("✅ Compresión completada", 
                                       f"{message}\n\n¿Deseas abrir la carpeta de destino?")
            if result:
                self.open_output_folder()
        else:
            messagebox.showerror("❌ Error", message)
        
        self.compress_button.config(state="normal")
    
    def open_output_folder(self):
        output_path = self.output_file.get()
        if output_path and os.path.exists(output_path):
            folder_path = os.path.dirname(output_path)
            os.startfile(folder_path)
        else:
            messagebox.showwarning("Advertencia", "No hay archivo de salida disponible.")

def main():
    root = tk.Tk()
    app = PDFCompressorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
