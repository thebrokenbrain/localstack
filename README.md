# LocalStack.

## Requisitos software.
### Docker.
Para instalar Docker serguir la documentación: https://docs.docker.com/engine/install/ubuntu/

### AWS CLI.
Ejemplo de instalación de AWS CLI en Linux:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```
Para instalar AWS CLI en otros sistemas operativos consultar la documentación: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

### AWS SDK para Python (Boto3).
Usaremos Boto3 como SDK (https://aws.amazon.com/es/sdk-for-python/). Instalándolo de la siguiente forma:

```bash
pip install boto3
```

### Librerías adicionales.
La siguiente librería es necesearia para cargar el fichero **```.env```** desde el programa de python.
```bash
pip install python-dotenv
```

## Preparando el entorno para las pruebas.
Lo primero es arrancar el servicio de LocalStack:

```bash
$ make start
Starting LocalStack
docker compose up -d
[+] Running 2/2
 ✔ Network localstack_default  Created                                                                                                                                                                                                                                   0.1s 
 ✔ Container localstack-main   Started       
```
Lo siguiente será modificar las variables de configuración y credenciales de AWS para que aws-cli use las de este repositorio. No sobrescriben a las que puedan existir el directorio "~/.aws" que en donde se suelen almacenar por defecto los credenciales.

```bash
$ source .env
```

Verificar la conexión con LocalStack:

```bash
$ make check
Checking connection to LocalStack
aws --profile=localstack --endpoint-url=http://127.0.0.1:4566 sts get-caller-identity
{
    "UserId": "AKIAIOSFODNN7EXAMPLE",
    "Account": "000000000000",
    "Arn": "arn:aws:iam::000000000000:root"
}
```
Por último, cargar el alias **```aws --profile=localstack --endpoint-url=$LOCALSTACK_ENDPOINT_URL```** que facilitará poder usar el comando **```aws```** de forma simplificada.

```bash
source aws_alias
```
Con el alias cargado ya cargado en lugar de ejecutar, por ejemplo, el siguiente comando para verificar la conexión con la API de AWS de LocalStack:

```bash
$ aws --profile=localstack --endpoint-url=http://127.0.0.1:4566 sts get-caller-identity
```

Podremos ejecutar:

```bash
$ aws sts get-caller-identity
```

## Demo de pruebas "```main.py```"
### Descripción.
Se ha creado un pequeño programa en python que usa la librería Boto3, que es el SDK de AWS para dicho lenguaje.

Se realiza lo siguiente:
- Crear dos buckets.
- Inicializarlo con imágenes.
- Copiar las imágenes de un bucket a otro.
- Eliminar los buckets.

### Ejecución del programa.
Para ejecutar el programa **```main.py```**, después de haber preparado el entorno para las pruebas y que LocalStack se encuentre corriendo correctamente, hay que lanzar:

```bash
make demo
```
![Demo](./assets/demo.gif)

## Comandos.
| **Acción** | **Comando** |
|--------|---------|
| Ayuda | make help |
| Arrancar LocalStack | make start |
| Parar LocalStack | make stop |
| Generar credenciales de AWS para LocalStack | make configure <br> |
| Modificar la ruta de las variables de configuración <br>de AWS a los ficheros de este proyecto (carpeta .aws) | source .env |
| Verificar conexión con LocalStack | make check |
| Muestra el comando a ejecutar para cargar <br>los alias creados a modo de helper | make load-aliases |
| Correr la demo | make demo |


## Referencias.
- https://docs.localstack.cloud/getting-started/installation/
- https://hands-on.cloud/testing-python-aws-applications-using-localstack/#h-installation
- https://docs.aws.amazon.com/sdkref/latest/guide/file-location.html
- https://boto3.amazonaws.com/v1/documentation/api/latest/index.html#

## Stack
- aws-cli
- boto3
- docker
- docker compose
- python3