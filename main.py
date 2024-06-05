import time 
from jwt_handler import encodeJWT, decodeJWT, refreshJWT

user = {"email":"tlbkvs@gmail.com", "username":"katana", "id":1}

#получаем токины
jwt_token = encodeJWT(user) # {'access':adkfadks, 'refresh':dfjj9jdfij}
print(jwt_token)

#проходит время
time.sleep(6)

#прилетает декодированный токен, если время не истекло, если время жизни токена истекло прилетает пустой dict
decoded = decodeJWT(jwt_token['access'])
print(decoded)

#обновляем старые токены, на новые
new_jwt_token = refreshJWT(jwt_token['refresh'])
print(new_jwt_token)

