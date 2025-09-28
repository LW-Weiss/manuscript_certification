import os
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# --- Configuração ---
JSON_INPUT_FOLDER = "mini_corpus_json"
PDF_OUTPUT_FOLDER = "artigos_pdf_completos" # Novo nome para a pasta de saída
TEMPLATE_FILE = "template.html"

# --- Preparação do Ambiente ---
if not os.path.exists(PDF_OUTPUT_FOLDER):
    os.makedirs(PDF_OUTPUT_FOLDER)

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(TEMPLATE_FILE)

print("Iniciando a geração dos PDFs completos...")

# --- Loop Principal ---
for json_filename in os.listdir(JSON_INPUT_FOLDER):
    if json_filename.endswith('.json'):
        input_filepath = os.path.join(JSON_INPUT_FOLDER, json_filename)
        print(f"  Processando arquivo: {json_filename}...")
        
        with open(input_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # --- LÓGICA PARA AS REFERÊNCIAS ---
        # (Isso é para o template, não muda a extração)
        bib_entries = data.get('bib_entries', {})
        lista_de_referencias_estruturadas = []
        for ref_data in bib_entries.values():
            if not ref_data: continue

            paginas_str = ""
            volume = ref_data.get('volume')
            pagina_inicial = ref_data.get('firstpage')
            pagina_final = ref_data.get('lastpage')
            if volume: paginas_str += f"Vol. {volume}"
            if pagina_inicial:
                if paginas_str: paginas_str += ", "
                paginas_str += f"pp. {pagina_inicial}-{pagina_final}"

            ref_dict = {
                "authors": ref_data.get('authors', []),
                "title": ref_data.get('title', 'N/A'),
                "Páginas": paginas_str if paginas_str else "N/A",
                "pub_year": ref_data.get('pub_year', 'N/A'),
                "doi": ref_data.get('doi')
            }
            lista_de_referencias_estruturadas.append(ref_dict)
            
        # --- Renderização do Template ---
        # Enviamos todos os dados para o template de uma vez
        html_content = template.render(
            metadata=data.get('metadata', {}), 
            abstract=data.get('abstract', 'Resumo não disponível.'),
            body_text=data.get('body_text', []),
            bib_entries=bib_entries # Passamos o dicionário original
        )
        
        pdf_filename = os.path.splitext(json_filename)[0] + '.pdf'
        pdf_filepath = os.path.join(PDF_OUTPUT_FOLDER, pdf_filename)
        
        HTML(string=html_content).write_pdf(pdf_filepath)
        
        print(f"  [✓] PDF gerado: {pdf_filename}")

print(f"\nProcesso concluído! PDFs completos salvos na pasta '{PDF_OUTPUT_FOLDER}'.")