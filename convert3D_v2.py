import os
import sys
import subprocess

# Extensões de vídeo suportadas
EXTENSOES_SUPORTADAS = ('.mp4', '.mkv', '.avi', '.mov')

def exibir_menu():
    print("==========================================================")
    print("      CONVERSOR 3D - Escolha o modo de execução")
    print("==========================================================")
    print(" [1] Converter para 3D Anáglifo E 2D (Ambos - Padrão)")
    print(" [2] Converter APENAS para 3D Anáglifo")
    print(" [3] Converter APENAS para 2D")
    print(" [0] Sair")
    print("==========================================================")
    
    try:
        modo = input("Selecione o tipo de conversão [1]: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nOperação cancelada pelo usuário.")
        sys.exit(0)
        
    if modo == "":
        modo = "1"
        
    if modo not in ("1", "2", "3", "0"):
        print("❌ Opção inválida! Utilizando a opção padrão [1].\n")
        modo = "1"
        
    if modo == "0":
        print("Saindo do conversor.")
        sys.exit(0)
        
    print("\n----------------------------------------------------------")
    print(" Escolha a duração do processamento:")
    print(" [1] Vídeo Completo (Padrão)")
    print(" [2] Amostra de 1 minuto (para teste rápido)")
    print("----------------------------------------------------------")
    
    try:
        duracao_op = input("Selecione a duração [1]: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nOperação cancelada pelo usuário.")
        sys.exit(0)
        
    e_amostra = duracao_op == "2"
    
    print("\n----------------------------------------------------------")
    print(" Informe a pasta onde os vídeos estão armazenados:")
    print(" (Aperte Enter para usar a pasta atual)")
    print("----------------------------------------------------------")
    
    try:
        pasta_input = input(f"Caminho [{os.getcwd()}]: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nOperação cancelada pelo usuário.")
        sys.exit(0)
        
    if not pasta_input:
        diretorio_alvo = os.getcwd()
    else:
        diretorio_alvo = os.path.abspath(os.path.expanduser(pasta_input))
        
    if not os.path.isdir(diretorio_alvo):
        print(f"❌ O diretório informado não existe: {diretorio_alvo}")
        sys.exit(1)

    print("\n==========================================================")
    if e_amostra:
        print("⚡ Modo Amostra ativado: será gerado apenas 1 minuto de vídeo.")
    else:
        print("🎬 Modo Completo ativado: o vídeo inteiro será processado.")
    print(f"📂 Diretório alvo: {diretorio_alvo}")
    print("==========================================================")

    return modo, e_amostra, diretorio_alvo

