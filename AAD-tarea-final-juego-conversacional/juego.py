import mysql.connector
import pickle
from validador import validar_sintaxis  # El archivo validador.py debe estar en la misma carpeta que este

# Conexión a la base de datos
connect = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "admin",
  database = "juego"
)
cursor = connect.cursor()

# Datos de la BD
lista_salas = []  # [id_sala, descripcion]
lista_salidas = []  # [id_sala, salida, id_salida]
lista_objetos = []  # [nombre_objeto, id_sala]
lista_personajes = []  # [id_sala, nombre_personaje]
record = 0

# Datos de la partida
nombre_jugador = ""
monedas = 0
puntos = 0
inventario = []
sala_actual = 1
salas_visitadas = []
flags = [
  ["mesa examinada", False],
  ["candelabro recogido", False],
  ["cuadro examinado", False],
  ["llave recogida", False],
  ["cofre abierto", False],
  ["monedas recogidas", False],
  ["cuchillo recogido", False],
  ["guerrero asesinado", False],
  ["escudo recogido", False],
  ["candelabro vendido", False],
  ["palanca comprada", False],
  ["final desbloqueado", False]
]

# Miscelánea
ordenes_validas_por_sala = [
  [
    0, [  # En todas las salas
      "inventario", "nuevo", "guardar", "cargar", "mapa", "ayuda", "ir norte", "ir sur", "ir este", "ir oeste"
    ]
  ],
  [
    1, [
      "coger candelabro", "mirar mesa", "mirar candelabro"
    ]
  ],
  [
    2, [
      "abrir cofre", "abrir cofre con llave", "coger llave", "coger monedas", "mirar cuadro", "mirar llave", "mirar cofre", "mirar monedas", "usar llave con cofre"
    ]
  ],
  [
    3, [
      "coger escudo", "coger cuchillo", "hablar con guerrero", "mirar guerrero", "mirar escudo", "mirar cuchillo", "usar cuchillo con guerrero", "empujar guerrero con cuchillo"
    ]
  ],
  [
    4, [
      "comprar palanca", "vender candelabro", "hablar con tendero", "mirar tendero"
    ]
  ],
  [
    5, [
      "usar palanca"
    ]
  ]
]

mensaje_error_sintaxis = "No entiendo lo que me estás pidiendo."
mensaje_error_orden_no_valida = "No tiene sentido hacer eso."
mensaje_error_accion_repetida = "Ya has hecho eso."


def guardar_partida():
  global nombre_jugador, monedas, puntos, inventario, sala_actual, salas_visitadas, flags

  # Guardar el archivo en disco
  datos_partida = [
    nombre_jugador, monedas, puntos, inventario, sala_actual, salas_visitadas, flags
  ]
  nombre_archivo = "{}_savegame.pickle".format(nombre_jugador)
  archivo_guardado = open(nombre_archivo, 'wb')
  pickle.dump(datos_partida, archivo_guardado)
  archivo_guardado.close()

  # Guardar el nombre de archivo en la BD
  sql = "SELECT * FROM partidas_guardadas"
  cursor.execute(sql)
  # Si ya existe una partida con este nombre, sobreescribirla
  for i in cursor:
    if i[0] == nombre_jugador:
      sql = "DELETE FROM partidas_guardadas WHERE jugador = '{}'".format(nombre_jugador)
      cursor.execute(sql)

  sql = "INSERT INTO partidas_guardadas VALUES ('{}', '{}')".format(nombre_jugador, nombre_archivo)
  cursor.execute(sql)
  connect.commit()
  print("Partida guardada en {}.".format(nombre_archivo))

