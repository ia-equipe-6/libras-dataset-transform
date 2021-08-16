import pandas as pd
import numpy as np

TEMPO = 1 #Tempo de análise, 1 = 1 segundo.
PARTES = 4 # Partes divido por tempo acima. 4 partes é um para cada 0.20 segundo.

df_orig = pd.read_csv('ten_words_dataset.csv')

videos_key = pd.unique(df_orig["ID"])
linhas = list()

for video_key in videos_key:
    df_videos_key = df_orig[df_orig["ID"] == video_key]
    primeiro_frame = df_videos_key.iloc[0]
    fps_part = (primeiro_frame['FPS'] * TEMPO) / PARTES
    fps_part = round(fps_part, 0)
    frame_count = primeiro_frame['FRAME_COUNT']

    novas_linhas = list()
    acabou = False

    while (not acabou and frame_count > 0):
        linha = list()

        for parte in range(PARTES):
            frame_parte = frame_count - (parte * fps_part)
            linha.append(frame_parte)

            if (frame_parte <= 0):
                acabou = True

        novas_linhas.append(linha)
        frame_count -= 1

    word = primeiro_frame['WORD']
    ignorar_colunas = ['ID', 'WORD', 'FPS', 'FRAME_COUNT', 'DURATION', 'WIDTH', 'HEIGHT', 'FRAME', 'TIME']
    colunas_parte = [c for c in list(df_videos_key.columns) if c not in ignorar_colunas]
    colunas = [c for c in colunas_parte]

    for parte in range(1, PARTES):
        colunasMX = [c + "_T-" + str(parte) for c in colunas_parte]
        colunas = colunas + colunasMX

    colunas = ['WORD'] + colunas

    for nova_linha in novas_linhas:
        linha = list()
        linha.append(word)

        for parte_linha in nova_linha:
            if (parte_linha > 0):
                linha_antiga = df_videos_key[df_videos_key["FRAME"] == parte_linha]
                linha = linha + list(linha_antiga[colunas_parte].iloc[0])
            else:
                linha_vazia = [0.0 for i in range(len(colunas_parte))]
                linha = linha + linha_vazia

        linhas.append(linha)

df_final = pd.DataFrame(linhas, columns=colunas)
print(df_final.columns)
df_final.to_csv('ten_words_temp.csv')