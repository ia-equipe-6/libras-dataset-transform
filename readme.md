# Conversor Frame Dataset para Libras Dataset 

Esse código converte um dataset gerado frame by frame de vídeos de palavras em libras, para uma linha com junção de diversos frames em x tempo, que será usado para o treinamento final. A quantidade de tempo e de frames pode ser definido no ponto inicial do código. Atualmente são 4 frames por 1 segundo em uma única linha.

* Giovanna Lima Marques 
* Ricardo Augusto Coelho (https://github.com/tiorac)
* Tiago Goes Teles 
* Wellington de Jesus Albuquerque 

## Processo

1. Carrega todo o dataset de frame.
1. Obtem todos os ids únicos de vídeo para o processo.
1. Para cada ID único de vídeo:
    1. Obtem todos os frames com o ID.
    1. Calcula o quantos frames deve pular para a mesma linha.
    1. Do último para o primeiro frame, gera a linha do dataset de junção, obedecendo os pulos.
    1. Quando ter que gerar linha vazia, passa para a próxima palavra.
1. Salva o dataset com as junções de linhas.

## Converter Dataset

1. Clone o repositório.
    ```cmd
    git clone https://github.com/ia-equipe-6/libras-dataset-transform.git
    ```
1. Copia o dataset gerado na pasta do código clonado com o nome 'words_dataset.csv'
1. Execute o conversor de dataset:
    ```cmd
    python .\libras-dataset-transform.py
    ```

A saída é um novo dataset chamado "libras_dataset.csv".

## Próximos Passos

Utilize o código de normalização e treinamento
(Em Breve)

## Bibliotecas

Esse código utiliza as seguintes bibliotecas para conversão do dataset:

* Pandas