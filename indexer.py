import os
import glob
import json
import re

# --- CONFIGURE AQUI ---
# Onde estão os seus 40.000 json?
CORPUS_DIR = "../json" 
OUTPUT_INDEX = "mega_indice.json"

def normalize_title(title):
    """Limpa o título para facilitar o match (remove pontuação, minúsculas)"""
    if not title: return ""
    # Remove tudo que não é letra ou número e põe minúsculo
    return re.sub(r'[^a-z0-9]', '', title.lower())

def create_local_index():
    files = glob.glob(os.path.join(CORPUS_DIR, "*.json"))
    print(f"📦 Encontrados {len(files)} arquivos. Criando índice...")

    index = {}
    count = 0

    for f_path in files:
        try:
            with open(f_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Tenta achar o título e o abstract DO PRÓPRIO ARQUIVO
            # (A estrutura pode variar, ajuste conforme seu JSON)
            metadata = data.get('metadata', {})
            title = metadata.get('title')
            
            # Se não achou em metadata, tenta na raiz (alguns JSONs variam)
            if not title: title = data.get('title')
            
            # Pega o Abstract
            abstract = data.get('abstract')
            # Fallback: Se não tem abstract explícito, pega o primeiro parágrafo do texto
            if not abstract and data.get('body_text'):
                abstract = data['body_text'][0].get('text', '')[:1000] # Limita tamanho

            if title and abstract:
                # Cria uma chave simplificada para busca rápida
                clean_key = normalize_title(title)
                
                # Salva no índice
                index[clean_key] = {
                    "original_title": title,
                    "abstract": abstract,
                    "file": os.path.basename(f_path)
                }
                count += 1
                
        except Exception as e:
            # Ignora arquivos corrompidos
            pass
            
        if count % 1000 == 0:
            print(f"   Processados: {count}...")

    print(f"\n✅ Índice criado com {len(index)} artigos.")
    print(f"💾 Salvando em {OUTPUT_INDEX}...")
    
    with open(OUTPUT_INDEX, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)

if __name__ == "__main__":
    create_local_index()