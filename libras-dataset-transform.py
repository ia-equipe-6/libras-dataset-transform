import pandas as pd

TEMPO = 1 #Tempo de análise, 1 = 1 segundo.
PARTES = 4 # Partes divido por tempo acima. 4 partes é um para cada 0.20 segundo.
ARQUIVO_ENTRADA = "words_dataset.csv"
ARQUIVO_SAIDA = "libras_dataset.csv"

#Carrega dataset de frame
df_orig = pd.read_csv(ARQUIVO_ENTRADA)

#Obtem todos os IDs únicos
videos_key = pd.unique(df_orig["ID"])
linhas = list()

#Faz processo por ID, onde cada ID representa todos os frames de um único vídeo.
for video_key in videos_key:
    #Obtem todos os frames de um único vídeo, pelo ID
    df_videos_key = df_orig[df_orig["ID"] == video_key]
    primeiro_frame = df_videos_key.iloc[0]
    
    #Calcula o pulo entre frames dentro da mesma linha do novo dataset
    fps_part = (primeiro_frame['FPS'] * TEMPO) / PARTES
    fps_part = round(fps_part, 0)
    frame_count = primeiro_frame['FRAME_COUNT']

    novas_linhas = list()
    acabou = False

    #Obtem os grupos, cada vídeo gera diversas linhas no BD, nesse loop gera o agrupamento dessas linhas
    while (not acabou and frame_count > 0):
        linha = list()

        for parte in range(PARTES):
            frame_parte = frame_count - (parte * fps_part)
            linha.append(frame_parte)

            if (frame_parte <= 0):
                acabou = True

        novas_linhas.append(linha)
        frame_count -= 1

    #Organiza as colunas de interesses ou que serão ignoradas
    word = primeiro_frame['WORD']
    ignorar_colunas = ['ID', 'WORD', 'FPS', 'FRAME_COUNT', 'DURATION', 'WIDTH', 'HEIGHT', 'FRAME', 'TIME']
    colunas_parte = [c for c in list(df_videos_key.columns) if c not in ignorar_colunas]
    colunas = [c for c in colunas_parte]

    #Cria as colunas dos outros tempos
    for parte in range(1, PARTES):
        colunasMX = [c + "_T-" + str(parte) for c in colunas_parte]
        colunas = colunas + colunasMX

    colunas = ['WORD'] + colunas

    #Gera as linhas pelo agrupamento calculado
    for nova_linha in novas_linhas:
        linha = list()
        linha.append(word)

        for parte_linha in nova_linha:
            if (parte_linha > 0):
                linha_antiga = df_videos_key[df_videos_key["FRAME"] == parte_linha]
                linha = linha + list(linha_antiga[colunas_parte].iloc[0])
            else:
                #A Linha não existe, gera valores zerados
                linha_vazia = [0.0 for i in range(len(colunas_parte))]
                linha = linha + linha_vazia

        linhas.append(linha)

#Salva Dataset
df_final = pd.DataFrame(linhas, columns=colunas)
print(df_final.columns)
df_final.to_csv(ARQUIVO_SAIDA, index=False)