def cargar_partida():
  global nombre_jugador, monedas, puntos, inventario, sala_actual, salas_visitadas, flags

  # Cargar partida de la BD
  nombre_archivo = ""
  sql = "SELECT * FROM partidas_guardadas"
  cursor.execute(sql)
  # Buscar el nombre de archivo de este personaje
  for i in cursor:
    if i[0] == nombre_jugador:
      nombre_archivo = i[1]

  if nombre_archivo == "":
    print("No se han encontrado partidas guardadas con este personaje.")
    return

  # Cargar el archivo del disco
  try:
    archivo_carga = open(nombre_archivo, 'rb')
  except FileNotFoundError:
    print("El archivo que se ha encontrado en la base de datos no se ha podido abrir. Comprueba que existe en la carpeta de partidas.")
    return
  
  datos_partida = pickle.load(archivo_carga)
  archivo_carga.close()

  # Reemplazar los datos actuales con los del pickle
  nombre_jugador = datos_partida[0]
  monedas = datos_partida[1]
  puntos = datos_partida[2]
  inventario = datos_partida[3]
  sala_actual = datos_partida[4]
  salas_visitadas = datos_partida[5]
  flags = datos_partida[6]

  ir_sala(sala_actual)


# Guardar puntos en la BD
def registrar_puntuacion():
  # Insertar la partida en la tabla de puntuaciones
  sql = "INSERT INTO puntuaciones(puntuacion, jugador) VALUES ({}, '{}')".format(puntos, nombre_jugador)
  cursor.execute(sql)
  connect.commit()

  if puntos > record:
    print("\n¡Enhorabuena! ¡Has establecido un nuevo récord!")
    # Si es nuevo récord, copiar la información recién insertada a la tabla record
    sql = "SELECT * FROM puntuaciones WHERE puntuacion = {} AND jugador = '{}'".format(puntos, nombre_jugador)
    cursor.execute(sql)
    for i in cursor:
      consulta = [i[0], i[1], i[2]]

    # Borrar el récord anterior
    sql = "DELETE FROM record"
    cursor.execute(sql)

    # Insertar el récord actual
    sql = "INSERT INTO record VALUES({}, {}, '{}')".format(consulta[0], consulta[1], consulta[2])
    cursor.execute(sql)
    connect.commit()

  print("Partida guardada.")
  return


# Añade el parámetro al inventario y suma los puntos correspondientes
def agregar_objeto_a_inventario(objeto):
  global puntos

  print("Metes [{}] en tu mochila.".format(objeto))
  inventario.append(objeto)
  print("¡Has encontrado un objeto! +50 puntos.")
  puntos = puntos + 50


# Comprobar si la dirección introducida por el usuario es válida. Devuelve una sala, o -1 si no hay salidas en esa dirección.
def comprobar_salidas(direccion):
  global sala_actual

  for i in lista_salidas:  # Para cada movimiento en el juego
    if i[0] == sala_actual:  # Filtrar por los movimientos de la sala actual
      if direccion == i[1]:  # Si la orden se corresponde a una salida
        return i[2]  # Devolver la sala de destino

  # De lo contrario
  print("No hay ninguna puerta en esa dirección.")
  return -1


