import google.generativeai as genai
import os

# 1. Cole sua chave aqui para testar
CHAVE = "CHAVE_API_AQUI"

print("--- INICIANDO TESTE DE CONEXÃO ---")

try:
    genai.configure(api_key=CHAVE)
    
    # Teste 1: Texto (LLM)
    print("Testando Gemini 2.5 Flash...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Olá, você está me ouvindo?")
    print(f"✅ Texto OK! Resposta: {response.text[:20]}...")

    # Teste 2: Embeddings (O que o LightRAG usa)
    print("\nTestando Modelo de Embedding...")
    embed = genai.embed_content(
        model="models/text-embedding-004",
        content="Teste de vetorização",
        task_type="retrieval_document"
    )
    print(f"✅ Embedding OK! Tamanho do vetor: {len(embed['embeddings'])}")
    
    print("\n🚀 TUDO CERTO! Sua chave está funcionando perfeitamente.")

except Exception as e:
    print(f"\n❌ ERRO DETECTADO: {e}")
    if "400" in str(e):
        print("Causa provável: Chave API inválida ou mal copiada.")
    elif "429" in str(e):
        print("Causa provável: Limite de cota atingido (muitas requisições).")
    elif "not found" in str(e).lower():
        print("Causa provável: O modelo selecionado não está disponível na sua região ou conta.")
