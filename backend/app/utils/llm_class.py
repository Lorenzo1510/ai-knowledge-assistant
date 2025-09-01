import os
from huggingface_hub import InferenceClient
from typing import Optional, List, Dict, Any
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMPredictor:
    """
    Classe per gestire predizioni con modelli LLM di Hugging Face
    """
    
    def __init__(self, model_name: str = "meta-llama/Meta-Llama-3-8B-Instruct", 
                 api_token: Optional[str] = None):
        """
        Inizializza il predictor
        
        Args:
            model_name: Nome del modello Hugging Face
            api_token: Token API (se None, usa variabile d'ambiente)
        """
        self.model_name = model_name
        self.api_token = api_token or os.getenv("HUGGINGFACEHUB_API_TOKEN")
        
        if not self.api_token:
            logger.warning("Token API non trovato. Funzionalità potrebbero essere limitate.")
        
        # Inizializza il client
        self.client = InferenceClient(token=self.api_token)
        
        # Sistema prompt di default
        self.system_prompt = "Sei un assistente AI esperto che risponde in italiano in modo preciso e utile."
    
    def set_system_prompt(self, prompt: str) -> None:
        """Imposta un nuovo system prompt"""
        self.system_prompt = prompt
    
    def create_messages(self, context: str, question: str, 
                       system_prompt: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Crea la lista di messaggi per la chat completion
        
        Args:
            context: Contesto per rispondere
            question: Domanda dell'utente
            system_prompt: System prompt personalizzato (opzionale)
        
        Returns:
            Lista di messaggi formattata
        """
        sys_prompt = system_prompt or self.system_prompt
        
        # Prompt dell'utente più strutturato
        user_content = f"""Ho bisogno di una risposta basata sul seguente contesto.

                            **Contesto:**
                            {context}

                            **Domanda:**
                            {question}

                            Fornisci una risposta accurata e completa basandoti esclusivamente sul contesto fornito."""

        return [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_content}
        ]
    
    def llm_predict(self, context: str, question: str, 
                   max_tokens: int = 512, 
                   temperature: float = 0.7,
                   system_prompt: Optional[str] = None) -> str:
        """
        Predice una risposta usando il modello LLM
        
        Args:
            context: Contesto su cui basare la risposta
            question: Domanda da porre
            max_tokens: Numero massimo di token da generare
            temperature: Temperatura per il campionamento (0.0-1.0)
            system_prompt: System prompt personalizzato (opzionale)
        
        Returns:
            Risposta generata dal modello
        """
        if not context.strip():
            return "Errore: Il contesto non può essere vuoto."
        
        if not question.strip():
            return "Errore: La domanda non può essere vuota."
        
        try:
            # Crea i messaggi
            messages = self.create_messages(context, question, system_prompt)
            
            # Chiamata al modello
            completion = self.client.chat_completion(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
            )
            
            # Estrai la risposta
            response_text = completion.choices[0].message.content
            
            if not response_text or response_text.strip() == "":
                return "Il modello non ha generato una risposta valida."
            
            return response_text.strip()
            
        except Exception as e:
            logger.error(f"Errore nella predizione: {e}")
            return f"Errore durante la generazione: {e}"
    
    def llm_predict_batch(self, contexts_questions: List[tuple], 
                         max_tokens: int = 512, 
                         temperature: float = 0.7) -> List[str]:
        """
        Predice risposte per multiple coppie context-question
        
        Args:
            contexts_questions: Lista di tuple (context, question)
            max_tokens: Numero massimo di token da generare
            temperature: Temperatura per il campionamento
        
        Returns:
            Lista di risposte generate
        """
        results = []
        for i, (context, question) in enumerate(contexts_questions):
            logger.info(f"Processando richiesta {i+1}/{len(contexts_questions)}")
            result = self.llm_predict(context, question, max_tokens, temperature)
            results.append(result)
        
        return results