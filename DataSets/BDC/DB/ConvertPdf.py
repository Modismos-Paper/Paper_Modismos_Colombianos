"""
Módulo para convertir archivos PDF a texto plano utilizando la biblioteca marker.
Procesa PDFs del Diccionario Breve de Colombianismos y extrae texto y metadatos.
"""

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
import os
import json
from pathlib import Path


def save_text_to_file(text, pdf_filename, output_dir="output"):
    """
    Guarda el texto extraído de un PDF en un archivo .txt.
    
    Args:
        text (str): Contenido de texto extraído del PDF.
        pdf_filename (str): Nombre del archivo PDF original.
        output_dir (str): Directorio donde guardar el archivo. Por defecto 'output'.
    
    Returns:
        str: Ruta completa del archivo de texto generado.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = Path(pdf_filename).stem
    output_file = os.path.join(output_dir, f"{base_name}_text.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Texto guardado en: {output_file}")
    return output_file



def save_metadata(metadata, pdf_filename, output_dir="output"):
    """
    Guarda los metadatos extraídos del PDF en formato JSON.
    
    Args:
        metadata (dict): Diccionario con los metadatos del documento.
        pdf_filename (str): Nombre del archivo PDF original.
        output_dir (str): Directorio donde guardar el archivo. Por defecto 'output'.
    
    Returns:
        str: Ruta completa del archivo JSON generado.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = Path(pdf_filename).stem
    metadata_file = os.path.join(output_dir, f"{base_name}_metadata.json")
    
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"Metadatos guardados en: {metadata_file}")
    return metadata_file

def main():
    """
    Función principal para procesar archivos PDF del Diccionario Breve de Colombianismos.
    Convierte cada PDF a texto y extrae metadatos, guardando ambos por separado.
    """
    pdf_files = ["Diccionario_breve_de_Colombiaismos_slown.pdf"]
    
    # Inicializar convertidor con modelos de marker
    converter = PdfConverter(artifact_dict=create_model_dict())
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            print(f"\nProcesando: {pdf_file}")
            
            try:
                rendered = converter(pdf_file)
                text, metadata, _ = text_from_rendered(rendered)
                
                save_text_to_file(text, pdf_file)
                save_metadata(metadata, pdf_file)
                
                print(f"✓ Completado: {pdf_file}")
                
            except Exception as e:
                print(f"✗ Error procesando {pdf_file}: {str(e)}")
        else:
            print(f"⚠ Archivo no encontrado: {pdf_file}")

if __name__ == "__main__":
    main()
