import os
import asyncio
import google.generativeai as genai
from lightrag import LightRAG, QueryParam
from lightrag.kg.shared_storage import initialize_pipeline_status

# 1. Configuração da API
CHAVE_MESTRA = "YOUR_API_KEY"
os.environ["GOOGLE_API_KEY"] = CHAVE_MESTRA
genai.configure(api_key=CHAVE_MESTRA)

# 2. FUNÇÃO LLM (Agora usando o Gemini 2.5 Flash)
async def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs) -> str:
    # Ajustado para o modelo que você confirmou que possui
    model = genai.GenerativeModel('gemini-2.5-flash')
    full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
    response = await model.generate_content_async(full_prompt)
    return response.text

# 3. FUNÇÃO EMBEDDING (Com correção para o erro 'embeddings')
async def embedding_func(texts: list[str]) -> list[list[float]]:
    try:
        # Usamos o modelo 004 que é o padrão atual para vetores
        result = genai.embed_content(
            model="models/text-embedding-004", 
            content=texts,
            task_type="retrieval_document"
        )
        
        # Correção para o erro que você teve: 
        # O Google pode retornar 'embeddings' ou apenas 'embedding'
        if 'embeddings' in result:
            return result['embeddings']
        return result['embedding']
        
    except Exception as e:
        print(f"Erro no processo de Embedding: {e}")
        return []

# O modelo text-embedding-004 tem 768 dimensões
llm_model_func.func = llm_model_func
embedding_func.embedding_dim = 768 

# 4. INICIALIZAÇÃO
rag = LightRAG(
    working_dir="./dickens",
    llm_model_func=llm_model_func,
    embedding_func=embedding_func
)

async def main():
    # Inicialização obrigatória das pastas
    await rag.initialize_storages()
    await initialize_pipeline_status()

    if os.path.exists("./book.txt"):
        with open("./book.txt", "r", encoding="utf-8") as f:
            print(f"🚀 Iniciando indexação com Gemini 2.5 Flash...")
            await rag.ainsert(f.read())
        
        print("\n--- RESPOSTA ---")
        # Modo híbrido para melhor qualidade
        print(await rag.aquery("Faça um resumo detalhado do texto", param=QueryParam(mode="hybrid")))
    else:
        print("Arquivo 'book.txt' não encontrado.")

if __name__ == "__main__":
    asyncio.run(main())
