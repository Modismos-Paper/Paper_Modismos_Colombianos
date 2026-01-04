"""
chrF: Character n-gram F-score
Métrica robusta a variaciones morfológicas y errores ortográficos
"""

import numpy as np
from typing import List
import warnings
warnings.filterwarnings('ignore')

def compute_chrf_score(candidato: str, referencia: str, n: int = 6, beta: int = 2) -> float:
    """
    Calcula chrF score entre dos textos.
    
    chrF (Character n-gram F-score) mide la similitud a nivel de caracteres,
    siendo más robusto a variaciones morfológicas y errores ortográficos que
    métricas basadas en palabras.
    
    Args:
        candidato: Texto generado por el modelo
        referencia: Texto de referencia (ground truth)
        n: Tamaño máximo de n-gramas de caracteres (default: 6)
        beta: Peso para el balance entre precisión y recall (default: 2)
              beta=2 da más peso al recall
        
    Returns:
        chrF score (rango: 0 a 1, valores más altos indican mayor similitud)
    """
    def get_char_ngrams(text: str, n: int) -> set:
        """Extrae n-gramas de caracteres de un texto."""
        # Remover espacios extras y normalizar
        text = ' '.join(text.split())
        ngrams = set()
        for i in range(len(text) - n + 1):
            ngrams.add(text[i:i+n])
        return ngrams
    
    # Calcular precision y recall para cada tamaño de n-grama
    total_precision = 0
    total_recall = 0
    num_ngrams = 0
    
    for ngram_size in range(1, n + 1):
        # Obtener n-gramas del candidato y referencia
        cand_ngrams = get_char_ngrams(candidato, ngram_size)
        ref_ngrams = get_char_ngrams(referencia, ngram_size)
        
        if len(cand_ngrams) == 0 or len(ref_ngrams) == 0:
            continue
        
        # Calcular intersección
        common_ngrams = cand_ngrams & ref_ngrams
        
        # Precision: ¿Qué proporción de n-gramas del candidato están en la referencia?
        precision = len(common_ngrams) / len(cand_ngrams) if len(cand_ngrams) > 0 else 0
        
        # Recall: ¿Qué proporción de n-gramas de la referencia están en el candidato?
        recall = len(common_ngrams) / len(ref_ngrams) if len(ref_ngrams) > 0 else 0
        
        total_precision += precision
        total_recall += recall
        num_ngrams += 1
    
    if num_ngrams == 0:
        return 0.0
    
    # Promediar precision y recall
    avg_precision = total_precision / num_ngrams
    avg_recall = total_recall / num_ngrams
    
    # Calcular F-score con beta
    if avg_precision + avg_recall == 0:
        return 0.0
    
    beta_squared = beta ** 2
    chrf = (1 + beta_squared) * (avg_precision * avg_recall) / (beta_squared * avg_precision + avg_recall)
    
    return chrf


def compute_chrf_batch(candidatos: List[str], referencias: List[str], n: int = 6, beta: int = 2) -> np.ndarray:
    """
    Calcula chrF score para múltiples pares de textos.
    
    Args:
        candidatos: Lista de textos generados por el modelo
        referencias: Lista de textos de referencia (ground truth)
        n: Tamaño máximo de n-gramas de caracteres (default: 6)
        beta: Peso para el balance entre precisión y recall (default: 2)
        
    Returns:
        Array con chrF scores (rango: 0 a 1)
    """
    scores = []
    for cand, ref in zip(candidatos, referencias):
        score = compute_chrf_score(cand, ref, n=n, beta=beta)
        scores.append(score)
    
    return np.array(scores)


def print_chrf_stats(scores: np.ndarray, model_name: str = ""):
    """
    Imprime estadísticas de chrF.
    
    Args:
        scores: Array con chrF scores
        model_name: Nombre del modelo evaluado (opcional)
    """
    mean_score = np.mean(scores)
    std_score = np.std(scores)
    min_score = np.min(scores)
    max_score = np.max(scores)
    
    print(f"\n{'='*60}")
    print(f"Estadísticas chrF{' - ' + model_name if model_name else ''}")
    print(f"{'='*60}")
    print(f"Media:        {mean_score:.4f}")
    print(f"Desv. Est.:   {std_score:.4f}")
    print(f"Mínimo:       {min_score:.4f}")
    print(f"Máximo:       {max_score:.4f}")
    print(f"{'='*60}\n")
