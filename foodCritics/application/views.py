from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Comentarios, Restaurantes, Categorias, Usuarios, plato
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import googlemaps

login_check = False
# Create your views here.\

API_KEY = '' #Identificador en la API de Google --- YOUR API KEY

gmaps = googlemaps.Client(key=API_KEY)

#Ubicacion geofrafica del usuario
coordinatesLatitude = ''
coordinatesLongitude = ''

puntos_user = 0

bonos = [40,50,50,25,75,40] 

@csrf_exempt
def home(request):
  global puntos_user, coordinatesLatitude, coordinatesLongitude

  searchTerm = request.GET.get('search')
  rest = Restaurantes.objects.all()

  if searchTerm:
    if(Restaurantes.objects.filter(name__icontains=searchTerm)):
      rest = Restaurantes.objects.filter(name__icontains = searchTerm)

    elif(Categorias.objects.filter(tipo__icontains=searchTerm)):
      temp = Categorias.objects.get(tipo__icontains=searchTerm)
      rest = Restaurantes.objects.filter(type = temp)

  #Si el usuario permite conocer la ubicacion, la almacena
  if request.method == 'POST':
    coordinatesLatitude = request.POST['latitudes']
    coordinatesLongitude = request.POST['longitudes']
    
    consulta()

  return render(request, 'home.html', {'restaurants' : rest, 'puntos' : puntos_user})

#Obtencion de restaurantes cerca de la ubicacion especificada en un radio de 1000 metros
def consulta():
  places_result = gmaps.places_nearby(location=f'{coordinatesLatitude}, {coordinatesLongitude}', radius='1000', type='restaurant', open_now=False)

  #Almacenar los datos que seran usados de los restaurantes en la variable restaurantes

  for place in places_result['results']:

    my_place_id = place['place_id']

    nombre = place['name']

    location = place['geometry']['viewport']['northeast']

    #Campos que seran almacenados en la base de datos
    parametros_datos = gmaps.place(place_id=my_place_id, fields= ['rating'], language="ES")

    parametros_reviews = gmaps.place(place_id=my_place_id, fields=['review'], language="ES")

    #Comentarios hechos por usuarios
    comentarios = []

    #Valoracion general del restaurante
    rating_rest = 0

    #Almacena los comentarios del restaurante dentro de la variable comentarios
    try:
      data_user = parametros_reviews['result']['reviews']

      #Por cada comentario sacado de la API de google, toma los datos necesarios
      for data in data_user:
        name = data['author_name']
        time = data['relative_time_description']
        text = data['text']
        rating = data['rating']

        rating_rest += rating

        comentarios.append({'author': name, 'time': time, 'text': text, 'rating': rating})

      rating_rest /= len(data_user) if len(data_user) > 0 else 1

    except:
      None


    #Creacion del restaurante en la base de datos, en caso de existir lo actualiza

    try:
      Restaurantes.objects.filter(place_id = my_place_id).update(name= nombre, address= place['vicinity'], rating = rating_rest, location = location)
      Comentarios.objects.filter(place_id = my_place_id).update(reviews = comentarios)

    except:
      Restaurantes.objects.create(name= nombre, address= place['vicinity'], place_id = my_place_id, rating = rating_rest, location = location)
      Comentarios.objects.create(place_id = my_place_id, reviews = comentarios)


def enviarRestaurante(request):
  
  global puntos_user

  id = request.GET['restaurant']

  my_fields = ['name', 'price_level', 'rating', 'formatted_address', 'user_ratings_total', 'review', 'place_id']

  restaurante = Restaurantes.objects.get(place_id=id)
  comentarios = Comentarios.objects.get(place_id=id)

  if request.POST:
    author = request.POST['name_user']
    text = request.POST['comentario_user']
    rating = request.POST['puntuacion_user']

    message = f'nombre: {author}\ncomentario: {text}\npuntuacion: {rating}'

    print(message)

    comentario = {"author" : author, "time" : "No definido", "text" : text, "rating" : rating}
    
    comentarios.reviews.append(comentario)

    almacenar_comentarios = []

    for coment in comentarios.reviews:
      almacenar_comentarios.append(coment)

    puntos_user += 10

    Comentarios.objects.filter(place_id = id).update(reviews = almacenar_comentarios)

  return render(request, 'restaurante.html', {'place_id' : id, 'restaurante' : restaurante, 'comentarios' : comentarios, 'puntos' : puntos_user})

