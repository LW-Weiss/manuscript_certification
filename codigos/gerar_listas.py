import os
import json

def extrair_dados_artigo(filepath):
    """
    Lê um arquivo JSON de um artigo (formato S2ORC) e retorna um dicionário
    com a estrutura de referências detalhadas que você especificou.
    """
    
    resultado = {
        "Autores": [],
        "Palavras-Chave": [],
        "Referências": []  # Esta será uma lista de dicionários
    }

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{filepath}'")
        return None
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{filepath}' não é um JSON válido.")
        return None

    # Extrai Autores e Palavras-Chave do artigo principal
    metadata = data.get('metadata', {})
    if metadata:
        lista_de_autores_obj = metadata.get('authors', [])
        autores_formatados = [f"{author.get('first', '')} {author.get('last', '')}".strip() for author in lista_de_autores_obj]
        resultado["Autores"] = autores_formatados
        resultado["Palavras-Chave"] = metadata.get('keywords', [])

    # Lógica para extrair as referências na estrutura de dicionário
    bib_entries = data.get('bib_entries', {})
    if bib_entries:
        lista_de_referencias_estruturadas = []
        for ref_data in bib_entries.values():
            if not ref_data:
                continue

            # 1. Extrai os autores da referência para uma lista
            autores_ref_obj = ref_data.get('authors', [])
            lista_autores_ref = [f"{author.get('last', '')}, {author.get('first', '')}".strip() for author in autores_ref_obj]

            # 2. Monta a string de páginas
            paginas_str = ""
            volume = ref_data.get('volume')
            pagina_inicial = ref_data.get('firstpage')
            pagina_final = ref_data.get('lastpage')
            
            if volume:
                paginas_str += f"Vol. {volume}"
            if pagina_inicial:
                if paginas_str: paginas_str += ", "
                paginas_str += f"pp. {pagina_inicial}-{pagina_final}"

            # 3. Cria o dicionário para esta referência com as chaves exatas
            ref_dict = {
                "Autores Referência": lista_autores_ref,
                "Artigo Referência": ref_data.get('title', 'Título não disponível'),
                "Local": paginas_str if paginas_str else "Informação de página não disponível",
                "DoI": ref_data.get('doi', 'DOI não disponível')
            }
            
            lista_de_referencias_estruturadas.append(ref_dict)
            
        resultado["Referências"] = lista_de_referencias_estruturadas
        
    return resultado


# --- BLOCO DE EXECUÇÃO ---
if __name__ == "__main__":
    JSON_INPUT_FOLDER = "mini_corpus_json"
    ARQUIVO_JSON_EXEMPLO = "S0001706X13001861.json"
    
    caminho_completo = os.path.join(JSON_INPUT_FOLDER, ARQUIVO_JSON_EXEMPLO)
    
    dados_extraidos = extrair_dados_artigo(caminho_completo)
    
    if dados_extraidos:
        print("--- DADOS EXTRAÍDOS (ESTRUTURA CONFIRMADA) ---")
        print(json.dumps(dados_extraidos, indent=4, ensure_ascii=False))