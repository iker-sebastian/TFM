import jwt

#---------------------------------------- GENERAR TOKEN EUSKALMET ----------------------------------------#

# Definir rutas claves
ruta_private_key = 'API_Euskalmet_2024/privateKey.pem'
ruta_public_key = 'API_Euskalmet_2024/publicKey.pem'

# Lectura de las claves
with open(ruta_private_key, 'rb') as private_key_file:
    clave_privada = private_key_file.read()
with open(ruta_public_key, 'rb') as public_key_file:
    clave_publica = public_key_file.read()

# Definicion del payload
payload = {
    'aud': 'met01.apikey',
    'iss': 'TFM',
    'exp': 1731202255,
    'version': '1.0.0',
    'iat': 	1712781055,
    'email': 'iker.sebastian@opendeusto.es'
}

# Generacion de token JWT
token_jwt = jwt.encode(payload, clave_privada, algorithm='RS256')

# Header para el token
headers = {'Authorization': f'Bearer {token_jwt}'}
#print(headers)
