import sys
def leiaInt(n):
    while True:
        try:
            numero = int(input(n))
        except (TypeError,ValueError):
            print('\033[31mERRO! Digite um número inteiro válido\033[m')
        except KeyboardInterrupt:
            print('\n\033[31mO usuário preferiu sair\033[31m')
            sys.exit()
        else:
            return numero

def leiaFloat(n):
    while True:
        try:
            numero = float(input(n))
        except (TypeError,ValueError):
            print('\033[31mERRO! Digite um número válido\033[m')
        except KeyboardInterrupt:
            print('\n\033[31mO usuário preferiu sair\033[31m')
            sys.exit()
        else:
            return numero


def leiaStr(msg):
    while True:
        try:
            palavra = str(input(msg)).strip()
            if palavra == '' or not palavra.replace(' ','').isalpha():
                print('\033[31mERRO! Digite algo válido\033[m')
        except KeyboardInterrupt:
            print('\n\033[31mO usuário preferiu sair\033[31m')
            sys.exit()
        else:
            return palavra


def linha(tam=50):
    return '-' * tam


def cabecalho(txt):
    print(linha())
    print(txt.center(50))
    print(linha())


def menu(lista):
    cabecalho('MENU PRINCIPAL')
    contador = 1
    for item in lista:
        print(f'\033[1;37m{contador}\033[m - {item}')
        contador += 1
    print(linha())
    opc = leiaInt('Sua opção: ')
    return opc