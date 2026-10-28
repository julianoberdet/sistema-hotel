from lib.dados.database import conectar
from lib.interface import *
from datetime import date

while True:
    opcao = menu([
        'Ver quartos [LIVRE/OCUPADO]',
        'Check-in Completo',
        'Check-out',
        'Listar Clientes',
        'Deletar Cliente',
        'Sair'
    ])

    try:
        opcao = int(opcao)
    except:
        opcao = 0

    if opcao == 1:
        cabecalho('SITUAÇÃO DOS QUARTOS')
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT q.numero, q.tipo, q.preco_diaria, c.nome, c.nacionalidade, r.status
            FROM quartos q
            LEFT JOIN reservas r ON q.id = r.quarto_id AND r.status='ocupado'
            LEFT JOIN clientes c ON c.id = r.cliente_id
            ORDER BY q.numero
        """)
        for num, tipo, preco, nome, nac, status in cur.fetchall():
            if status == 'ocupado':
                print(f"Quarto {num} | {tipo} | R${float(preco):.2f} | OCUPADO - {nome} ({nac})")
            else:
                print(f"Quarto {num} | {tipo} | R${float(preco):.2f} | LIVRE")
        print(linha())
        cur.close()
        con.close()

    elif opcao == 2:
        cabecalho('CHECK-IN COMPLETO')
        cpf = leiaInt('CPF: ')
        nome = leiaStr('Nome: ')
        nasc = leiaInt('Data nascimento AAAA-MM-DD: ')
        nacionalidade = leiaStr('Nacionalidade: ')
        peso = leiaFloat('Peso: ')
        altura = leiaFloat('Altura: ')

        try:
            num_quarto = leiaInt('Número do quarto: ')
        except ValueError:
            print("\033[31mErro: Número do quarto inválido!\033[m")
            continue

        con = conectar()
        cur = con.cursor()
        try:
            cur.execute("SELECT id FROM quartos WHERE numero=%s", (num_quarto,))
            resultado = cur.fetchone()
            if not resultado:
                print("\033[31mQuarto não encontrado!\033[m")
            else:
                quarto_id = resultado[0]

                # Inserir cliente usando a coluna 'nascimento'
                cur.execute(
                    "INSERT INTO clientes (cpf, nome, nascimento, nacionalidade, peso, altura) VALUES (%s,%s,%s,%s,%s,%s)",
                    (cpf, nome, nasc, nacionalidade, peso, altura))
                cid = cur.lastrowid

                # Inserir reserva
                cur.execute(
                    "INSERT INTO reservas (cliente_id, quarto_id, data_checkin, status) VALUES (%s,%s,%s,'ocupado')",
                    (cid, quarto_id, date.today()))
                con.commit()
                print(f"\033[32mCheck-in de {nome} no quarto {num_quarto} realizado com sucesso!\033[m")
        except Exception as e:
            print(f"\033[31mErro ao realizar check-in: {e}\033[m")
            con.rollback()
        finally:
            cur.close()
            con.close()

    elif opcao == 3:
        cabecalho('CHECK-OUT')
        num = leiaInt('Número do quarto para check-out: ')
        con = conectar()
        cur = con.cursor()
        try:
            cur.execute(
                "UPDATE reservas SET status='livre', data_checkout=%s WHERE quarto_id=(SELECT id FROM quartos WHERE numero=%s) AND status='ocupado'",
                (date.today(), num))
            con.commit()
            if cur.rowcount > 0:
                print(f"\033[32mCheck-out do quarto {num} realizado com sucesso!\033[m")
            else:
                print(f"\033[31mNenhuma reserva ocupada encontrada para o quarto {num}.\033[m")
        except Exception as e:
            print(f"\033[31mErro: {e}\033[m")
        finally:
            cur.close()
            con.close()

    elif opcao == 4:
        cabecalho('CLIENTES CADASTRADOS')
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT cpf, nome, nascimento, nacionalidade, peso, altura FROM clientes")
        clientes = cur.fetchall()
        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for cpf, nome, nasc, nac, peso, alt in clientes:
                print(f"{cpf} | {nome} | Nasc: {nasc} | {nac} | {peso}kg | {alt}m")
        print(linha())
        cur.close()
        con.close()

    elif opcao == 5:
        cabecalho('DELETAR CLIENTE')
        cpf_del = leiaInt('Digite o CPF do cliente que deseja deletar: ')
        con = conectar()
        cur = con.cursor()
        try:
            # Verifica se o cliente existe
            cur.execute("SELECT id, nome FROM clientes WHERE cpf = %s", (cpf_del,))
            cliente = cur.fetchone()

            if not cliente:
                print("\033[31mCliente não encontrado com esse CPF.\033[m")
            else:
                cliente_id = cliente[0]
                nome_cliente = cliente[1]

                # Apaga as reservas do cliente primeiro para evitar conflito de chave estrangeira
                cur.execute("DELETE FROM reservas WHERE cliente_id = %s", (cliente_id,))
                # Apaga o cliente
                cur.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
                con.commit()
                print(f"\033[32mCliente '{nome_cliente}' deletado com sucesso!\033[m")
        except Exception as e:
            print(f"\033[31mErro ao deletar cliente: {e}\033[m")
            con.rollback()
        finally:
            cur.close()
            con.close()

    elif opcao == 6:
        cabecalho('Saindo... Até logo!')
        break
    else:
        print("\033[31mOpção inválida! Tenta de novo.\033[m")