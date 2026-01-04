"""
Sentence-BERT: Similitud semántica con embeddings multilingües
Modelo: paraphrase-multilingual-mpnet-base-v2

Basado en la documentación oficial de Sentence Transformers:
https://sbert.net/
"""

import os
# Prevent transformers from trying to load TensorFlow
os.environ['TRANSFORMERS_NO_TF'] = '1'

import torch
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import warnings
warnings.filterwarnings('ignore')
from sentence_transformers import models
from sentence_transformers import util


# Detectar dispositivo disponible (MPS para Apple Silicon, CUDA para NVIDIA, o CPU)
if torch.backends.mps.is_available():
    device = "mps"
    print("Usando GPU (Metal Performance Shaders) en Apple Silicon")
elif torch.cuda.is_available():
    device = "cuda"
    print("Usando GPU (CUDA)")
else:
    device = "cpu"
    print("Usando CPU")

# 1. Load pretrained Sentence Transformer models

# Using multilingual model for Spanish support
model_sbert = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2', device=device)

# XLM-RoBERTa model trained on STS multilingual data for semantic similarity
model_xlm = SentenceTransformer('sentence-transformers/stsb-xlm-r-multilingual', device=device)

# SciBETO using SciBETO large model and mean pooling
word_embedding_model = models.Transformer('Flaglab/SciBETO-large')
pooling_model = models.Pooling(
    word_embedding_model.get_word_embedding_dimension(),
    pooling_mode_mean_tokens=True,
    pooling_mode_cls_token=False,
    pooling_mode_max_tokens=False
)
model_scibeto = SentenceTransformer(modules=[word_embedding_model, pooling_model], device=device)


def compute_sbert_similarity(candidatos: List[str], referencias: List[str]) -> np.ndarray:
    """
    Calcula similitud de coseno entre candidatos y referencias usando Sentence-BERT.
    
    El modelo paraphrase-multilingual-mpnet-base-v2 genera embeddings semánticos
    que capturan el significado del texto, permitiendo comparar frases con 
    palabras diferentes pero significado similar.
    
    Según la documentación oficial (https://sbert.net/):
    - model.encode() calcula embeddings para las oraciones
    - model.similarity() calcula la similitud entre embeddings
    
    Args:
        candidatos: Lista de textos generados por el modelo
        referencias: Lista de textos de referencia (ground truth)
        
    Returns:
        Array con scores de similitud de coseno (rango: -1 a 1, típicamente 0 a 1)
        Valores cercanos a 1 indican alta similitud semántica
    """
    # 2. Calculate embeddings by calling model.encode()
    embeddings_candidatos = model_sbert.encode(candidatos)
    embeddings_referencias = model_sbert.encode(referencias)
    
    # 3. Calculate the embedding similarities
    # Using the official similarity method from Sentence Transformers
    similarities = []
    for emb_cand, emb_ref in zip(embeddings_candidatos, embeddings_referencias):
        # Calculate pairwise similarity
        sim = model_sbert.similarity(emb_cand, emb_ref)
        # Extract scalar value from tensor
        similarities.append(float(sim))
    
    return np.array(similarities)


def compute_xlm_similarity(candidatos: List[str], referencias: List[str]) -> np.ndarray:
    """
    Calcula similitud de coseno entre candidatos y referencias usando XLM-RoBERTa.
    
    El modelo stsb-xlm-r-multilingual está entrenado específicamente para
    similitud semántica textual en múltiples idiomas, proporcionando embeddings
    optimizados para comparar el significado de textos en español.
    
    Args:
        candidatos: Lista de textos generados por el modelo
        referencias: Lista de textos de referencia (ground truth)
        
    Returns:
        Array con scores de similitud de coseno (rango: -1 a 1, típicamente 0 a 1)
        Valores cercanos a 1 indican alta similitud semántica
    """
    # Calculate embeddings
    embeddings_candidatos = model_xlm.encode(candidatos)
    embeddings_referencias = model_xlm.encode(referencias)
    
    # Calculate the embedding similarities
    similarities = []
    for emb_cand, emb_ref in zip(embeddings_candidatos, embeddings_referencias):
        # Calculate pairwise similarity
        sim = model_xlm.similarity(emb_cand, emb_ref)
        # Extract scalar value from tensor
        similarities.append(float(sim))
    
    return np.array(similarities)

def compute_scibeto_similarity(candidatos: List[str], referencias: List[str]) -> np.ndarray:
    """
        Calcula similitud de coseno entre candidatos y referencias usando SciBETO-base.
        Args:
        candidatos: Lista de textos generados por el modelo
        referencias: Lista de textos de referencia (ground truth)
        
    Returns:
        Array con scores de similitud de coseno (rango: -1 a 1, típicamente 0 a 1)
        Valores cercanos a 1 indican alta similitud semántica
    """
    
    embeddings_candidatos = model_scibeto.encode(candidatos)  # Sin convert_to_tensor
    embeddings_referencias = model_scibeto.encode(referencias)
    
    similarities = []
    for emb_cand, emb_ref in zip(embeddings_candidatos, embeddings_referencias):
        sim = model_scibeto.similarity(emb_cand, emb_ref)
        similarities.append(float(sim))
    
    return np.array(similarities)

def print_sbert_stats(similarities: np.ndarray, model_name: str = ""):
    """
    Imprime estadísticas de similitud de Sentence-BERT.
    
    Args:
        similarities: Array con scores de similitud
        model_name: Nombre del modelo evaluado (opcional)
    """
    mean_sim = np.mean(similarities)
    std_sim = np.std(similarities)
    min_sim = np.min(similarities)
    max_sim = np.max(similarities)
    
    print(f"\n{'='*60}")
    print(f"Estadísticas Sentence-BERT{' - ' + model_name if model_name else ''}")
    print(f"{'='*60}")
    print(f"Media:        {mean_sim:.4f}")
    print(f"Desv. Est.:   {std_sim:.4f}")
    print(f"Mínimo:       {min_sim:.4f}")
    print(f"Máximo:       {max_sim:.4f}")
    print(f"{'='*60}\n")
