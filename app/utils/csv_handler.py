import csv

def salvar_em_csv(dados, arquivo):
    with open(arquivo, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(dados)