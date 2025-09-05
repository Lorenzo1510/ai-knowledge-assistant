import os

from app.utils.llm_class import LLMPredictor


def llm_predict(context: str, question: str, 
               max_tokens: int = 512, 
               temperature: float = 0.7) -> str:
    """
    Funzione standalone per predizioni LLM
    Mantiene la compatibilità con il codice esistente
    """
    # Crea un'istanza del predictor
    predictor = LLMPredictor()
    return predictor.llm_predict(context, question, max_tokens, temperature)