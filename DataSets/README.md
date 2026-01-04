# Sistema de Generación y Gestión de Datasets de Modismos Colombianos

Sistema integral para la extracción, procesamiento y consolidación de modismos colombianos provenientes de dos fuentes lexicográficas principales.

## Estructura del Proyecto

```
DataSet/
├── BDC/
│   ├── BDC.json
│   └── DB/
│       ├── ConvertPdf.py
│       ├── GenerateDB.ipynb
│       └── Diccionario_breve_de_Colombiaismos_slown_text.txt
├── DICOL/
│   ├── DICOL.json
│   └── DB/
│       ├── DictionaryRepository.js
│       └── GenerateDB.js
├── Complete_DataSets/
│   ├── DataSet.json
│   ├── DataSet_ConEjemplos.json
│   ├── DataSet_ConRegión.json
│   ├── DataSet_PrimeraOcurrencia.json
│   ├── DataSet_PrimeraOcurrencia_ConEjemplo.json
│   └── DB/
│       └── createDataSet.py
└── DataSets_Analysis.ipynb
```

## Fuentes de Datos

### BDC (Breve Diccionario de Colombianismos)

Extracción y procesamiento de modismos desde formato PDF mediante la biblioteca `marker`. Genera archivos de texto plano y metadatos asociados.

**Módulo**: `BDC/DB/ConvertPdf.py`

### DICOL (Diccionario de Colombianismos)

Acceso mediante API REST a la base de datos lexicográfica del Instituto Caro y Cuervo. Implementa capa de repositorio con soporte para almacenamiento dual (remoto/local).

**Módulo**: `DICOL/DB/DictionaryRepository.js`

## Datasets Generados

El script `createDataSet.py` genera cinco variantes del dataset consolidado:

### 1. DataSet.json
Dataset completo con todas las entradas de ambas fuentes.

### 2. DataSet_ConEjemplos.json
Subconjunto que incluye únicamente modismos con ejemplo de uso disponible.

### 3. DataSet_ConRegión.json
Modismos con información geográfica (región de uso) definida.

### 4. DataSet_PrimeraOcurrencia.json
Dataset deduplicado con una única entrada por modismo.

**Criterios de priorización**:
- Fuente BDC sobre DICOL
- Entradas con región definida sobre entradas sin región

### 5. DataSet_PrimeraOcurrencia_ConEjemplo.json
Dataset deduplicado que incluye únicamente modismos con ejemplo de uso.

## Estructura de Registros

Cada entrada contiene los siguientes campos:

- `modismo`: Expresión idiomática
- `significado`: Definición lexicográfica
- `ejemplo`: Contexto de uso (opcional)
- `región`: Área geográfica de uso (opcional)
- `Fuente`: Origen del registro (BDC/DICOL)

## Procesamiento de Datos

### Limpieza

- Eliminación de entradas sin definición válida
- Normalización de valores ausentes (`np.nan`)
- Reemplazo de cadenas vacías por valores nulos

### Consolidación

Los datasets se ordenan alfabéticamente por modismo y se combinan mediante concatenación vertical con reindexado completo.

### Deduplicación

La estrategia de primera ocurrencia utiliza ordenamiento multinivel para garantizar consistencia en la selección de registros únicos.

## Uso

```python
python createDataSet.py
```

El script genera automáticamente los cinco archivos JSON en el directorio `Complete_DataSets/`.

## Dependencias

Consultar `requirements.txt` para la lista completa de dependencias del proyecto.
