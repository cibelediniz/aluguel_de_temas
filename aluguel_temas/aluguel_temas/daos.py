from .models import *


class ClienteDAO:
    def listaClientes():
        # Retorna uma lista de todos os clientes no banco de dados.
        lista_clientes = Client.objects.all()
        return lista_clientes

    def salvaCliente(dados):
        # Cria um novo cliente no banco de dados com base nos dados fornecidos
        c = Client(name=dados['name'], cpf=dados['cpf'])
        c.save()

        # Salva até dois números de telefone associados ao cliente, se fornecidos
        if dados['ddd1'] != '':
            t1 = Phone(ddd=dados['ddd1'], number=dados['phone1'], client=c)
            t1.save()

        if dados['ddd2'] != '':
            t2 = Phone(ddd=dados['ddd2'], number=dados['phone2'], client=c)
            t2.save()

    def deletaCliente(id):
        # Deleta um cliente do banco de dados com base no ID fornecido
        c = Client.objects.get(pk=id)
        c.delete()

    def detalheCliente(id):
        # Retorna os detalhes de um cliente específico com base no ID fornecido
        return Client.objects.get(pk=id)

    def atualizaCliente(dados, id):
        # Atualiza os dados de um cliente existente com base no ID fornecido
        c = Client.objects.get(pk=id)
        c.name = dados['name']
        c.cpf = dados['cpf']
        c.save()

        # Atualiza ou cria até dois números de telefone associados ao cliente, se fornecidos
        if dados['ddd1'] != '' and dados['phone1'] != '':
            if c.phones.first():
                t1 = c.phones.first()
                t1.ddd = dados['ddd1']
                t1.number = dados['phone1']
                t1.save()
            else:
                t1 = Phone(ddd=dados['ddd1'], number=dados['phone1'], client=c)
                t1.save()

        if dados['ddd2'] != '' and dados['phone2'] != '':
            if c.phones.last() and c.phones.count() > 1:
                t2 = c.phones.last()
                t2.ddd = dados['ddd2']
                t2.number = dados['phone2']
                t2.save()
            else:
                t2 = Phone(ddd=dados['ddd2'], number=dados['phone2'], client=c)
                t2.save()


class TemaDAO:
    def listaTemas():
        # Retorna uma lista de todos os temas no banco de dados
        lista_temas = Theme.objects.all()
        return lista_temas

    def salvaTema(dados):
        # Cria um novo tema no banco de dados com base nos dados fornecidos, incluindo relacionamentos ManyToMany com itens
        t = Theme(name=dados['name'], color=dados['color'], price=dados['price'])
        t.save()

        minha_lista = dados.getlist('item')
        for i in minha_lista:
            # Obtem e adiciona os itens associados ao tema com base nos IDs fornecidos
            item = Item.objects.get(id=i)
            t.itens.add(item)
        t.save()

    def detalheTema(id):
        # Retorna os detalhes de um tema específico com base no ID fornecido
        return Theme.objects.get(pk=id)

    def deletaTema(id):
        # Deleta um tema do banco de dados com base no ID fornecido
        t = Theme.objects.get(pk=id)
        t.delete()

    def atualizaTema(dados, id):
        # Atualiza os dados de um tema existente com base no ID fornecido
        t = Theme.objects.get(pk=id)
        t.name = dados['name']
        t.color = dados['color']
        t.price = dados['price']
        t.save()


class ItemDAO:
    def listaItens():
        # Retorna uma lista de todos os itens no banco de dados
        lista_itens = Item.objects.all()
        return lista_itens

    def salvaItem(dados):
        # Cria um novo item no banco de dados com base nos dados fornecidos
        i = Item(name=dados['name'], description=dados['description'])
        i.save()

    def deletaItem(id):
        # Deleta um item do banco de dados com base no ID fornecido
        i = Item.objects.get(pk=id)
        i.delete()

    def detalheItem(id):
        # Retorna os detalhes de um item específico com base no ID fornecido
        return Item.objects.get(pk=id)

    def atualizaItem(dados, id):
        # Atualiza os dados de um item existente com base no ID fornecido
        i = Item.objects.get(pk=id)
        i.name = dados['name']
        i.description = dados['description']
        i.save()


class AluguelDAO:
    def listaAlugueis():
        # Retorna uma lista de todos os aluguéis no banco de dados
        lista_alugueis = Rent.objects.all()
        return lista_alugueis

    def salvaAluguel(dados):
        # Cria um novo aluguel no banco de dados com base nos dados fornecidos
        e = Address(street=dados['street'], number=dados['number'], complement=dados['complement'],
                     district=dados['district'], city=dados['city'], state=dados['state'], cep=dados['cep'])
        e.save()

        a = Rent(date=dados['date'], start_hours=dados['start_hours'], end_hours=dados['end_hours'],
                    client_id=dados['select_client'], theme_id=dados['select_theme'], address=e)
        a.save()

    def deletaAluguel(id):
        # Deleta um aluguel do banco de dados com base no ID fornecido
        a = Rent.objects.get(pk=id)
        a.delete()

    def detalheAluguel(id):
        # Retorna os detalhes de um aluguel específico com base no ID fornecido
        return Rent.objects.get(pk=id)

    def atualizaAluguel(dados, id):
        # Atualiza os dados de um aluguel existente com base no ID fornecido
        a = Rent.objects.get(pk=id)
        a.date = dados['date']
        a.start_hours = dados['start_hours']
        a.end_hours = dados['end_hours']

        end = a.address
        if not end:
            # Se não houver um endereço associado ao aluguel, cria um novo endereço
            end = Address(street=dados['street'], number=dados['number'], complement=dados['complement'],
                           district=dados['district'], city=dados['city'], state=dados['state'])
            print('novo endereço.')
        else:
            # Caso contrário, atualiza o endereço existente
            end.street = dados['street']
            end.number = dados['number']
            end.complement = dados['complement']
            end.district = dados['district']
            end.city = dados['city']
            end.state = dados['state']
            print('endereço atualizado.')
        end.save()
        a.address = end
        a.save()