# Función para ejecutar todas las órdenes disponibles
def ejecutar_orden(orden):
  global inventario, flags, lista_salidas, monedas, puntos

  # En todas las salas
  if orden == "inventario":
    if len(inventario) < 1:
      print("No tienes nada en la mochila.")
    else:
      print("Rebuscas en tu mochila en busca de algo útil. Tienes:")
      for item in inventario:
        print("\t{}".format(item))

  if orden == "nuevo":
    iniciar_partida()

  if orden == "guardar":
    guardar_partida()
  if orden == "cargar":
    cargar_partida()

  if orden == "mapa":
    print("[1] <-> [2] <-> [5] -> EXIT    N  ")
    print(" ^       ^                     ^  ")
    print(" |       |                   O<·>E")
    print(" v       v                     v  ")
    print("[3]     [4]                    S  ")

  if orden == "ir norte":
    sala_destino = comprobar_salidas("norte")
    if sala_destino != -1:
      ir_sala(sala_destino)

  if orden == "ir sur":
    sala_destino = comprobar_salidas("sur")
    if sala_destino != -1:
      ir_sala(sala_destino)

  if orden == "ir este":
    sala_destino = comprobar_salidas("este")
    if sala_destino != -1:
      ir_sala(sala_destino)

  if orden == "ir oeste":
    sala_destino = comprobar_salidas("oeste")
    if sala_destino != -1:
      ir_sala(sala_destino)

  if orden == "ayuda":
    print("Prueba a mirar alrededor. Mira todo lo que consideres interesante, quizá así encuentres alguna pista.")

  # Para la sala 1
  if sala_actual == 1:
    if orden == "coger candelabro":
      if comprobar_progreso("candelabro recogido"):
        print(mensaje_error_accion_repetida + "\n")
      else:
        if comprobar_progreso("mesa examinada"):
          agregar_objeto_a_inventario("candelabro")
          modificar_progreso("candelabro recogido", True)
        else:
          print(mensaje_error_sintaxis + "\n")

    if orden == "mirar mesa":
      print("Es una mesa de madera de roble que te llega por la cintura. Parece lo suficientemente larga para albergar a unas 12 personas, pero no hay ninguna silla alrededor, ni muestras de que haya sido usada en mucho tiempo.")
      if comprobar_progreso("candelabro recogido"):
        print("Está completamente vacía, con una visible falta de polvo en el centro.")
      else:
        print("Hay un candelabro apagado en el centro.")
        modificar_progreso("mesa examinada", True)

    if orden == "mirar candelabro":
      if comprobar_progreso("mesa examinada"):
        print("Es un candelabro ornamentado, y su fabricación es de la mejor calidad. Aunque está cubierto de polvo, las velas aún no se han gastado. No tienes cerillas para encenderlas, pero estimas que podrías regatear algo de oro por él.")
      else:
        print(mensaje_error_sintaxis + "\n")

  # Para la sala 2
  if sala_actual == 2:
    if orden == "abrir cofre" or orden == "abrir cofre con llave" or orden == "usar llave con cofre":
      if comprobar_progreso("cofre abierto"):
        print(mensaje_error_accion_repetida + "\n")
      else:
        if comprobar_progreso("llave recogida"):
          print("La llave encaja perfectamente en la cerradura. *CLAC* Giras la muñeca y la cerradura cae al suelo con un ruido seco. El cofre está abierto.")
          modificar_progreso("cofre abierto", True)
        else:
          print("No tienes la llave para abrir la cerradura, ni una ganzúa para forzarla.")

    if orden == "coger llave":
      if comprobar_progreso("llave recogida"):
        print(mensaje_error_accion_repetida + "\n")
      else:
        if comprobar_progreso("cuadro examinado"):
          agregar_objeto_a_inventario("llave")
          modificar_progreso("llave recogida", True)
        else:
          print(mensaje_error_sintaxis + "\n")

    if orden == "coger monedas":
      if comprobar_progreso("monedas recogidas"):
        print(mensaje_error_accion_repetida + "\n")
      else:
        if comprobar_progreso("cofre abierto"):
          print("Metes las monedas en tu mochila.")
          monedas = monedas + 100
          modificar_progreso("monedas recogidas", True)
        else:
          print(mensaje_error_sintaxis + "\n")

    if orden == "mirar cuadro":
      print("Es un cuadro de un paisaje campestre. El terreno es completamente llano y en el fondo se discierne una casa blanca con un tejado rojo. Te quedas unos minutos admirando la simpleza de la composición, la selección de colores y el detalle del cielo azul. Admirar este cuadro te trae recuerdos de tu tierra. Ardes en ansias de salir de aquí.")
      if comprobar_progreso("cuadro examinado"):
        print("Está en el suelo apoyado contra la pared. Ocultaba un hueco con una llave.")
      else:
        print("Algo no te cuadra, parece que no está recto del todo. Levantas el cuadro de su clavo y lo colocas en el suelo. Detrás hay un hueco pequeño en la pared en el que descansa una llave de cobre llena de polvo.")
        modificar_progreso("cuadro examinado", True)

    if orden == "mirar llave":
      if comprobar_progreso("cuadro examinado"):
        print("Es una llave de cobre de unos ocho centímetros de longitud. Tiene una fina capa de polvo por encima y algunas muecas revelan que ha sido usada más de mil veces.")
        if comprobar_progreso("cofre abierto"):
          print("La has usado para abrir el cofre del final de la sala.")
        else:
          print("Quizá haya alguna cerradura cerca donde puedas usarla.")
      else:
        print(mensaje_error_sintaxis + "\n")

    if orden == "mirar cofre":
      # FIXME: la orden se ejecuta correctamente, pero justo después se imprime el mensaje de orden no válida
      print("Es un cofre de madera de roble, con tablones de unos cinco centímetros de grosor y unos remates de hierro. Tiene una cerradura de cobre que parece desgastada, tanto por el tiempo como por ladrones que no tuvieron suerte forzándola.")
      if comprobar_progreso("cofre abierto"):
        print("Pero tú has encontrado la llave y ahora sus secretos no se te resisten.")
        if comprobar_progreso("monedas recogidas"):
          print("Has cogido todas las monedas que había dentro.")
        else:
          print("Hay una montaña de monedas de oro en su interior.")
      else:
        print("Y parece que de momento tú tampoco tienes suerte.")

    if orden == "mirar monedas":
      if comprobar_progreso("cofre abierto"):
        if comprobar_progreso("monedas recogidas"):
          print("Has cogido todas las monedas que había dentro del cofre.")
        else:
          print("Cuentas una centena de monedas de oro con el emblema del rey esparcidas sin reparo en el cofre de madera. Te preguntas quién las ha guardado aquí, y si podrías encontrar más por alguna otra parte.")
      else:
        print(mensaje_error_sintaxis + "\n")

  # Para la sala 3
  if sala_actual == 3:
    if orden == "coger escudo":
      if comprobar_progreso("escudo recogido"):
        print(mensaje_error_accion_repetida + "\n")
      else:
        if comprobar_progreso("guerrero asesinado"):
          agregar_objeto_a_inventario("escudo")
          modificar_progreso("escudo recogido", True)
        else:
          print("Forcejeas con el guerrero para arrancarle el escudo de las manos, pero es un soldado entrenado y lleva vigilándote desde que te ha visto venir. De un empujón caes al suelo. Te duele la cabeza.")

    if orden == "coger cuchillo":
      if comprobar_progreso("cuchillo recogido"):
        print(mensaje_error_accion_repetida + "\n")
      else:
        agregar_objeto_a_inventario("cuchillo")
        modificar_progreso("cuchillo recogido", True)
        print("El guerrero te ve y grita: \"¡Eh, eh! ¿Qué crees que estás haciendo? Deja eso, vamos.\"")

    if orden == "hablar con guerrero":
      if comprobar_progreso("guerrero asesinado"):
        print("Seguro que te crees muy gracioso ahora mismo. El guerrero no responde, obviamente.")
      else:
        print("El guerrero, aunque cansado, tiene la guardia alta y no se fía de ti. Presta atención a tus movimientos, no a tus palabras.")

    if orden == "mirar guerrero":
      if comprobar_progreso("guerrero asesinado"):
        print("Antes era un superviviente como tú, que intentaba salir de la fortaleza a pesar de sus heridas físicas y mentales. Ahora es un cadáver.")
        if comprobar_progreso("escudo recogido"):
          print("Por si fuera poco, le has robado el escudo. Al menos ha sido rápido.")
        else:
          print("Ha dejado caer su escudo, quizá puedas darle un nuevo uso.")
      else:
        print("Es un guerrero de la guardia real, entrenado para defender esta fortaleza. Lleva una armadura de acero templado y su yelmo luce el emblema del rey. Parece magullado y te mira de reojo con desconfianza. Empuña su escudo con fuerza y una pizca de orgullo.")

    if orden == "mirar escudo":
      print("Es un escudo de acero con el emblema del rey. Está oxidado por el borde.")
      if comprobar_progreso("guerrero asesinado"):
        print("Y también cubierto de sangre.")
      else:
        print("El guerrero lo empuña con fuerza y una pizca de orgullo.")

    if orden == "mirar cuchillo":
      print("Es un cuchillo de acero templado, con un emblema del rey en el mango. El guerrero lo ha dejado en el suelo mientras descansaba.")

      if comprobar_progreso("cuchillo recogido"):
        if comprobar_progreso("guerrero asesinado"):
          print("Está manchado de sangre.")
        else:
          print("Piénsatelo dos veces antes de usarlo.")
      else:
        print("Con tan solo verlo se te llena la mente de ideas. Está ahí tirado, esperando a que lo cojas.")

    if orden == "usar cuchillo con guerrero" or orden == "empujar guerrero con cuchillo":
      if comprobar_progreso("guerrero asesinado"):
        print(mensaje_error_accion_repetida + "\n")
        print("¿De verdad quieres hacerlo otra vez?")
      else:
        if "cuchillo" not in inventario:
          print("No tienes un cuchillo para hacer eso. Todavía. Pero tampoco es que vayas a hacerlo, ¿verdad?")
        else:
          print("Te lanzas encima del guerrero y le incrustas el cuchillo en el costado expuesto. El guerrero grita con todas sus fuerzas. Para que se calle, le rebanas el cuello. Te recompones y vuelves a levantarte. El guerrero ha dejado caer su escudo. Ya está hecho.")
          modificar_progreso("guerrero asesinado", True)

  # Para la sala 4
  if sala_actual == 4:
    if orden == "comprar palanca":
      if comprobar_progreso("palanca comprada"):
        print(mensaje_error_accion_repetida + "\n")
      else:
        if monedas >= 90:
          print("El tendero pide 90 monedas por la palanca. Poco a poco las sacas de tu mochila y se las dejas en el mostrador. Te dice: \"Un placer hacer negocios contigo.\" No sabes si lo dice de verdad o porque es su trabajo.")
          monedas = monedas - 90
          agregar_objeto_a_inventario("palanca")
          modificar_progreso("palanca comprada", True)
          print("¡Has comprado un objeto! +75 puntos.")
          puntos = puntos + 75
        else:
          print("No tienes suficiente dinero para permitírtelo.")

    if orden == "vender candelabro":
      if "candelabro" in inventario:
        print("Recibes 50 monedas por tu venta.")
        modificar_progreso("candelabro vendido", True)
        inventario.remove("candelabro")
        monedas = monedas + 50
      else:
        print(mensaje_error_orden_no_valida + "\n")

    if orden == "hablar con tendero":
      print("El tendero dice: \"Tengo una palanca muy especial a la venta, si estás interesado en comprarla. Tan sólo 90 monedas de nada.\"")
    if orden == "mirar tendero":
      print("El tendero te devuelve la mirada, sonriente. Está observando tu mochila con especial atención, esperando que le vendas algo.")

  # Para la sala 5
  if sala_actual == 5:
    if orden == "usar palanca":
      if "palanca" in inventario:
        print("Usas la palanca para desatrancar la puerta. Se abre un pasillo al este, terminando en una apertura de luz blanca al fondo.")
        modificar_progreso("final desbloqueado", True)
      else:
        print("No tienes una palanca.")


