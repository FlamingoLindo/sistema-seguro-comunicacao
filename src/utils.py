"""
FUNÇÕES ÚTEIS
"""

import os

def clear_screen():
    """
    Função para limpar a tela do terminal.
    """
    
    os.system('cls')

def anonimizar_dados(cpf, phone):
    """
    Função para anonimizar os dados de CPF e telefone.
    """

    cpf_anon = "XXX.XXX.XXX-" + cpf[-2:]
    phone_anon = "XXXXX-" + phone[-4:]
    return cpf_anon, phone_anon