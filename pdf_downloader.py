import requests
import fitz # PyMuPDF
import os
import time

# Pasta para salvar
if not os.path.exists("pdfs_baixados"):
    os.mkdir("pdfs_baixados")

HEADERS = {
    "User-Agent": "PesquisaUniversitaria/1.0 (mailto:C3007819@fgv.edu.br)"
}

def get_pdf_link_unpaywall(doi):
    """Pergunta ao Unpaywall se existe uma versão gratuita legal"""
    try:
        # Unpaywall API gratuita
        url = f"https://api.unpaywall.org/v2/{doi}?email=C3007819@fgv.edu.br"
        r = requests.get(url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            # Verifica se tem localização de Open Access
            if data.get('is_oa') and data.get('best_oa_location'):
                return data['best_oa_location'].get('url_for_pdf')
    except Exception as e:
        print(f"Erro Unpaywall: {e}")
    return None

def download_and_extract_text(doi):
    print(f"🔍 Procurando PDF para DOI: {doi}...")
    
    # 1. Tenta achar o link
    pdf_url = get_pdf_link_unpaywall(doi)
    
    if not pdf_url:
        print("   ❌ Nenhum link Open Access encontrado (Paywall?).")
        return None
    
    print(f"   ✅ Link encontrado: {pdf_url}")
    print("   ⬇️ Baixando...")
    
    try:
        # 2. Baixa o arquivo
        r = requests.get(pdf_url, headers=HEADERS, timeout=15, allow_redirects=True)
        if r.status_code == 200 and 'application/pdf' in r.headers.get('Content-Type', ''):
            filename = f"pdfs_baixados/{doi.replace('/', '_')}.pdf"
            
            with open(filename, 'wb') as f:
                f.write(r.content)
            
            # 3. Lê o texto do PDF baixado
            print("   📖 Extraindo texto...")
            doc = fitz.open(filename)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            
            return full_text
        else:
            print(f"   ❌ Falha no download. Status: {r.status_code}")
    except Exception as e:
        print(f"   ❌ Erro no download: {e}")
        
    return None

# --- TESTE COM UM DOI QUE SABEMOS QUE É OPEN ACCESS ---
if __name__ == "__main__":
    # Exemplo: Um artigo da PLOS ONE (Geralmente Open Access)
    doi_teste = "10.1371/journal.pone.0266500" 
    
    texto = download_and_extract_text(doi_teste)
    
    if texto:
        print("\n" + "="*40)
        print(f"TEXTO EXTRAÍDO ({len(texto)} caracteres):")
        print(texto[:500] + "...") # Mostra o começo
    else:
        print("Não rolou.")