# Procesar si la orden es válida en el contexto actual
def comprobar_orden_existente(orden):
  # Recoger todas las órdenes válidas en la sala
  ordenes_validas = []
  for i in ordenes_validas_por_sala:
    if i[0] == 0 or i[0] == sala_actual:
      ordenes_validas.extend(i[1])

  if orden in ordenes_validas:
    return True
  else:
    return False


# Recoger órdenes del usuario
def pedir_orden_usuario():
  orden_usuario = input("¿Qué haces ahora? >")

  # Si el juego no entiende el input
  if not validar_sintaxis(orden_usuario):
    print(mensaje_error_sintaxis + "\n")
    pedir_orden_usuario()

  # Si el juego entiende el input, pero no puede procesarlo en el contexto actual
  if not comprobar_orden_existente(orden_usuario):
    print(mensaje_error_orden_no_valida + "\n")
    pedir_orden_usuario()

  print("")
  ejecutar_orden(orden_usuario)


# Si el jugador entra en la sala 0, comprobar si gana o pierde y se guardan sus puntos en la base de datos
def comprobar_victoria():
  global puntos

  if "escudo" in inventario:
    print("La sala está llena de radiación, pero usas el escudo que has robado para pasar sin problemas. Poco a poco te acercas a la luz del fondo, y mientras caminas piensas en lo que has pasado para salir de aquí. Las atrocidades que has cometido. Piensas que quizá no te merezcas ser libre... pero al menos estás vivo, ¿verdad?")
    print("Has ganado. +1000 puntos.")
    puntos = puntos + 1000
  else:
    print("La sala está llena de radiación. Sientes como tu cuerpo se debilita por momentos mientras te acercas a la luz al final del túnel. Empiezas a pensar que quizá el túnel que estás viendo no esté ahí. Y tienes razón. Al alcanzar la luz, te desplomas muerto en el suelo. Estabas tan cerca. En tus últimos alientos rezas para que alguien recuerde tu historia.")
    print("Has perdido...")

  registrar_puntuacion()


