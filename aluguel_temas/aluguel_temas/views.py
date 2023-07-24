from django.shortcuts import redirect, render
from .models import *


def index(request):
    return render(request, 'index.html')

class ClientViews:
    def listClient(request):
        clients_list = Client.objects.all()
        context = {'clients_list': clients_list}
        return render(request, 'client/listClient.html', context)

    def formClient(request):
        return render(request, 'client/formClient.html')

    def saveClient(request):
        c = Client(name=request.POST['name'],
                   cpf=request.POST['cpf'])
        c.save()
        
        if(request.POST['ddd1']!=''):
            t1 = Phone(ddd=request.POST['ddd1'],
                   number=request.POST['phone1'],
                   client=c)
            t1.save()
            
        if(request.POST['ddd2']!=''):
            t2 = Phone(ddd=request.POST['ddd2'],
                   number=request.POST['phone2'],
                   client=c)
            t2.save()
            
        
        return redirect('/listClient')

    def deleteClient(request, id):
        c = Client.objects.get(pk=id)
        c.delete()
        return redirect('/listClient')

    def detailClient(request, id):
        client = Client.objects.get(pk=id)
        return render(request, 'client/formEditClient.html', {'client': client} )

    def updateClient(request, id):
        c = Client.objects.get(pk=id)
        c.name = request.POST['name']
        c.cpf = request.POST['cpf']
        c.save()
        if(request.POST['ddd1']!='' and request.POST['phone1']!='' ):
            if(c.phones.first()):
                t1 = c.phones.first()
                t1.ddd = request.POST['ddd1']
                t1.number = request.POST['phone1']
                t1.save()
            else: 
                t1 = Phone(ddd=request.POST['ddd1'],
                number=request.POST['phone1'],
                client=c)
                t1.save()
                      
        if(request.POST['ddd2']!='' and request.POST['phone2']!=''):
            if(c.phones.last() and c.phones.count()>1):
                t2 = c.phones.last()
                t2.ddd = request.POST['ddd2']
                t2.number =request.POST['phone2']
                t2.save()
            else: 
                t2 = Phone(ddd=request.POST['ddd2'],
                number=request.POST['phone2'],
                client=c)
                t2.save()    
            
        return redirect('/listClient')

class ThemeViews:
    def listTheme(request):
        themes_list = Theme.objects.all()
        context = {'theme_list': themes_list}
        return render(request, 'theme/listTheme.html', context)

    def formTheme(request):
        list_item = Item.objects.all()
        return render(request, 'theme/formTheme.html', {'list_item':list_item})

    def saveTheme(request):
        t = Theme(name=request.POST['name'], 
                    color=request.POST['color'], 
                    price=request.POST['price'],
                    )
        t.save()
        my_list = request.POST.getlist('item')

        for i in my_list:
            item = Item.objects.get(id=i)
            t.itens.add(item)
        t.save()
        return redirect('/listTheme')
    
    def deleteTheme(request, id):
        t = Theme.objects.get(pk=id)
        t.delete()
        return redirect('/listTheme')

    def detailTheme(request, id):
        theme = Theme.objects.get(pk=id)
        return render(request, 'theme/formEditTheme.html', {'theme': theme} )

    def updateTheme(request, id):
        t = Theme.objects.get(pk=id)
        t.name = request.POST['name']
        t.color = request.POST['color']
        t.price = request.POST['price']
        t.save()
        return redirect('/listTheme')

class ItemViews:
    def listItem(request):
        item_list = Item.objects.all()
        context = {'item_list': item_list}
        return render(request, 'item/listItem.html', context)

    def formItem(request):
        return render(request, 'item/formItem.html')

    def saveItem(request):
        i = Item(name=request.POST['name'], 
                 description=request.POST['description'])
        i.save()
        return redirect('/listItem')

    def deleteItem(request, id):
        i = Item.objects.get(pk=id)
        i.delete()
        return redirect('/listItem')
    
    def detailItem(request, id):
        item = Item.objects.get(pk=id)
        return render(request, 'item/formEditItem.html', {'item': item} )

    def updateItem(request, id):
        i = Item.objects.get(pk=id)
        i.name = request.POST['name']
        i.description = request.POST['description']
        i.save()
        return redirect('/listItem')

class RentViews:
    
    def listRent(request):
        rent_list = Rent.objects.all()
        context = {'rent_list': rent_list}
        return render(request, 'rent/listRent.html', context) 
    
    def formRent(request):
        client_list = Client.objects.all()
        theme_list = Theme.objects.all()
        context = {'client_list':client_list, 'theme_list': theme_list}
        return render(request, 'rent/formRent.html', context)
    
    def saveRent(request):
        a = Address(street = request.POST['street'],
                 number = request.POST['number'],
                 complement = request.POST['complement'], 
                 district = request.POST['district'],
                 city = request.POST['city'],
                 state = request.POST['state'],
                 cep = request.POST['cep'] )
        a.save()
        
        r = Rent(date=request.POST['date'], 
                 start_hours=request.POST['start_hours'],
                 end_hours=request.POST['end_hours'],
                 client_id= request.POST['select_client'],
                 theme_id = request.POST['select_theme'],
                 address = a )
        r.save()
        return redirect('/listRent')

    def deleteRent(request, id):
        i = Rent.objects.get(pk=id)
        i.delete()
        return redirect('/listRent')
    
    def detailRent(request, id):
        rent = Rent.objects.get(pk=id)
        return render(request, 'rent/formEditRent.html', {'rent': rent})
    
    def updateRent(request, id):
        r = Rent.objects.get(pk=id)
        r.date = request.POST['date']
        r.start_hours = request.POST['start_hours']
        r.end_hours = request.POST['end_hours']
        
        addr = r.address
        
        if not addr:
            addr = Address(street = request.POST['street'],
                number = int(request.POST['number']),
                complement = request.POST['complement'],
                district = request.POST['district'],
                city = request.POST['city'],
                state = request.POST['state'])
            
            print('novo endereco')
        else:
            print(r.address)
            addr.street = request.POST['street']
            addr.number = int(request.POST['number'])
            addr.complement = request.POST['complement']
            addr.district = request.POST['district']
            addr.city = request.POST['city']
            addr.state = request.POST['state']
            print('endereco atualizado')
        addr.save()
        r.address = addr
        r.save()
        return redirect('/listRent')