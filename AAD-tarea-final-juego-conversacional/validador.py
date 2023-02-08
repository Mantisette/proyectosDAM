# Validador v2

# Palabras válidas
comandos = ["inventario", "nuevo", "guardar", "cargar", "mapa", "ayuda", "si", "no"]
verbos = ["dar", "abrir", "cerrar", "coger", "hablar", "mirar", "usar", "empujar", "tirar"]
verbos_tienda = ["comprar", "vender"]
verbos_ir = ["ir"]
ir_direcciones = ["norte", "sur", "este", "oeste"]
conjunciones = ["a", "con"]
objetos = ["llave", "cofre", "candelabro", "cuchillo", "monedas", "escudo", "mesa", "palanca", "cuadro"]
personajes = ["guerrero", "tendero"]

# Tokens
token_comandos = 0
token_verbos = 1
token_verbos_tienda = 11
token_verbos_ir = 12
token_ir_direcciones = 13
token_conjunciones = 14
token_objetos = 2
token_personajes = 3

# Mapa de tokens y sus listas de palabras aceptadas
lista_tokens = [
  [comandos, token_comandos],
  [verbos, token_verbos],
  [verbos_tienda, token_verbos_tienda],
  [verbos_ir, token_verbos_ir],
  [ir_direcciones, token_ir_direcciones],
  [conjunciones, token_conjunciones],
  [objetos, token_objetos],
  [personajes, token_personajes]
]

# Reglas contextuales
regla_inicio_frase = [
  token_verbos, token_verbos_tienda, token_verbos_ir
]
regla_final_frase = [
  token_ir_direcciones, token_objetos, token_personajes
]

# Mapa de reglas y sus listas de palabras aceptadas 
lista_reglas = [
  [
    token_verbos,
    [token_conjunciones, token_objetos, token_personajes]
  ],
  [
    token_verbos_tienda,
    [token_objetos]
  ],
  [
    token_verbos_ir,
    [token_ir_direcciones]
  ],
  [
    token_ir_direcciones,
    [-1]  # No debería haber nada detrás de las conjunciones
  ],
  [
    token_conjunciones,
    [token_objetos, token_personajes]
  ],
  [
    token_objetos,
    [token_conjunciones]
  ],
  [
    token_personajes,
    [token_conjunciones]
  ],
]


# Tokenizacion de la frase. Devuelve una lista con los tokens correspondientes, o vacía si falla la tokenización
def tokenizar(frase):
  # Tratar el input del usuario
  frase = frase.split(" ")

  # Convertir cada palabra a tokens que el script entienda
  tokens_input_usuario = []
  for palabra in frase:  # Cada palabra que introduce el usuario
    for categoria_lista_tokens in lista_tokens:  # Cada sublista de la lista de tokens
      for palabra_valida in categoria_lista_tokens[0]:  # Cada palabra recogida en la sublista asignada a ese token
        if palabra == palabra_valida:
          tokens_input_usuario.append(categoria_lista_tokens[1])

  if len(tokens_input_usuario) != len(frase):  # Si ha fallado alguna tokenización
    tokens_input_usuario = []

  return tokens_input_usuario


# Comprobación sintáctica. Devuelve un boolean indicando si la sintaxis se adecúa a las reglas definidas al principio
def comprobar_sintaxis(tokens_input_usuario):
  # Si la lista de tokens está vacía, la validación no es posible
  if len(tokens_input_usuario) < 1:
    return False

  inicial = tokens_input_usuario[0]
  final = tokens_input_usuario[len(tokens_input_usuario) - 1]

  # Los comandos solo se ejecutan si son la única palabra de la frase
  if inicial == 0:
    if len(tokens_input_usuario) > 1:
      return False
    else:
      return True

  # Las frases solo pueden empezar con verbos.
  if inicial not in regla_inicio_frase:
    return False

  for idx, token in enumerate(tokens_input_usuario[:-1]):  # Recorrer todos los tokens de la función anterior
    siguiente = tokens_input_usuario[idx + 1]  # El siguiente token para comparar
    for regla in lista_reglas:  # Recorrer todas las reglas relevantes a este contexto
      if token == regla[0]:  # Encontrar las reglas que sigue este token
        if siguiente not in regla[1]:  # Comparar si el token sigue dichas reglas
          return False

  # Las frases solo pueden acabar con direcciones, objetos o personajes.
  if final not in regla_final_frase:
    return False

  # Si el código llega hasta aquí, los tokens han pasado todos los controles
  return True


def validar_sintaxis(input_usuario):
  return(comprobar_sintaxis(tokenizar(input_usuario)))
