"""
Script para generar CSV y Excel con datos de prompt 3 del modelo Sonar.
Columnas: Ejemplo, Modismo, Definición Real, Sinónimo, Definición Sinónimo

Selección: 1,715 registros aleatorios incluyendo los 611 con región definida
"""

import json
import pandas as pd
import os
import random

# Configuración de semilla para reproducibilidad
random.seed(42)

# Configuración de tamaño de muestra
TOTAL_MUESTRA = 1715
REGISTROS_CON_REGION = 611

# ============================================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================================
script_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del script
base_dir = os.path.dirname(script_dir)  # Directorio LLMs_Metrics

# ============================================================================
# CARGA DE DATOS
# ============================================================================

# Cargar datos de prompt 3
print("Cargando datos de prompt 3...")
with open(os.path.join(base_dir, 'LLMs_Results', 'prompt_3_metrics_data.json'), 'r', encoding='utf-8') as f:
    prompt3_data = json.load(f)

# Cargar dataset con región para identificar modismos con región
print("Cargando dataset con región...")
with open(os.path.join(base_dir, 'DataSet', 'DataSet_ConRegión.json'), 'r', encoding='utf-8') as f:
    dataset_region = json.load(f)

# ============================================================================
# IDENTIFICACIÓN DE MODISMOS CON REGIÓN
# ============================================================================

# Crear conjunto de modismos que tienen región definida
modismos_con_region = set()
for item in dataset_region:
    region = item.get('región')
    if region and region.strip():  # Región no vacía
        modismos_con_region.add(item.get('modismo'))

print(f"  → {len(modismos_con_region)} modismos únicos con región identificados")

# ============================================================================
# FILTRADO DE DATOS
# ============================================================================

# Filtrar solo registros del modelo Sonar
print("Filtrando registros de Sonar...")
sonar_records = [record for record in prompt3_data if record.get('modelo') == 'perplexity/sonar']

print(f"  → {len(sonar_records)} registros de Sonar encontrados")

# ============================================================================
# SELECCIÓN ALEATORIA CON REGIÓN INCLUIDA
# ============================================================================

# Separar registros por si tienen región o no
registros_con_region = [r for r in sonar_records if r.get('modismo') in modismos_con_region]
registros_sin_region = [r for r in sonar_records if r.get('modismo') not in modismos_con_region]

print(f"\nSeleccionando muestra de {TOTAL_MUESTRA} registros:")
print(f"  → Registros con región: {len(registros_con_region)}")
print(f"  → Registros sin región disponibles: {len(registros_sin_region)}")

# Calcular cuántos registros sin región necesitamos
registros_sin_region_needed = TOTAL_MUESTRA - len(registros_con_region)

# Seleccionar aleatoriamente de los registros sin región
registros_sin_region_seleccionados = random.sample(registros_sin_region, registros_sin_region_needed)

# Combinar ambos grupos
sonar_records = registros_con_region + registros_sin_region_seleccionados
random.shuffle(sonar_records)  # Mezclar para que no estén agrupados

print(f"  → Total seleccionados: {len(sonar_records)} registros")

# ============================================================================
# PREPARACIÓN DE DATOS PARA EXPORTACIÓN
# ============================================================================

# Crear lista de diccionarios con las columnas solicitadas
data = []
for record in sonar_records:
    data.append({
        'Ejemplo': record.get('ejemplo', ''),
        'Modismo': record.get('modismo', ''),
        'Definición Real': record.get('significado_real', ''),
        'Sinónimo': record.get('literal_generado', ''),
        'Definición Sinónimo': record.get('definicion_generada', '')
    })

# ============================================================================
# EXPORTACIÓN A CSV Y EXCEL
# ============================================================================

# Crear DataFrame
df = pd.DataFrame(data)

# Exportar a Excel
output_excel = os.path.join(script_dir, 'sonar_prompt_3.xlsx')
df.to_excel(output_excel, index=False, engine='openpyxl')

# Exportar a CSV
output_csv = os.path.join(script_dir, 'sonar_prompt_3.csv')
df.to_csv(output_csv, index=False, encoding='utf-8')

# ============================================================================
# RESUMEN
# ============================================================================

print("\n✓ Archivos generados exitosamente:")
print(f"  → Excel: {os.path.basename(output_excel)} ({len(sonar_records)} registros)")
print(f"  → CSV: {os.path.basename(output_csv)} ({len(sonar_records)} registros)")
