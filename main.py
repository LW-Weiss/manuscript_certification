import asyncio
import time
import os
import datetime

# --- IMPORTS DOS SEUS SCRIPTS ---
# Certifique-se que os nomes dos arquivos estão exatos na pasta
try:
    from verifier_ollama_direct import DirectVerifier
    from retry_with_pdfs import run_retry_pipeline
except ImportError as e:
    print(f"❌ Erro de Importação: {e}")
    print("Verifique se os arquivos 'verifier_direct_ollama.py' e 'retry_with_pdfs_v2.py' estão na mesma pasta.")
    exit()

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}\n")

async def main_workflow():
    # --- ⏱️ INÍCIO DO CRONÔMETRO GLOBAL ---
    global_start_time = time.time()
    
    print_header("INICIANDO O FLUXO HÍBRIDO (WHITE-HAT)")
    print(f"📅 Data/Hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # ---------------------------------------------------------
    # FASE 1: VARREDURA RÁPIDA (ABSTRACTS)
    # ---------------------------------------------------------
    print_header("FASE 1: Verificação Rápida (Abstracts)")
    try:
        verifier = DirectVerifier()
        await verifier.run_pipeline()
    except Exception as e:
        print(f"❌ Erro crítico na Fase 1: {e}")
        return

    print("\n✅ FASE 1 CONCLUÍDA.")
    time.sleep(2) # Pausa técnica

    # ---------------------------------------------------------
    # FASE 2: PENTE FINO (PDFS / HÍBRIDO)
    # ---------------------------------------------------------
    print_header("FASE 2: Pente Fino (Recuperação de PDFs)")
    print("ℹ️  Estratégia: Tentar Unpaywall/S2 + Ler pasta 'pdfs_baixados'...")
    
    try:
        await run_retry_pipeline()
    except Exception as e:
        print(f"❌ Erro crítico na Fase 2: {e}")
        return

    # ---------------------------------------------------------
    # 🏁 RESUMO FINAL E TEMPO TOTAL
    # ---------------------------------------------------------
    global_end_time = time.time()
    total_seconds = global_end_time - global_start_time
    
    # Formata para ficar bonito (Horas:Minutos:Segundos)
    formatted_time = str(datetime.timedelta(seconds=int(total_seconds)))

    print("\n")
    print("="*60)
    print(f"🏁  PROCESSO FINALIZADO COM SUCESSO")
    print("="*60)
    print(f"⏱️  TEMPO TOTAL DE EXECUÇÃO: {formatted_time} ({total_seconds:.2f}s)")
    print(f"📂  Relatório Final: relatorio_final_v2.csv")
    
    # Contagem de PDFs na pasta para controle
    pdf_count = 0
    if os.path.exists("pdfs_baixados"):
        pdf_count = len([f for f in os.listdir("pdfs_baixados") if f.endswith(".pdf")])
    
    print(f"📚  Biblioteca Local: {pdf_count} PDFs na pasta 'pdfs_baixados'")
    print("-" * 60)
    print("💡 PRÓXIMOS PASSOS (MODO MANUAL):")
    print("   1. Abra o CSV final e filtre os 'NOT_MENTIONED' ou sem PDF.")
    print("   2. Baixe-os manualmente e salve na pasta 'pdfs_baixados'.")
    print("   3. Rode este script novamente para processá-los.")
    print("="*60)

if __name__ == "__main__":
    try:
        asyncio.run(main_workflow())
    except KeyboardInterrupt:
        print("\n🛑 Processo interrompido pelo usuário.")