def restauranteIniciado(request):
  
  global puntos_user

  id = request.GET['restaurant']

  my_fields = ['name', 'price_level', 'rating', 'formatted_address', 'user_ratings_total', 'review', 'place_id']

  restaurante = Restaurantes.objects.get(place_id=id)
  comentarios = Comentarios.objects.get(place_id=id)
  detalle = request.session['email']
  detalleUsuario = Usuarios.objects.get(email = detalle)
  if request.POST:
    author = request.POST['name_user']
    text = request.POST['comentario_user']
    rating = request.POST['puntuacion_user']

    message = f'nombre: {author}\ncomentario: {text}\npuntuacion: {rating}'

    print(message)

    comentario = {"author" : author, "time" : "No definido", "text" : text, "rating" : rating}
    
    comentarios.reviews.append(comentario)

    almacenar_comentarios = []

    for coment in comentarios.reviews:
      almacenar_comentarios.append(coment)

    puntos_user += 10

    Comentarios.objects.filter(place_id = id).update(reviews = almacenar_comentarios)

  return render(request, 'restauranteIniciado.html', {'place_id' : id, 'restaurante' : restaurante, 'comentarios' : comentarios, 'puntos' : puntos_user, "detalle":detalleUsuario})


def mapa(request):
  global puntos_user, coordinatesLongitude, coordinatesLatitude, API_KEY

  rest = Restaurantes.objects.all()

  coordinates = { 'lat': coordinatesLatitude, 'lng': coordinatesLongitude}

  return render(request, 'mapa.html', {'puntos' : puntos_user, 'coordinates' : coordinates, 'KEY': API_KEY, 'restaurants': rest})

def mapaIngresado(request):
  global puntos_user, coordinatesLongitude, coordinatesLatitude, API_KEY

  rest = Restaurantes.objects.all()

  coordinates = { 'lat': coordinatesLatitude, 'lng': coordinatesLongitude}
  detalle = request.session['email']
  detalleUsuario = Usuarios.objects.get(email = detalle)

  return render(request, 'mapaIngresado.html', {'puntos' : puntos_user, 'coordinates' : coordinates, 'KEY': API_KEY, 'restaurants': rest, 'detalle' : detalleUsuario})


@csrf_exempt
def puntos(request):

  global puntos_user, bonos
  detalle = request.session['email']
  detalleUsuario = Usuarios.objects.get(email = detalle)

  puntos_user = detalleUsuario.points

  if request.POST:

    redeem = request.POST['redeem']

    puntos_user -= int(redeem)

    Usuarios.objects.filter(email = detalle).update(points = puntos_user)



  return render(request, 'puntos.html', {'puntos' : puntos_user, 'bonos': bonos,'detalle' : detalleUsuario})



def puntuacionTotal(comentarios):
  puntuacion_total = 0

  for datos in comentarios.reviews:

    print(datos)

    rating = int(datos['rating'])

    puntuacion_total += rating
  
  puntuacion_total /= len(comentarios.reviews) if len(comentarios.reviews) > 0 else 1

  return puntuacion_total

def menu(request):
  global puntos_user
  id = request.GET['menu']
  restaurante = Restaurantes.objects.get(place_id=id)
  menu = plato.objects.filter(restaurante=id)
  detalle = request.session['email']
  detalleUsuario = Usuarios.objects.get(email = detalle)
  return render(request, 'menu.html', {'place_id' : id , 'menu' : menu, 'puntos' : puntos_user, 'restaurante' : restaurante, 'detalle' : detalleUsuario})

def menuMayor(request):
  global puntos_user
  id = request.GET['menu']
  menu = plato.objects.filter(restaurante=id)
  detalle = request.session['email']
  detalleUsuario = Usuarios.objects.get(email = detalle)
  restaurante = Restaurantes.objects.get(place_id=id)
  menu = menu.order_by('-price')
  return render(request, 'menu.html', {'place_id' : id , 'menu' : menu, 'puntos' : puntos_user,'restaurante' : restaurante,'detalle' : detalleUsuario})

