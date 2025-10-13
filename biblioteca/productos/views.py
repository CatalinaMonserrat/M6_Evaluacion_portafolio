from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def libro_list(request):
    #sin BD todavia, simulamos datos
    libros_simulados = [
        {'id':1, 'titulo':'El señor de los anillos', 'autor':'JRR Tolkien'},
        {'id':2, 'titulo':'El hobbit', 'autor':'JRR Tolkien'},
        {'id':3, 'titulo':'El silmarillion', 'autor':'JRR Tolkien'},
    ]
    return render(request, 'libro_list.html', {'libros':libros_simulados})

def libro_detail(request, pk):
    libro = {'id':pk, 'titulo':'El señor de los anillos', 'autor':'JRR Tolkien', 'precio': 9990}
    return render(request, 'libro_detail.html', {'libro_id':libro})

