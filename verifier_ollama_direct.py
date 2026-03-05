import os
import glob
import json
import asyncio
import time
import random
import re
import requests
import difflib
import csv
import numpy as np
import pandas as pd
import ollama
from concurrent.futures import ThreadPoolExecutor
from semanticscholar import SemanticScholar
from json_parser import load_claims_from_json

# --- CONFIGURAÇÕES ---
TARGET_DIR = "corpora/mini_corpus_json"
INDEX_FILE = "mega_indice.json"           
CACHE_FILE = "biblioteca_cache.json"      
OUTPUT_FILE = "relatorio_direto_ollama.csv"

# IDENTIFICAÇÃO
EMAIL_CONTACT = "pesquisa@universidade.br" 
HEADERS = {"User-Agent": f"CitationVerifier/Direct (mailto:{EMAIL_CONTACT})"}

# OLLAMA
OLLAMA_MODEL_NAME = "llama3.1"
MAX_WEB_WORKERS = 10 

# --- UTILITÁRIOS ---
def clean_text_for_csv(text):
    if not text: return ""
    text = str(text).replace('\n', ' ').replace('\r', '').replace('\t', ' ')
    return " ".join(text.split())

def clean_title_aggressive(text):
    if not text: return ""
    text = re.sub(r'\(\d{4}\)', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return " ".join(text.split()).strip()

def normalize_key(text):
    if not text: return ""
    return re.sub(r'[^a-z0-9]', '', text.lower())

def load_json_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_json_file(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def reconstruct_openalex_abstract(inverted_index):
    if not inverted_index: return None
    try:
        max_index = max(max(positions) for positions in inverted_index.values())
        text_list = [""] * (max_index + 1)
        for word, positions in inverted_index.items():
            for pos in positions: text_list[pos] = word
        return " ".join(text_list)
    except: return None

# --- BUSCA WEB ---
sch = SemanticScholar(timeout=10)

def search_crossref(title):
    try:
        url = "https://api.crossref.org/works"
        params = {"query.bibliographic": title, "rows": 1}
        r = requests.get(url, params=params, headers=HEADERS, timeout=5)
        if r.status_code == 200:
            items = r.json().get('message', {}).get('items', [])
            if items: return items[0].get('DOI')
    except: pass
    return None

def fetch_openalex_full(title, doi=None):
    try:
        query = f"doi:{doi}" if doi else f"title.search:{title}"
        url = f"https://api.openalex.org/works?filter={query}&per_page=1"
        r = requests.get(url, headers=HEADERS, timeout=8)
        if r.status_code == 200:
            data = r.json()
            results = data.get('results', [])
            if results:
                item = results[0]
                inverted = item.get('abstract_inverted_index')
                abstract = reconstruct_openalex_abstract(inverted)
                found_doi = item.get('doi')
                if found_doi: found_doi = found_doi.replace("https://doi.org/", "")
                return abstract, found_doi
    except: pass
    return None, None

def fetch_from_web_worker(item):
    time.sleep(random.uniform(0.5, 1.5))
    raw_title = item['cited_paper_title']
    doi = item.get('cited_doi')
    if not raw_title or len(raw_title) < 5: return None, None
    clean_query = clean_title_aggressive(raw_title)
    
    try:
        paper = None
        fields = ['title', 'abstract', 'tldr']
        if doi:
            try: paper = sch.get_paper(doi, fields=fields)
            except: pass
        if not paper:
            try: 
                results = sch.search_paper(clean_query, limit=1, fields=fields)
                if results: paper = results[0]
            except: pass

        if paper:
            content = paper.abstract if paper.abstract else (paper.tldr['text'] if paper.tldr else None)
            if content: return content, (doi if doi else raw_title)

        abstract_oa, doi_oa = fetch_openalex_full(clean_query, doi)
        if abstract_oa: return abstract_oa, (doi_oa if doi_oa else raw_title)

        if not doi:
            found_doi = search_crossref(clean_query)
            if found_doi:
                try:
                    paper = sch.get_paper(found_doi, fields=fields)
                    if paper and (paper.abstract or paper.tldr):
                        return (paper.abstract or paper.tldr['text']), found_doi
                except: pass
    except: pass
    return None, None

def download_wrapper(idx, item):
    return idx, fetch_from_web_worker(item)

# --- VERIFICADOR DIRETO ---
class DirectVerifier:
    def __init__(self):
        self.results_data = [] 
        print("📂 Carregando bases...")
        self.local_index = load_json_file(INDEX_FILE)
        self.web_cache = load_json_file(CACHE_FILE)
        self.local_keys_list = list(self.local_index.keys())
        self.norm_web_cache = {normalize_key(k): v for k, v in self.web_cache.items()}

    async def verify_claim_direct(self, claim, abstract):
        prompt = f"""You are a scientific fact-checker.
        CLAIM: "{claim}"
        SOURCE TEXT: "{abstract}"
        
        Does the SOURCE TEXT support the CLAIM?
        
        Instructions:
        1. Ignore spelling errors in the claim.
        2. If the text explicitly supports the claim, say SUPPORTIVE.
        3. If the text explicitly contradicts the claim, say CONTRADICTORY.
        4. If the text does not contain enough information, say NOT_MENTIONED.
        
        Reply STRICTLY in this format:
        VEREDITO: [SUPPORTIVE / CONTRADICTORY / NOT_MENTIONED]
        EXPLICAÇÃO: [Short explanation in Portuguese]
        """
        messages = [{'role': 'user', 'content': prompt}]
        try:
            # Thread para não travar enquanto o Ollama pensa
            response = await asyncio.to_thread(
                ollama.chat, 
                model=OLLAMA_MODEL_NAME, 
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            return f"Error: {e}"

    def find_content_aggressive(self, title, doi):
        search_key = normalize_key(title)
        if search_key in self.local_index: return self.local_index[search_key]['abstract'], "LOCAL 🏠"
        if len(search_key) > 15:
            matches = difflib.get_close_matches(search_key, self.local_keys_list, n=1, cutoff=0.85)
            if matches: return self.local_index[matches[0]]['abstract'], "LOCAL (Fuzzy) 🏠"
        if doi and doi in self.web_cache and self.web_cache[doi]: return self.web_cache[doi], "CACHE 💾"
        if search_key in self.norm_web_cache and self.norm_web_cache[search_key]: return self.norm_web_cache[search_key], "CACHE 💾"
        return None, None

    async def run_pipeline(self):
        files = glob.glob(os.path.join(TARGET_DIR, "*.json"))
        print(f"\n🚀 MODO DIRETO (SEM LIGHTRAG): {len(files)} ARQUIVOS.")
        
        global_start = time.time()

        for file_idx, target_file in enumerate(files):
            file_start_time = time.time()
            file_basename = os.path.basename(target_file)
            print(f"\n{'='*60}")
            print(f"📂 ARQUIVO [{file_idx+1}/{len(files)}]: {file_basename}")
            
            try: claims = load_claims_from_json(target_file)
            except: continue
            if not claims: continue

            # --- ETAPA 1: DOWNLOAD ---
            t0 = time.time()
            items_to_download = []
            resolved = {} 
            for i, item in enumerate(claims):
                c, s = self.find_content_aggressive(item['cited_paper_title'], item.get('cited_doi'))
                if c: resolved[i] = (c, s)
                else: items_to_download.append((i, item))

            if items_to_download:
                print(f"   🌐 Baixando {len(items_to_download)} itens...")
                with ThreadPoolExecutor(max_workers=MAX_WEB_WORKERS) as executor:
                    loop = asyncio.get_running_loop()
                    futures = [loop.run_in_executor(executor, download_wrapper, idx, item) for idx, item in items_to_download]
                    
                    completed = 0
                    sucessos = 0
                    for f in asyncio.as_completed(futures):
                        idx, (content, saved_key) = await f
                        completed += 1
                        if content:
                            resolved[idx] = (content, "INTERNET 🌍")
                            self.web_cache[saved_key if saved_key else claims[idx]['cited_paper_title']] = content
                            sucessos += 1
                        else:
                            resolved[idx] = (None, "NÃO ENCONTRADO ❌")
                            k = claims[idx].get('cited_doi') or claims[idx]['cited_paper_title']
                            self.web_cache[k] = None
                        print(f"      ⏳ {completed}/{len(items_to_download)} | Sucessos: {sucessos}", end="\r")
                if sucessos > 0: save_json_file(CACHE_FILE, self.web_cache)
                print("") 
            t_download = time.time() - t0

            # --- ETAPA 2: INFERÊNCIA ---
            t0 = time.time()
            print("   🧠 Verificando (Modo Direto)...")
            count_processed = 0
            
            for i, item in enumerate(claims):
                data = resolved.get(i)
                abstract = data[0] if data else None
                source = data[1] if data else "N/A"
                
                veredito = "SKIPPED"
                explicacao = "Restrito"
                
                if abstract:
                    count_processed += 1
                    resp = await self.verify_claim_direct(item['claim_text'], abstract)
                    
                    if "VEREDITO:" in resp:
                        try:
                            parts = resp.split("EXPLICAÇÃO:")
                            veredito = parts[0].replace("VEREDITO:", "").strip()
                            explicacao = parts[1].strip() if len(parts) > 1 else ""
                        except:
                            veredito = "FORMAT_ERROR"
                            explicacao = resp[:100]
                    else:
                        veredito = "CHECK_LOGS"
                        explicacao = resp[:100]
                
                explicacao = clean_text_for_csv(explicacao)
                veredito = clean_text_for_csv(veredito)
                
                status_icon = "⚪"
                if "SUPPORTIVE" in veredito: status_icon = "🟢"
                elif "CONTRADICTORY" in veredito: status_icon = "🔴"
                elif "NOT_MENTIONED" in veredito: status_icon = "🟡"
                
                if abstract:
                    print(f"      {status_icon} {veredito[:15]}...")

                self.results_data.append({
                    "Arquivo": file_basename,
                    "Claim": item['claim_text'],
                    "Veredito": veredito,
                    "Fonte": source,
                    "DOI": item.get('cited_doi', ''),  # Adicionado DOI ao CSV
                    "Titulo_Artigo": item['cited_paper_title'],
                    "Explicação": explicacao
                })
            t_inference = time.time() - t0
            
            pd.DataFrame(self.results_data).to_csv(
                OUTPUT_FILE, index=False, sep=';', quoting=csv.QUOTE_ALL, encoding='utf-8-sig'
            )

            file_total_time = time.time() - file_start_time
            print(f"\n📊 [BENCHMARK] {file_basename}")
            print(f"   🌍  Busca: {t_download:.2f}s")
            print(f"   🧠  IA:    {t_inference:.2f}s (para {count_processed} itens)")
            if count_processed > 0:
                print(f"      🚀 Média por item: {t_inference/count_processed:.2f}s")
            print(f"   ⏱️  TOTAL: {file_total_time:.2f}s")

        print(f"\n🏁 TEMPO TOTAL: {(time.time() - global_start):.2f}s")

if __name__ == "__main__":
    asyncio.run(DirectVerifier().run_pipeline())