def menuMenor(request):
  global puntos_user
  id = request.GET['menu']
  detalle = request.session['email']
  detalleUsuario = Usuarios.objects.get(email = detalle)
  menu = plato.objects.filter(restaurante=id)
  restaurante = Restaurantes.objects.get(place_id=id)
  menu = menu.order_by('price')

  return render(request, 'menu.html', {'place_id' : id , 'menu' : menu, 'puntos' : puntos_user,'restaurante' : restaurante, 'detalle' : detalleUsuario})
  
def busquedaRestaurante(request):
  termino = request.POST.get('search')

  restaurantes = Restaurantes.objects.all()
  if termino:
    if Restaurantes.objects.filter(name=termino):
      restarurantes = Restaurantes.objects.filter(name_icontains = termino)

def reviewMenu(request):
  global puntos_user
  id = request.GET['reviewMenu']
  #print(id)
  platos = plato.objects.filter(id=id)
  comentarios = plato.objects.get(id=id)
  detalle = request.session['email']
  detalleUsuario = Usuarios.objects.get(email = detalle)
  #print(platos)
  if request.POST:
    author = request.POST['name_user']
    text = request.POST['comentario_user']
    rating = request.POST['puntuacion_user']

    message = f'nombre: {author}\ncomentario: {text}\npuntuacion: {rating}'

    print(message)

    comentario = {"author" : author, "time" : "No definido", "text" : text, "rating" : rating}
    
    comentarios.reviews.append(comentario)

    almacenar_comentarios = []

    for coment in comentarios.reviews:
      almacenar_comentarios.append(coment)

    puntos_user += 10

    plato.objects.filter(id = id).update(reviews = almacenar_comentarios)

  return render(request, 'reviewMenu.html',{'plato':platos, 'puntos': puntos_user, 'detalle':detalleUsuario})


def Registro(request):
  if request.method == 'POST':

    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['pass']
    points = request.POST['points']

    if verifica_registro(email):
      messages.info(request, "Usuario ya resgistrado, por favor ingresa")
    else:  
      agregar = Usuarios(name = name, email = email, password = password, points = points)
      agregar.save()
      return render(request, 'salto2.html')

  return render(request, 'registro.html')

def verifica_registro(criterio):
  query = False
  if True:
    query = Usuarios.objects.filter(email = criterio).exists()
  return query
def Ingreso(request):
  global login_check
  rest = Restaurantes.objects.all()
  if login_check:
    return render(request, 'homeiniciado.html')
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['pass']
    try:
      detalleUsuario = Usuarios.objects.get(email = request.POST['email'], password = request.POST['pass'])
      request.session['email'] = detalleUsuario.email
      request.session['pass'] = detalleUsuario.password
      request.session['id'] = detalleUsuario.id
      request.session['points'] = detalleUsuario.id
      login_check = True
      return render(request, 'salto2.html')

    except Usuarios.DoesNotExist as e:
      messages.info(request,"Correo y/o contraseña no son correctos")

  return render (request, 'ingreso.html')

def HomeIniciado(request):
  global login_check 
  searchTerm = request.GET.get('search')
  rest = Restaurantes.objects.all()
  detalle = request.session['email']
  detalleUsuario = Usuarios.objects.get(email = detalle)

  if searchTerm:
    if(Restaurantes.objects.filter(name__icontains=searchTerm)):
      rest = Restaurantes.objects.filter(name__icontains = searchTerm)

    elif(Categorias.objects.filter(tipo__icontains=searchTerm)):
      temp = Categorias.objects.get(tipo__icontains=searchTerm)
      rest = Restaurantes.objects.filter(type = temp)

  return render(request, 'homeiniciado.html',{"detalle":detalleUsuario, 'restaurants' : rest})

def logout_request(request):
  global login_check
  login_check = False
  return Salto(request)

def Salto(request):
  global login_check
  return render(request, 'salto.html')

def Salto2(request):
  global login_check
  return render(request, 'salto2.html')

def destacados(request):
  restaurantes = Restaurantes.objects.order_by('-rating')
  return render(request, 'destacados.html', {'restaurants': restaurantes[0:5], 'puntos': puntos_user})
