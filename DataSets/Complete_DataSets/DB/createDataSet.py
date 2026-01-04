"""
Generación de conjuntos de datos consolidados de modismos colombianos.

Extrae y combina datos de dos fuentes (DICOL y BDC), aplicando diferentes
criterios de filtrado para generar múltiples variantes del dataset.
"""

import pandas as pd
import numpy as np
import os
pd.set_option('future.no_silent_downcasting', True)

# Obtener el directorio del script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_DICOL(location):
    """Extrae datos del Diccionario de Colombianismos (DICOL)."""
    return pd.read_json(location)

def extract_BDC(location):
    """Extrae datos del Breve Diccionario de Colombianismos (BDC)."""
    return pd.read_json(location)


# Carga y limpieza de DICOL
location_DICOL = os.path.join(SCRIPT_DIR, "../../DICOL/DICOL.json")
DICOL = extract_DICOL(location_DICOL)
# Excluye entradas sin definición válida
DICOL = DICOL[(DICOL["significado"] != "Definición no encontrada.")].copy()
DICOL = DICOL.replace({'Ejemplo no encontrado.': np.nan, '': np.nan})
DICOL["Fuente"] = "DICOL"

# Carga y limpieza de BDC
location_BDC = os.path.join(SCRIPT_DIR, "../../BDC/BDC.json")
BDC = extract_BDC(location_BDC)
BDC = BDC[(BDC["significado"] != "")].copy()
BDC = BDC.replace({'': np.nan})
BDC["Fuente"] = "BDC"

# Consolidación de ambas fuentes en un único dataset
print("Datos de BDC: ", len(BDC))
print("Datos de DICOL: ", len(DICOL))
print()
DataSet = pd.concat([BDC, DICOL], ignore_index=True)
DataSet.rename(columns={"palabra":"modismo"}, inplace=True)
DataSet.sort_values(by=["modismo"], inplace=True)
print(f"Total de definiciones: {len(DataSet)}")
DataSet.to_json(os.path.join(SCRIPT_DIR, "../DataSet.json"), orient="records", force_ascii=False, indent=4)

# Dataset filtrado: solo modismos con ejemplo disponible
DataSet_WithExample = DataSet.dropna(subset=["ejemplo"]).reset_index(drop=True).sort_values(by=["modismo"])
print(f"Total de ejemplos: {len(DataSet_WithExample)}")
DataSet_WithExample.to_json(os.path.join(SCRIPT_DIR, "../DataSet_ConEjemplos.json"), orient="records", force_ascii=False, indent=4)

# Dataset de primera ocurrencia: una entrada por modismo único
# Criterios de priorización:
#   1. Fuente BDC sobre DICOL (mayor información regional)
#   2. Dentro de cada fuente, prioriza entradas con región definida
DataSet_FirstOccurrence = DataSet.sort_values(by=["Fuente", "región"], ascending=[True, True]).drop_duplicates(subset=["modismo"], keep="first").reset_index(drop=True).sort_values(by=["modismo"])
print(f"Total modismos únicos: {len(DataSet_FirstOccurrence)}")
DataSet_FirstOccurrence.to_json(os.path.join(SCRIPT_DIR, "../DataSet_PrimeraOcurrencia.json"), orient="records", force_ascii=False, indent=4)

# Dataset filtrado: solo modismos con región geográfica definida
DataSet_WithRegion = DataSet.dropna(subset=["región"]).reset_index(drop=True).sort_values(by=["modismo"])
print(f"Total modismos con región: {len(DataSet_WithRegion)}")
DataSet_WithRegion.to_json(os.path.join(SCRIPT_DIR, "../DataSet_ConRegión.json"), orient="records", force_ascii=False, indent=4)


# Dataset de primera ocurrencia con ejemplo disponible.
DataSet_FirstOccurrence_WithExample = DataSet_WithExample.sort_values(by=["Fuente", "región"], ascending=[True, True]).drop_duplicates(subset=["modismo"], keep="first").reset_index(drop=True).sort_values(by=["modismo"])
print(f"Total modismos únicos con ejemplo (primera ocurrencia): {len(DataSet_FirstOccurrence_WithExample)}")
DataSet_FirstOccurrence_WithExample.to_json(os.path.join(SCRIPT_DIR, "../DataSet_PrimeraOcurrencia_ConEjemplo.json"), orient="records", force_ascii=False, indent=4)

print()