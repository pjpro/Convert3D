import os
import subprocess

# Extensões de vídeo suportadas
EXTENSOES_SUPORTADAS = ('.mp4', '.mkv', '.avi', '.mov')

def processar_pastas():
    # Pega o diretório onde o script Python está rodando
    diretorio_atual = os.getcwd()
    
    print("==========================================================")
    # Correção de grafia na mensagem inicial
    print(" Iniciando busca recorrente e conversão de arquivos 3D")
    print("==========================================================")
    
    # os.walk percorre recursivamente a pasta atual e todas as subpastas
    for raiz, pastas, arquivos in os.walk(diretorio_atual):
        for arquivo in arquivos:
            # Verifica se é um arquivo de vídeo suportado
            if arquivo.lower().endswith(EXTENSOES_SUPORTADAS):
                
                # Regra de ouro: Só processa se tiver "3D" no nome
                # Ignora arquivos que o próprio script já possa ter gerado antes
                if "3d" in arquivo.lower() and "_anaglifo_3d" not in arquivo.lower() and "_2d" not in arquivo.lower():
                    
                    caminho_completo = os.path.join(raiz, arquivo)
                    nome_base, extensao = os.path.splitext(arquivo)
                    
                    # Define os caminhos de saída na mesma pasta do arquivo original
                    saida_anaglifo = os.path.join(raiz, f"{nome_base}_Anaglifo_3D{extensao}")
                    saida_2d = os.path.join(raiz, f"{nome_base}_2D{extensao}")
                    
                    print(f"\n🎬 Vídeo 3D encontrado em: {raiz}")
                    print(f"📄 Arquivo: {arquivo}")
                    print("-" * 58)
                    
                    # 1. CONVERSÃO PARA 3D ANÁGLIFO PERFEITO
                    print("🔄 Gerando versão 3D Anáglifo...")
                    cmd_anaglifo = [
                        'ffmpeg', '-i', caminho_completo,
                        '-sws_flags', 'lanczos',
                        '-filter_complex', '[0:v]split=2[left_raw][right_raw]; [left_raw]crop=iw/2:ih:0:0,scale=1920:1080[left]; [right_raw]crop=iw/2:ih:iw/2:0,scale=1920:1080[right]; [left]lutrgb=g=0:b=0[red]; [right]lutrgb=r=0[cyan]; [red][cyan]blend=all_mode=\'addition\',setsar=1',
                        '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy', saida_anaglifo, '-y'
                    ]
                    
                    # 2. CONVERSÃO PARA 2D PERFEITO
                    print("🔄 Gerando versão 2D...")
                    cmd_2d = [
                        'ffmpeg', '-i', caminho_completo,
                        '-sws_flags', 'lanczos',
                        '-vf', 'crop=iw/2:ih:0:0,scale=1920:1080,setsar=1',
                        '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy', saida_2d, '-y'
                    ]
                    
                    # Executa os comandos no terminal do Ubuntu de forma segura
                    try:
                        subprocess.run(cmd_anaglifo, check=True)
                        subprocess.run(cmd_2d, check=True)
                        print(f"✅ Concluído com sucesso!")
                    except subprocess.CalledProcessError as e:
                        print(f"❌ Erro ao processar o arquivo {arquivo}: {e}")

    print("\n==========================================================")
    print(" 🎉 Varredura e conversões concluídas!")
    print("==========================================================")

if __name__ == "__main__":
    processar_pastas()