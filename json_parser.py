import json
import glob
import os
from typing import List, Dict, Any

def load_claims_from_json(json_path: str) -> List[Dict[str, Any]]:
    print(f"\n LENDO ARQUIVO (MODO SENTENCE/REFOFFSETS): {os.path.basename(json_path)}")
    
    if not os.path.exists(json_path):
        print(f"❌ Arquivo não encontrado: {json_path}")
        return []

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    bib_entries = data.get('bib_entries', {})
    body_text = data.get('body_text', [])
    
    extracted_claims = []
    
    print(f"📚 Bibliografia: {len(bib_entries)} itens.")
    print(f"📄 Blocos de texto: {len(body_text)}")

    for block in body_text:
        text = block.get('sentence', '')
        refs = block.get('refoffsets', {})
        
        # Filtra textos muito curtos para evitar ruído
        if refs and len(text) > 20:
            for ref_id in refs.keys():
                # Verifica se a referência existe na bibliografia
                if ref_id in bib_entries:
                    ref_data = bib_entries[ref_id]
                    
                    # Se ref_data for None (nulo), pula para o próximo
                    if not ref_data:
                        continue
                        
                    title = ref_data.get('title', 'Unknown Title')
                    
                    # --- AQUI ESTÁ A CORREÇÃO MÁGICA ---
                    # Pegamos o DOI se ele existir nos metadados da referência
                    doi = ref_data.get('doi') 
                    
                    extracted_claims.append({
                        "claim_text": text,
                        "cited_paper_title": title,
                        "cited_doi": doi,  # <--- Agora o DOI é salvo e passado adiante!
                        "cited_ref_id": ref_id
                    })

    print(f"✅ SUCESSO: {len(extracted_claims)} pares extraídos corretamente.")
    return extracted_claims

if __name__ == "__main__":
    # Teste rápido
    arquivos = glob.glob("corpora/mini_corpus_json/*.json")
    if arquivos:
        claims = load_claims_from_json(arquivos[0])
        if claims:
            print("\n--- Exemplo de Extração ---")
            print(f"📝 Frase: {claims[0]['claim_text'][:80]}...")
            print(f"🔗 Cita: {claims[0]['cited_paper_title']}")
            print(f"🆔 DOI: {claims[0].get('cited_doi', 'N/A')}") # Teste para ver se pegou
    else:
        print("❌ Nenhum JSON encontrado.")