# 🎬 Conversor de vídeos 3D Side-by-Side para Anáglifo (óculos red-cian) & 2D

Documentação Completa, Histórico de Melhorias e Manual de Uso

## OBSERVAÇÕES IMPORTANTES:

**1)** Todos os caminhos (diretórios) citados correspondem à minha máquina pessoal. Adapte ao seu caso.
**2)** Testado no Ubuntu 26.04. Adapte ao seu sistema operacional.
**3)** Precisa ter o ffmpeg instalado. No meu caso, instalei a última versão estável, via SNAP. 
**4)** Utilizei o Gemini para adaptar meu programa original e encontrar os melhores parâmetros para o ffmpeg. Foram incontáveis horas!
**5)** Esse programa em Python foi criado porque não encontrei nenhuma solução viável de programa de conversão.
**6)** Use por sua conta e risco.


## 📑 Índice de Conteúdo

1. [Verificação Inicial do Script Original (`convert3D.py`)](#1-verificação-inicial-do-script-original-convert3dpy)
2. [Criação da Versão Otimizada (`convert3D_v2.py`)](#2-criação-da-versão-otimizada-convert3d_v2py)
3. [Tratamento de Erros e Limpeza de Arquivos Corrompidos](#3-tratamento-de-erros-e-limpeza-de-arquivos-corrompidos)
4. [Menu Interativo de Modos de Conversão](#4-menu-interativo-de-modos-de-conversão)
5. [Modo Amostra de 1 Minuto (Para Teste Rápido)](#5-modo-amostra-de-1-minuto-para-teste-rápido)
6. [Seleção Dinâmica do Diretório Alvo](#6-seleção-dinâmica-do-diretório-alvo)
7. [Comandos de Execução no Linux Ubuntu](#7-comandos-de-execução-no-linux-ubuntu)
8. [Código Fonte Completo do `convert3D_v2.py`](#8-código-fonte-completo-do-convert3d_v2py)
9. [Criação da Versão Otimizada v3 (`convert3D_v3.py`) - Dubois & 16:9](#9-criação-da-versão-otimizada-v3-convert3d_v3py---dubois--169)
10. [Guia Passo a Passo do Menu Interativo (`convert3D_v3.py`)](#10-guia-passo-a-passo-do-menu-interativo-convert3d_v3py)

---

## 1. Verificação Inicial do Script Original (`convert3D.py`)

A análise inicial do script original `convert3D.py` confirmou que:

- **`Sintaxe OK`** O código Python não possuía erros de compilação ou sintaxe.
- **`FFmpeg OK`** Os filtros FFmpeg configurados para desdobramento de vídeo 3D Side-by-Side (SBS) funcionam corretamente.

**Observações técnicas levantadas:**
- O script reprocessava todos os vídeos a cada execução, mesmo que já tivessem sido convertidos previamente.
- Se interrompido no meio, arquivos parciais podiam ser mantidos.

---

## 2. Criação da Versão Otimizada (`convert3D_v2.py`)

Para preservar a versão original do usuário, foi criado o arquivo `convert3D_v2.py`.

**Melhoria implementada:** Adicionada verificação de existência com `os.path.exists()` para evitar a reconversão desnecessária de arquivos de saída que já estejam presentes no disco.

---

## 3. Tratamento de Erros e Limpeza de Arquivos Corrompidos

Foi esclarecido o comportamento do programa caso o `ffmpeg` apresente algum erro durante a conversão:

- **O script NÃO é interrompido:** Ele captura o erro, exibe a mensagem de falha no terminal e prossegue para o próximo vídeo/pasta.
- **Limpeza Automática:** Caso ocorra um erro durante a conversão, qualquer arquivo parcial ou corrompido gerado durante a tentativa é removido automaticamente do disco para não impedir tentativas futuras.

---

## 4. Menu Interativo de Modos de Conversão

Implementado um menu inicial interativo para que o usuário possa escolher o tipo de saída desejado:

- `[1]` Converter para 3D Anáglifo E 2D (Ambos - Padrão)
- `[2]` Converter APENAS para 3D Anáglifo
- `[3]` Converter APENAS para 2D
- `[0]` Sair

---

## 5. Modo Amostra de 1 Minuto (Para Teste Rápido)

Adicionada a escolha de duração antes da conversão:

- **Vídeo Completo:** Converte o arquivo por inteiro.
- **Amostra (1 minuto):** Adiciona a flag `-t 60` ao FFmpeg e insere o sufixo `_sample` no nome dos arquivos gerados (ex: `video_Anaglifo_3D_sample.mp4`), permitindo testes rápidos sem sobrescrever nem demorar.

---

## 6. Seleção Dinâmica do Diretório Alvo

Foi removida a restrição de ter que mover o script para dentro da pasta dos vídeos.

Agora o script solicita a pasta desejada no início, suportando caminhos relativos, absolutos ou atalhos como `~/Vídeos`. Ao apertar **Enter**, ele utiliza o diretório atual.

---

## 7. Comandos de Execução no Linux Ubuntu

**Forma 1: Executar na mesma pasta do script**
```bash
cd /home/paulo/Vídeos/Conversor_3D
python3 convert3D_v3.py
```

**Forma 2: Executar de qualquer pasta do sistema**
```bash
python3 /home/paulo/Vídeos/Conversor_3D/convert3D_v3.py
```

**Forma 3: Criar um atalho permanente no terminal (Alias)**
```bash
echo "alias convert3d='python3 /home/paulo/Vídeos/Conversor_3D/convert3D_v3.py'" >> ~/.bashrc
source ~/.bashrc
```

Após criar o alias, basta digitar no terminal:
```bash
convert3d
```

---

## 8. Código Fonte Completo do `convert3D_v2.py`

```python
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
```

---

## 9. Criação da Versão Otimizada v3 (`convert3D_v3.py`) - Dubois & 16:9

A versão `convert3D_v3.py` foi desenvolvida para aproveitar os recursos nativos do **FFmpeg n4.3.1** (Snap no Ubuntu):

- **Método Dubois (`stereo3d=in=sbs2l:out=arcd`)**: Substitui a projeção manual `lutrgb/blend` pelo algoritmo matricial Dubois. Isso reduz drasticamente o efeito de *ghosting* (fantasma), preserva fidelidade cromática e diminui a fadiga visual ao utilizar óculos 3D Anáglifo.
- **Aproveitamento Máximo da Tela (16:9 Fullscreen)**: Aplica o redimensionamento `scale=1920:1080,setsar=1` para que a imagem ocupe 100% da área útil em telas Full HD 16:9 sem distorções horizontais.
- **Perfil de Saturação Ajustável**: Suporte a modo Cores Vívidas (+20% saturação via `eq=saturation=1.20`) e modo Dubois Padrão.
- **Busca Rápida na Amostra (Fast Seeking)**: Permite pular aberturas e logotipos ajustando o minuto de início da amostra (ex: `-ss 00:05:00` para iniciar aos 5 minutos).

---

## 10. Guia Passo a Passo do Menu Interativo (`convert3D_v3.py`)

O script `convert3D_v3.py` oferece um menu totalmente interativo no terminal. Abaixo está o detalhamento de cada etapa de configuração:

1. **Etapa 1: Seleção do Modo de Conversão**
   - `[1] Ambos (Padrão)`: Converte os vídeos para 3D Anáglifo e também gera a versão 2D.
   - `[2] APENAS 3D Anáglifo`: Renderiza apenas a versão 3D para óculos Red/Cyan.
   - `[3] APENAS 2D`: Extrai apenas a visão 2D (olho esquerdo) em 16:9 Full HD.
   - `[0] Sair`: Cancela e encerra o script.

2. **Etapa 2: Perfil de Saturação de Cores (3D Anáglifo)**
   - `[1] Padrão Dubois (Recomendado)`: Utiliza a matriz Dubois pura. Mantém cores equilibradas sem provocar tremores ou fadiga visual.
   - `[2] Cores Vívidas (+20%)`: Aplica o filtro `eq=saturation=1.20` para aumentar a vivacidade das cores.

3. **Etapa 3: Duração do Processamento**
   - `[1] Vídeo Completo`: Processa todo o arquivo de vídeo do início ao fim.
   - `[2] Amostra de 1 Minuto`: Processa um trecho rápido de 60 segundos para teste.

4. **Etapa 4: Minuto de Início da Amostra (Seek)**
   - Disponível quando o modo **Amostra [2]** é selecionado.
   - Permite definir em qual minuto do filme a amostra começará (Padrão: `5` minutos).
   - Utiliza busca rápida (`-ss 00:05:00`) antes da decodificação para ignorar vinhetas e logotipos iniciais.

5. **Etapa 5: Seleção da Pasta / Diretório Alvo**
   - Solicita o caminho da pasta onde estão os arquivos de vídeo. Pressionar **Enter** utiliza o diretório atual do terminal.

**Exemplo de Execução no Terminal:**
```bash
$ python3 /home/paulo/Vídeos/Conversor_3D/convert3D_v3.py

==========================================================
      CONVERSOR 3D (v3) - Otimizado para FFmpeg n4.3.1
   (Método Dubois para Cores Perfeitas + Saída 16:9 1080p)
==========================================================
 [1] Converter para 3D Anáglifo E 2D (Ambos - Padrão)
 [2] Converter APENAS para 3D Anáglifo (Dubois Red/Cyan)
 [3] Converter APENAS para 2D (Mono Left 16:9)
 [0] Sair
==========================================================
Selecione o tipo de conversão [1]: 1

----------------------------------------------------------
 Perfil de Saturação de Cores (para 3D Anáglifo):
 [1] Padrão Dubois (Recomendado - Cores naturais & Sem tremores)
 [2] Cores Vívidas / Saturação +20% (Cores mais intensas)
----------------------------------------------------------
Selecione a saturação [1]: 1

----------------------------------------------------------
 Escolha a duração do processamento:
 [1] Vídeo Completo (Padrão)
 [2] Amostra de 1 minuto (Iniciando aos 5 minutos - Pula aberturas)
----------------------------------------------------------
Selecione a duração [1]: 2
Minuto de início para a amostra [5]: 5

----------------------------------------------------------
 Informe a pasta onde os vídeos estão armazenados:
 (Aperte Enter para usar a pasta atual)
----------------------------------------------------------
Caminho [/home/paulo/Vídeos/Conversor_3D]: 

==========================================================
⚡ Modo Amostra ativado: 1 minuto gravado a partir dos 5m00s do filme.
🎨 Perfil de Cores: Dubois Padrão (Natural)
📐 Proporção de Saída: 16:9 Fullscreen (1920x1080, SAR 1:1)
📂 Diretório alvo: /home/paulo/Vídeos/Conversor_3D
==========================================================
```

---

© **[Paulo Jorge dos Santos](https://pj.pro.br)** | Site: [https://pj.pro.br](https://pj.pro.br)  
*Software Open Source — Livre para qualquer pessoa baixar, alterar e usar.*

---

📄 **Versão HTML:** [Site do projeto](https://pjpro.github.io/Convert3D/)
