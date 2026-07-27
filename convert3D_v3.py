import os
import sys
import subprocess

# Extensões de vídeo suportadas
EXTENSOES_SUPORTADAS = ('.mp4', '.mkv', '.avi', '.mov')

def exibir_menu():
    print("==========================================================")
    print("      CONVERSOR 3D (v3) - Otimizado para FFmpeg n4.3.1")
    print("   (Método Dubois para Cores Perfeitas + Saída 16:9 1080p)")
    print("==========================================================")
    print(" [1] Converter para 3D Anáglifo E 2D (Ambos - Padrão)")
    print(" [2] Converter APENAS para 3D Anáglifo (Dubois Red/Cyan)")
    print(" [3] Converter APENAS para 2D (Mono Left 16:9)")
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
    print(" Perfil de Saturação de Cores (para 3D Anáglifo):")
    print(" [1] Padrão Dubois (Recomendado - Cores naturais & Sem tremores)")
    print(" [2] Cores Vívidas / Saturação +20% (Cores mais intensas)")
    print("----------------------------------------------------------")
    
    try:
        sat_op = input("Selecione a saturação [1]: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nOperação cancelada pelo usuário.")
        sys.exit(0)
        
    saturar_vivido = sat_op == "2"

    print("\n----------------------------------------------------------")
    print(" Escolha a duração do processamento:")
    print(" [1] Vídeo Completo (Padrão)")
    print(" [2] Amostra de 1 minuto (Iniciando aos 5 minutos - Pula aberturas)")
    print("----------------------------------------------------------")
    
    try:
        duracao_op = input("Selecione a duração [1]: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nOperação cancelada pelo usuário.")
        sys.exit(0)
        
    e_amostra = duracao_op == "2"
    minuto_inicio = 5 if e_amostra else 0
    
    if e_amostra:
        try:
            min_input = input("Minuto de início para a amostra [5]: ").strip()
            if min_input:
                minuto_inicio = max(0, int(min_input))
        except ValueError:
            print("⚠️ Valor inválido. Utilizando o minuto 5 como padrão.")
            minuto_inicio = 5
        except (KeyboardInterrupt, EOFError):
            print("\nOperação cancelada pelo usuário.")
            sys.exit(0)
    
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
        print(f"⚡ Modo Amostra ativado: 1 minuto gravado a partir dos {minuto_inicio}m00s do filme.")
    else:
        print("🎬 Modo Completo ativado: o vídeo inteiro será processado.")
    print(f"🎨 Perfil de Cores: {'Cores Vívidas (+20%)' if saturar_vivido else 'Dubois Padrão (Natural)'}")
    print("📐 Proporção de Saída: 16:9 Fullscreen (1920x1080, SAR 1:1)")
    print(f"📂 Diretório alvo: {diretorio_alvo}")
    print("==========================================================")

    return modo, e_amostra, minuto_inicio, saturar_vivido, diretorio_alvo

def processar_pastas():
    modo, e_amostra, minuto_inicio, saturar_vivido, diretorio_alvo = exibir_menu()
    
    # Define o que será processado com base na escolha
    quer_anaglifo = modo in ("1", "2")
    quer_2d = modo in ("1", "3")
    
    # Sufixo para diferenciar os arquivos de amostra dos completos
    sufixo_sample = f"_sample_{minuto_inicio}m" if e_amostra else ""
    sufixo_sat = "_vivido" if saturar_vivido else ""

    print("\n==========================================================")
    print(" Iniciando busca recorrente e conversão otimizada (FFmpeg n4.3.1)")
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
                    saida_anaglifo = os.path.join(raiz, f"{nome_base}_Anaglifo_3D{sufixo_sat}{sufixo_sample}{extensao}")
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
                        # 1. CONVERSÃO PARA 3D ANÁGLIFO OTIMIZADA (MÉTODO DUBOIS + 16:9 TELA CHEIA)
                        if quer_anaglifo:
                            if not anaglifo_existe:
                                print(f"🔄 Gerando versão 3D Anáglifo Dubois 16:9 [{'Vívida +20%' if saturar_vivido else 'Natural'}] ({f'Amostra 1 min a partir dos {minuto_inicio}m' if e_amostra else 'Completo'})...")
                                
                                # Monta o filtro com base na preferência de saturação
                                vf_anaglifo = 'stereo3d=in=sbs2l:out=arcd,eq=saturation=1.20,scale=1920:1080,setsar=1' if saturar_vivido else 'stereo3d=in=sbs2l:out=arcd,scale=1920:1080,setsar=1'
                                
                                cmd_anaglifo = ['ffmpeg']
                                if e_amostra:
                                    # Busca rápida antes da decodificação (-ss antes do -i)
                                    tempo_inicio = f"00:{minuto_inicio:02d}:00"
                                    cmd_anaglifo.extend(['-ss', tempo_inicio])
                                    
                                cmd_anaglifo.extend([
                                    '-i', caminho_completo,
                                    '-sws_flags', 'lanczos',
                                    '-vf', vf_anaglifo,
                                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy'
                                ])
                                if e_amostra:
                                    cmd_anaglifo.extend(['-t', '60'])
                                cmd_anaglifo.extend([saida_anaglifo, '-y'])
                                
                                subprocess.run(cmd_anaglifo, check=True)
                            else:
                                print("⏩ Versão 3D Anáglifo já existe. Pulando...")
                        
                        # 2. CONVERSÃO PARA 2D OTIMIZADA (MONO LEFT + 16:9 TELA CHEIA)
                        if quer_2d:
                            if not d2_existe:
                                print(f"🔄 Gerando versão 2D 16:9 ({f'Amostra 1 min a partir dos {minuto_inicio}m' if e_amostra else 'Completo'})...")
                                cmd_2d = ['ffmpeg']
                                if e_amostra:
                                    tempo_inicio = f"00:{minuto_inicio:02d}:00"
                                    cmd_2d.extend(['-ss', tempo_inicio])
                                    
                                cmd_2d.extend([
                                    '-i', caminho_completo,
                                    '-sws_flags', 'lanczos',
                                    '-vf', 'stereo3d=in=sbs2l:out=ml,scale=1920:1080,setsar=1',
                                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy'
                                ])
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
