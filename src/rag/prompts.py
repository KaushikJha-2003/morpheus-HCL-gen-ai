"""
Prompt template utilities for different personas.
"""
from langchain_core.prompts import PromptTemplate
from config.settings import PERSONAS


def create_prompt_template(persona: str) -> PromptTemplate:
    """
    Create a prompt template based on the selected persona.
    
    Args:
        persona: Selected persona name
        
    Returns:
        PromptTemplate object
    """
    instruction = PERSONAS.get(persona, "You are a helpful AI assistant.")
    
    template = f"""
{instruction}

Use ONLY the context below to answer.

CONTEXT:
{{context}}

QUESTION:
{{question}}

ANSWER:
"""
    
    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

