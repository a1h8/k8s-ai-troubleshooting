"""
Interface pour soumettre des extraits à un LLM et contrôler l'intégrité.
"""
import openai

def ask_llm(prompt, api_key, model="gpt-4"):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=512
    )
    return response['choices'][0]['message']['content']

# Exemple de contrôle d'intégrité (à adapter selon la politique interne)
def check_integrity(context, llm_response):
    # Implémenter des règles pour vérifier la cohérence, la non-divulgation, etc.
    # Par exemple, vérifier la présence de termes interdits ou incohérents
    return True  # Stub à personnaliser
