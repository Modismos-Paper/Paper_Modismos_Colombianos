# Colombian Idioms Dataset Generation and Management System

Comprehensive system for extraction, processing, and consolidation of Colombian idioms from two main lexicographic sources.

## Project Structure

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

## Data Sources

### BDC (Brief Dictionary of Colombianisms)

Extraction and processing of idioms from PDF format using the `marker` library. Generates plain text files and associated metadata.

**Module**: `BDC/DB/ConvertPdf.py`

### DICOL (Dictionary of Colombianisms)

Access via REST API to the lexicographic database of Instituto Caro y Cuervo. Implements repository layer with dual storage support (remote/local).

**Module**: `DICOL/DB/DictionaryRepository.js`

## Generated Datasets

The `createDataSet.py` script generates five variants of the consolidated dataset:

### 1. DataSet.json
Complete dataset with all entries from both sources.

### 2. DataSet_ConEjemplos.json
Subset that includes only idioms with available usage examples.

### 3. DataSet_ConRegión.json
Idioms with defined geographic information (region of use).

### 4. DataSet_PrimeraOcurrencia.json
Deduplicated dataset with a single entry per idiom.

**Prioritization criteria**:
- BDC source over DICOL
- Entries with defined region over entries without region

### 5. DataSet_PrimeraOcurrencia_ConEjemplo.json
Deduplicated dataset that includes only idioms with usage examples.

## Record Structure

Each entry contains the following fields:

- `modismo`: Idiomatic expression
- `significado`: Lexicographic definition
- `ejemplo`: Usage context (optional)
- `región`: Geographic area of use (optional)
- `Fuente`: Record source (BDC/DICOL)

## Data Processing

### Cleaning

- Removal of entries without valid definition
- Normalization of missing values (`np.nan`)
- Replacement of empty strings with null values

### Consolidation

Datasets are sorted alphabetically by idiom and combined through vertical concatenation with complete reindexing.

### Deduplication

The first occurrence strategy uses multi-level sorting to ensure consistency in selecting unique records.

## Usage

```python
python createDataSet.py
```

The script automatically generates the five JSON files in the `Complete_DataSets/` directory.

## Dependencias

Consultar `requirements.txt` para la lista completa de dependencias del proyecto.
