import pandas as pd
import os
import requests
import fitz  # PyMuPDF
import asyncio
import ollama
import time
import re
import csv
from semanticscholar import SemanticScholar

# --- CONFIGURAÇÕES ---
INPUT_CSV = "relatorio_final_hibrido.csv"  # Pode usar o output anterior para tentar preencher o que faltou
# Se for a primeira vez rodando a fase 2, use "relatorio_direto_ollama.csv"
if not os.path.exists(INPUT_CSV):
    INPUT_CSV = "relatorio_direto_ollama.csv"

OUTPUT_CSV = "relatorio_final_v2.csv"
PDF_DIR = "pdfs_baixados"

# SEUS DADOS
EMAIL_CONTACT = "C3007819@fgv.edu.br"
HEADERS = {"User-Agent": f"CitationVerifier/Hybrid (mailto:{EMAIL_CONTACT})"}
OLLAMA_MODEL = "llama3.1"

# API SECUNDÁRIA
sch = SemanticScholar(timeout=10)

if not os.path.exists(PDF_DIR):
    os.mkdir(PDF_DIR)

# --- 1. FUNÇÃO PARA DESCOBRIR DOI FALTANTE ---
def fetch_doi_from_title(title):
    """Se não tem DOI, pergunta pro Crossref quem é esse artigo."""
    if not title or len(str(title)) < 5: return None
    try:
        # Limpa o título para busca
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', str(title))
        url = "https://api.crossref.org/works"
        params = {"query.bibliographic": clean, "rows": 1}
        r = requests.get(url, params=params, headers=HEADERS, timeout=5)
        if r.status_code == 200:
            items = r.json().get('message', {}).get('items', [])
            if items:
                found_title = items[0].get('title', [''])[0]
                # Verifica se o título achado é parecido (simples checagem de tamanho)
                if abs(len(found_title) - len(title)) < 50: 
                    print(f"         ✨ DOI descoberto via Crossref: {items[0].get('DOI')}")
                    return items[0].get('DOI')
    except: pass
    return None

# --- 2. FUNÇÕES DE DOWNLOAD (UNPAYWALL + SEMANTIC SCHOLAR) ---
def get_pdf_link_unpaywall(doi):
    try:
        url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL_CONTACT}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get('is_oa') and data.get('best_oa_location'):
                return data['best_oa_location'].get('url_for_pdf')
    except: pass
    return None

def get_pdf_link_semanticscholar(doi):
    """Tenta achar link via Semantic Scholar (S2)"""
    try:
        paper = sch.get_paper(doi, fields=['openAccessPdf'])
        if paper and paper.openAccessPdf:
            return paper.openAccessPdf['url']
    except: pass
    return None

# --- SUBSTITUA A FUNÇÃO download_or_read_pdf POR ESTA VERSÃO (V3) ---

def normalize_string_for_match(s):
    """Remove tudo que não é letra/número e põe minúsculo para comparar"""
    if not s: return ""
    return re.sub(r'[^a-z0-9]', '', str(s).lower())

def download_or_read_pdf(doi, title):
    """
    Versão V3: Busca Universal (Cobre arquivos com nomes longos/códigos extras)
    """
    # 1. Preparação dos nomes para busca
    clean_doi = normalize_string_for_match(doi) if doi else "sem_doi"
    
    # Limpa o título, mas garante que não fique vazio
    clean_title = normalize_string_for_match(title)
    # Pegamos só os primeiros 50 caracteres do título limpo para comparar
    # (Isso ajuda se o arquivo tiver o título cortado)
    short_clean_title = clean_title[:50] if len(clean_title) > 50 else clean_title
    
    try:
        files_in_dir = os.listdir(PDF_DIR)
    except FileNotFoundError:
        return None

    target_file = None

    # --- ESTRATÉGIA 1: BUSCA LOCAL (PRIORIDADE MÁXIMA) ---
    print(f"      🔎 Procurando na pasta por título similar...")
    
    for f in files_in_dir:
        if not f.lower().endswith(".pdf"): continue
        
        # Limpa o nome do arquivo da pasta
        clean_filename = normalize_string_for_match(f.replace(".pdf", ""))
        
        # LÓGICA DE MATCH (CRUZAMENTO TOTAL)
        
        # A) Match por DOI (Se o arquivo tiver o DOI no nome)
        match_doi = (clean_doi in clean_filename) and (len(clean_doi) > 5)
        
        # B) Match por TÍTULO (Mão Dupla)
        # 1. O arquivo está dentro do título? (Ex: arquivo 'study_design.pdf' vs Título 'Study Design in...')
        file_in_title = (clean_filename in clean_title) and (len(clean_filename) > 15)
        
        # 2. O título (ou parte dele) está dentro do arquivo? (Ex: Título 'Study Design' vs Arquivo 'Study Design - versao_final.pdf')
        title_in_file = (short_clean_title in clean_filename) and (len(short_clean_title) > 15)

        if match_doi:
            print(f"         ✅ Match por DOI no arquivo: {f}")
            target_file = os.path.join(PDF_DIR, f)
            break
        
        if file_in_title or title_in_file:
            print(f"         ✅ Match por TÍTULO no arquivo: {f}")
            target_file = os.path.join(PDF_DIR, f)
            break

    # Se achou localmente, lê e retorna
    if target_file:
        return read_pdf_text(target_file)

    # --- ESTRATÉGIA 2: TENTA BAIXAR (Se não achou local) ---
    if doi and str(doi) != "nan" and len(str(doi)) > 5:
        print(f"      ⬇️ Não achei local. Buscando online DOI: {doi}...")
        
        # Tenta Unpaywall
        url = get_pdf_link_unpaywall(doi)
        source_name = "Unpaywall"
        
        # Tenta Semantic Scholar
        if not url:
            url = get_pdf_link_semanticscholar(doi)
            source_name = "SemanticScholar"
        
        if url:
            try:
                # Salva com nome seguro (DOI limpo) para achar fácil depois
                safe_filename = clean_doi + ".pdf"
                save_path = os.path.join(PDF_DIR, safe_filename)
                
                print(f"         🔗 Link ({source_name}): {url[:40]}...")
                r = requests.get(url, headers=HEADERS, timeout=15)
                
                if r.status_code == 200 and 'pdf' in r.headers.get('Content-Type', '').lower():
                    with open(save_path, 'wb') as f: f.write(r.content)
                    print("         ✅ Download Sucesso!")
                    return read_pdf_text(save_path)
                else:
                    print(f"         ❌ Link falhou (Status {r.status_code}).")
            except: print("         ❌ Erro na conexão.")
        else:
            print("         ⚠️ Sem link nas APIs.")

    return None

