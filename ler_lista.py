import openpyxl

def ler_planilha(nome_arq):
    wb = openpyxl.load_workbook(nome_arq)

    planilha = wb.active

    itens = []

    for linha in planilha.iter_rows(values_only=True):
        itens.append(linha)

    return itens