# Cambia el estado de una flag al valor pasado como parámetro
def modificar_progreso(flag, valor):
  for i in flags:
    if i[0] == flag:
      i[1] = valor


# Devuelve el estado de una flag pasada como parámetro
def comprobar_progreso(flag):
  for i in flags:
    if i[0] == flag:
      return i[1]


# Presentar estado del jugador
def estado_jugador():
  print("\n{} | Monedas: {} | Puntos: {} | Record: {} | Sala {}".format(nombre_jugador, monedas, puntos, record, sala_actual))


# Aquí solo debe entrar si el usuario introduce una dirección correcta
# Mover al jugador a la nueva sala y procesar los datos pertinentes
def ir_sala(sala_destino):
  global puntos, sala_actual

  if sala_destino == 0:
    if comprobar_progreso("final desbloqueado"):
      comprobar_victoria()
    else:
      print("La puerta está bloqueada. Quizá puedas abrirla con una palanca.")
      return

  sala_actual = sala_destino

  # Mostrar la descripción de la sala actual
  descripcion = ""
  for i in lista_salas:
    if i[0] == sala_actual:
      descripcion = i[1]
  # ...Por si acaso
  if descripcion == "":
    print("Ha habido un error en el procesamiento de la sala. Saliendo...")
    quit()

  print(descripcion)

  # Añadir puntos al descubrir una nueva sala
  if sala_actual not in salas_visitadas:
    print("¡Has descubierto una nueva sala! +100 puntos.")
    puntos = puntos + 100
    salas_visitadas.append(sala_actual)

  # Mostrar los personajes que hay
  for i in lista_personajes:
    if sala_actual == i[0]:
      print("Hay un {} en esta sala.".format(i[1]))

  # Mostrar las posibles salidas
  for i in lista_salidas:
    if i[0] == sala_actual:
      print("Hay una salida hacia el {}.".format(i[1]))