def read_pdf_text(filepath):
    try:
        doc = fitz.open(filepath)
        text = ""
        for page in doc: text += page.get_text()
        return text
    except: return None

# --- 3. FUNÇÃO DA IA ---
async def verify_full_paper(claim, full_text):
    truncated_text = full_text[:250000] # Limite seguro
    prompt = f"""You are a scientific fact-checker.
    CLAIM: "{claim}"
    
    Use the FULL TEXT below to verify the claim.
    
    FULL TEXT:
    "{truncated_text}"
    
    Does the FULL TEXT support the CLAIM?
    
    Reply STRICTLY in this format:
    VEREDITO: [SUPPORTIVE / CONTRADICTORY / NOT_MENTIONED]
    EXPLICAÇÃO: [Explanation in Portuguese]
    """
    try:
        response = await asyncio.to_thread(
            ollama.chat, model=OLLAMA_MODEL, messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']
    except Exception as e: return f"Error: {e}"

# --- PIPELINE PRINCIPAL ---
async def run_retry_pipeline():
    print(f"📂 Lendo: {INPUT_CSV}")
    df = pd.read_csv(INPUT_CSV, sep=';', encoding='utf-8-sig', quotechar='"')
    
    # Filtra (NOT_MENTIONED, SKIPPED ou onde DOI está vazio mas deveria ter)
    # Se quiser forçar rodar em tudo que está vazio de DOI, ajuste aqui
    mask = df['Veredito'].str.contains('NOT_MENTIONED', case=False, na=False) | \
           df['Veredito'].str.contains('SKIPPED', case=False, na=False)
    
    to_retry = df[mask].copy()
    print(f"🎯 Linhas para tentar recuperar: {len(to_retry)}")
    
    count_saved = 0
    
    for index, row in to_retry.iterrows():
        print(f"\n[{index+1}] Claim: {row['Claim'][:40]}...")
        
        doi = row.get('DOI', None)
        title = row.get('Titulo_Artigo', row.get('Fonte', ''))
        
        # 1. Se não tem DOI, tenta descobrir agora!
        if pd.isna(doi) or str(doi).strip() == "":
            print(f"      🔍 DOI faltando. Pesquisando título no Crossref...")
            new_doi = fetch_doi_from_title(title)
            if new_doi:
                doi = new_doi
                df.at[index, 'DOI'] = new_doi # Salva no DF principal
        
        # 2. Tenta baixar ou ler PDF
        full_text = download_or_read_pdf(doi, title)
        
        if full_text:
            print(f"      📖 Texto lido ({len(full_text)} chars). IA avaliando...")
            resp = await verify_full_paper(row['Claim'], full_text)
            
            new_veredito = "ERROR"
            new_explicacao = resp
            if "VEREDITO:" in resp:
                try:
                    parts = resp.split("EXPLICAÇÃO:")
                    new_veredito = parts[0].replace("VEREDITO:", "").strip()
                    new_explicacao = parts[1].strip() if len(parts) > 1 else ""
                except: pass
            
            print(f"      ⚡ Novo Resultado: {new_veredito}")
            
            if "NOT_MENTIONED" not in new_veredito and "ERROR" not in new_veredito:
                count_saved += 1
                
            df.at[index, 'Veredito'] = new_veredito
            df.at[index, 'Explicação'] = f"[FULL PAPER] {new_explicacao}"
            df.at[index, 'Fonte'] = "PDF COMPLETO"
        else:
            print("      💨 Ainda sem PDF.")

    df.to_csv(OUTPUT_CSV, index=False, sep=';', quoting=csv.QUOTE_ALL, encoding='utf-8-sig')
    print(f"\n✅ Finalizado! {count_saved} itens recuperados/melhorados.")
    print(f"💾 Salvo em: {OUTPUT_CSV}")

if __name__ == "__main__":
    asyncio.run(run_retry_pipeline())