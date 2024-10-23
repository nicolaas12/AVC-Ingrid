#### produtos itens disponíveis quantidade e valor###
produtos = [
    (1, "Smartphone", "Eletrônicos", 1200.00, 10),
    (2, "Camiseta", "Vestuário", 50.00, 20),
    (3, "Notebook", "Eletrônicos", 2500.00, 5),
    (4, "Calça", "Vestuário", 120.00, 15)
]

##### gravação ####
encomendas = {}
numero_pedido = 402  # Começando a numeração do pedido com  dígito###

             # #codigo, cupom list##
cupons = {
    "CUPOM10": (10, "2024-12-31"),
    "CUPOM15": (15, "2024-12-31"),
    "CUPOM20": (20, "2024-12-31"),
}


##gerador de desco.t list###
def gerar_cupom():
    codigo = f"CUPOM{random.randint(1, 100)}"
    desconto = random.choice([10, 15, 20])
    validade = "2024-12-31"
    cupons[codigo] = (desconto, validade)
    return codigo


def listar_cupons():
    print("\n--- Cupons Disponíveis ---")
    for codigo, (desconto, validade) in cupons.items():
        print(f"{codigo}: {desconto}% de desconto (Válido até {validade})")
    print("----------------------------")


def validar_cupom(cupom):
    if cupom in cupons:
        desconto, validade = cupons[cupom]
        return desconto
    return 0


def listar_produtos():
    print("\n--- Produtos Disponíveis ---")
    for id, nome, categoria, preco, quantidade in produtos:
        print(f"ID: {id} - {nome} (Categoria: {categoria}, Preço: R$ {preco:.2f}, Estoque: {quantidade})")
    print("----------------------------")


def coletar_dados_cliente():
    nome = input("Nome do cliente: ")
    while True:                 ###barramento por falta de elemento,###
        cpf = input("CPF do cliente (11 dígitos): ")
        if len(cpf) == 11 and cpf.isdigit():
            break
        else:
            print("CPF inválido! Deve conter exatamente 11 dígitos.")

    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
    email = input("E-mail do cliente: ")

    print("\n--- Confirmação de Dados ---")
    print(f"Nome: {nome}")
    print(f"CPF: {cpf}")
    print(f"Data de Nascimento: {data_nascimento}")
    print(f"E-mail: {email}")
    confirmar = input("Os dados estão corretos? (s/n): ")

    if confirmar.lower() == 's':
        return nome, cpf, email      ##retnna nome, CPF e e-mail### retorno de cadastro###
    else:
        print("Por favor, insira os dados novamente.")
        return coletar_dados_cliente()


def coletar_dados_pagamento():
    print("\n--- Escolha o Método de Pagamento ---")
    print("1. Cartão de Crédito")
    print("2. Boleto")
    print("3. Pix")
    escolha_pagamento = input("Escolha uma opção (1, 2 ou 3): ")

    if escolha_pagamento == "1":
        tipo_cartao = input("Tipo de cartão de crédito (Visa, MasterCard, etc.): ")
        numero_cartao = input("Número do cartão de crédito: ")
        while True:
            validade = input("Validade do cartão (MM/AA): ")
            if len(validade) == 5 and validade[2] == '/' and validade[:2].isdigit() and validade[3:].isdigit():
                break
            else:
                print("Data de validade inválida! Formato correto: MM/AA")
        cvv = input("CVV do cartão: ")
        return "Cartão de Crédito", tipo_cartao, numero_cartao, validade, cvv

    elif escolha_pagamento == "2":
        confirmar = input("Você escolheu Boleto. Deseja confirmar? (s/n): ")
        if confirmar.lower() == 's':
            return "Boleto", None, None, None, None
        else:
            return coletar_dados_pagamento()  ##realocação dados do pagamento###

    elif escolha_pagamento == "3":
        return "Pix", None, None, None, None

    else:
        print("Opção inválida! Tente novamente.")
        return coletar_dados_pagamento()


