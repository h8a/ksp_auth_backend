# ksp_auth_backend

## Ejecutar servicio employees con autentificacion

Ejecutar docker compose

```bash
docker compose up -d
```
Revisar logs

```bash
docker compose logs -f
```

## Endpoints

Crear user:
```bash
curl --location 'localhost:80/api/v1.0.0/auth/register' \
--header 'Content-Type: application/json' \
--data '{
    "username": "user2",
    "password": "12345678"
}'
```

Logear usuario
```bash
curl --location 'localhost:80/api/v1.0.0/auth/login' \
--header 'Content-Type: application/json' \
--data '{
    "username": "user2",
    "password": "12345678"
}'
```
Obtendra una respuesta como la siguiente:
```bash
{
    "status": true,
    "data": {
        "username": "user2",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0OWE0YjZkLWQyNTAtNDNkMC1iODBjLTA4NzAzYjdmNTUxYSIsImV4cCI6MTY4MDAxMzgxN30.5Az43392ItvX58CkojQbL7B_Ca6Mp7tkaR7vQVHoEVU"
    }
}
```

Ahora para tener acceso a los endpoints del servicio employees utilizar el token de la siguiente forma:
```bash
curl --location 'localhost:80/api/v1.0.0/employees' \
--header 'Authorization: ksp eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0OWE0YjZkLWQyNTAtNDNkMC1iODBjLTA4NzAzYjdmNTUxYSIsImV4cCI6MTY4MDAxMzgxN30.5Az43392ItvX58CkojQbL7B_Ca6Mp7tkaR7vQVHoEVU'
```

Obtendra una respuesta similar a usar al servicio con normalidad y sin autentificacion aunque en esta ocasion si valida el token:
```bash
{
    "status": true,
    "data": []
}
```

Para validar que la cabecera si esta siendo validada, puede probar hacer la consulta sin la cabecera Authorization:
```bash
curl --location 'localhost:80/api/v1.0.0/employees'
```

Obtendra una respuesta como la siguiente:
```bash
{
    "status": false,
    "message": "Bad authorization header"
}
```