# Empezar una nueva partida desde el principio
def iniciar_partida():
  global nombre_jugador, monedas, puntos, inventario, flags

  nombre_jugador = input("Introduce tu nombre >")
  print("\n¡Bienvenido, {}! Buena suerte.".format(nombre_jugador))
  monedas = 0
  puntos = 0
  inventario.clear()
  for i in flags:
    i[1] = False
  ir_sala(1)


# Cargar todos los datos del juego de la BD
def inicio_cargar_datos_de_bd():
  global record

  # Recoger salas de la BD
  sql = "SELECT * FROM sala"
  cursor.execute(sql)
  for x in cursor:
    lista = [x[0], x[1]]
    lista_salas.append(lista)

  # Recoger salidas de la BD
  sql = "SELECT * FROM salida"
  cursor.execute(sql)
  for x in cursor:
    lista = [x[1], x[2], x[3]]
    lista_salidas.append(lista)

  # Recoger objetos de la BD
  sql = "SELECT * FROM objeto"
  cursor.execute(sql)
  for x in cursor:
    lista = [x[1], x[2]]
    lista_objetos.append(lista)

  # Recoger personajes de la BD
  sql = "SELECT * FROM personaje"
  cursor.execute(sql)
  for x in cursor:
    lista = [x[1], x[2]]
    lista_personajes.append(lista)

  # Recoger record de la BD
  sql = "SELECT * FROM record"
  cursor.execute(sql)
  for x in cursor:
    record = x[1]


def main():
  inicio_cargar_datos_de_bd()
  iniciar_partida()
  while True:
    estado_jugador()
    pedir_orden_usuario()


main()
cursor.close()
connect.close()