def processar_pastas():
    modo, e_amostra, diretorio_alvo = exibir_menu()
    
    # Define o que será processado com base na escolha
    quer_anaglifo = modo in ("1", "2")
    quer_2d = modo in ("1", "3")
    
    # Sufixo para diferenciar os arquivos de amostra dos completos
    sufixo_sample = "_sample" if e_amostra else ""

    print("\n==========================================================")
    print(" Iniciando busca recorrente e conversão de arquivos 3D")
    print("==========================================================")
    
    # os.walk percorre recursivamente a pasta informada e todas as subpastas
    for raiz, pastas, arquivos in os.walk(diretorio_alvo):
        for arquivo in arquivos:
            # Verifica se é um arquivo de vídeo suportado
            if arquivo.lower().endswith(EXTENSOES_SUPORTADAS):
                
                # Regra de ouro: Só processa se tiver "3D" no nome
                # Ignora arquivos que o próprio script já possa ter gerado antes
                if ("3d" in arquivo.lower() 
                        and "_anaglifo_3d" not in arquivo.lower() 
                        and "_2d" not in arquivo.lower()
                        and "_sample" not in arquivo.lower()):
                    
                    caminho_completo = os.path.join(raiz, arquivo)
                    nome_base, extensao = os.path.splitext(arquivo)
                    
                    # Define os caminhos de saída na mesma pasta do arquivo original
                    saida_anaglifo = os.path.join(raiz, f"{nome_base}_Anaglifo_3D{sufixo_sample}{extensao}")
                    saida_2d = os.path.join(raiz, f"{nome_base}_2D{sufixo_sample}{extensao}")
                    
                    # Verifica existência prévia dos arquivos convertidos
                    anaglifo_existe = os.path.exists(saida_anaglifo)
                    d2_existe = os.path.exists(saida_2d)
                    
                    # Verifica se o que o usuário solicitou já existe no disco
                    precisa_anaglifo = quer_anaglifo and not anaglifo_existe
                    precisa_2d = quer_2d and not d2_existe
                    
                    if not precisa_anaglifo and not precisa_2d:
                        print(f"\n⏭️ Pulando '{arquivo}': Formatos solicitados ({'Amostra' if e_amostra else 'Completo'}) já existem.")
                        continue
                    
                    print(f"\n🎬 Vídeo 3D encontrado em: {raiz}")
                    print(f"📄 Arquivo: {arquivo}")
                    print("-" * 58)
                    
                    # Executa os comandos no terminal do Ubuntu de forma segura
                    try:
                        # 1. CONVERSÃO PARA 3D ANÁGLIFO PERFEITO
                        if quer_anaglifo:
                            if not anaglifo_existe:
                                print(f"🔄 Gerando versão 3D Anáglifo ({'Amostra 1 min' if e_amostra else 'Completo'})...")
                                cmd_anaglifo = [
                                    'ffmpeg', '-i', caminho_completo,
                                    '-sws_flags', 'lanczos',
                                    '-filter_complex', '[0:v]split=2[left_raw][right_raw]; [left_raw]crop=iw/2:ih:0:0,scale=1920:1080[left]; [right_raw]crop=iw/2:ih:iw/2:0,scale=1920:1080[right]; [left]lutrgb=g=0:b=0[red]; [right]lutrgb=r=0[cyan]; [red][cyan]blend=all_mode=\'addition\',setsar=1',
                                    '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy'
                                ]
                                if e_amostra:
                                    cmd_anaglifo.extend(['-t', '60'])
                                cmd_anaglifo.extend([saida_anaglifo, '-y'])
                                
                                subprocess.run(cmd_anaglifo, check=True)
                            else:
                                print("⏩ Versão 3D Anáglifo já existe. Pulando...")
                        
                        # 2. CONVERSÃO PARA 2D PERFEITO
                        if quer_2d:
                            if not d2_existe:
                                print(f"🔄 Gerando versão 2D ({'Amostra 1 min' if e_amostra else 'Completo'})...")
                                cmd_2d = [
                                    'ffmpeg', '-i', caminho_completo,
                                    '-sws_flags', 'lanczos',
                                    '-vf', 'crop=iw/2:ih:0:0,scale=1920:1080,setsar=1',
                                    '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy'
                                ]
                                if e_amostra:
                                    cmd_2d.extend(['-t', '60'])
                                cmd_2d.extend([saida_2d, '-y'])
                                
                                subprocess.run(cmd_2d, check=True)
                            else:
                                print("⏩ Versão 2D já existe. Pulando...")

                        print(f"✅ Processamento concluído com sucesso!")
                    except subprocess.CalledProcessError as e:
                        print(f"❌ Erro ao processar o arquivo {arquivo}: {e}")
                        # Remove arquivos incompletos/corrompidos gerados nesta tentativa falha
                        if quer_anaglifo and not anaglifo_existe and os.path.exists(saida_anaglifo):
                            try:
                                os.remove(saida_anaglifo)
                                print(f"🧹 Arquivo incompleto removido: {saida_anaglifo}")
                            except OSError:
                                pass
                        if quer_2d and not d2_existe and os.path.exists(saida_2d):
                            try:
                                os.remove(saida_2d)
                                print(f"🧹 Arquivo incompleto removido: {saida_2d}")
                            except OSError:
                                pass

    print("\n==========================================================")
    print(" 🎉 Varredura e conversões concluídas!")
    print("==========================================================")

if __name__ == "__main__":
    processar_pastas()