def adicionar_produto(nome_cliente, produto_id):
    if nome_cliente not in encomendas:
        encomendas[nome_cliente] = []

    ####contador de estoque em lista##
    for i, (id, nome, categoria, preco, quantidade) in enumerate(produtos):
        if id == produto_id:
            while True:
                quantidade_desejada = int(input("Quantidade desejada: "))
                if quantidade >= quantidade_desejada:
                    encomendas[nome_cliente].append(
                        (nome, categoria, preco, quantidade_desejada))  # quantidade##
                    produtos[i] = (id, nome, categoria, preco, quantidade - quantidade_desejada)  #refresh estoque##
                    print(f"{quantidade_desejada} unidade(s) de {nome} adicionada(s) ao pedido de {nome_cliente}.")
                    if quantidade_desejada >= 5:  ###desconto por sessão###
                        listar_cupons()
                    return
                else:
                    print(f"A quantidade solicitada excede o estoque disponível. Estoque atual: {quantidade}.")
                    print("Por favor, selecione uma nova quantidade.")
            break
    else:
        print("Produto não encontrado ou sem estoque.")

####regras descont###
def calcular_total(nome_cliente, cupom=None):
    total = 0
    if nome_cliente in encomendas:
        for nome, categoria, preco, quantidade in encomendas[nome_cliente]:
            total += preco * quantidade

    if cupom:
        desconto = validar_cupom(cupom)
        total -= total * (desconto / 100)

    return total


def aplicar_desconto(total):
    desconto = 0
    if total > 500:
        desconto = total * 0.10  # 10% de desconto
    return total - desconto, desconto


def visualizar_pedido(nome_cliente):
    if nome_cliente in encomendas and encomendas[nome_cliente]:
        print("\n--- Itens no Carrinho ---")
        for nome, categoria, preco, quantidade in encomendas[nome_cliente]:
            print(f"{nome} (Categoria: {categoria}, Preço: R$ {preco:.2f}, Quantidade: {quantidade})")
    else:
        print("Nenhum produto no carrinho.")


def finalizar_compra(nome_cliente, email):
    global numero_pedido
    cupom = input("Digite um cupom de desconto (ou deixe em branco para não usar): ")
    total = calcular_total(nome_cliente, cupom)
    total_com_desconto, desconto = aplicar_desconto(total)

    if total > 0:
        visualizar_pedido(nome_cliente)  ####detalhamento do carrinho da sessão###
        print("\n--- Detalhes do Pedido ---")
        print(f"Total a pagar para {nome_cliente}: R$ {total_com_desconto:.2f}")
        print(f"Desconto aplicado: R$ {desconto:.2f} (Cupom: {cupom})")
        print(f"\033[94mNúmero do pedido: {numero_pedido}\033[0m")
        print(f"Método de pagamento: {coletar_dados_pagamento()[0]}")
        print("Os dados do pedido também serão enviados para o seu e-mail.")
        print("\n--- Agradecemos pela sua compra! ---")

        numero_pedido += 1  ##adiciona contag. ao pedido###
        encomendas[nome_cliente] = []  ##limpa historico pedido.###
    else:
        print("Não há produtos no pedido.")

### visível ao usuário### interface
def main():
    while True:
        print("\n---Unishop---")
        print("1. Listar Produtos Disponíveis")
        print("2. Adicionar Produto")
        print("3. Remover Produto do Carrinho")
        print("4. Finalizar Compra")
        print("5. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            listar_produtos()

        elif escolha == "2":
            cliente, cpf, email = coletar_dados_cliente()
            while True:
                listar_produtos()
                produto_id = int(input("ID do produto: "))
                adicionar_produto(cliente, produto_id)
                continuar = input("Deseja adicionar mais produtos ao carrinho? (s/n): ")
                if continuar.lower() != 's':
                    break
            ###status carrinho antes de finalizar compra###
            finalizar_compra(cliente, email)

        elif escolha == "3":
            cliente = input("Nome do cliente: ")
            remover_produto(cliente)

        elif escolha == "4":
            cliente = input("Nome do cliente: ")
            finalizar_compra(cliente, email)

        elif escolha == "5":
            print("Finalizando Sessão..")
            break

        else:
            print("Opção inválida, tente novamente.")


### star.applyv1
main()