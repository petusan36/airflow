# Airflow
Base airflow

Estructura sugerida para el arbol de directorios que se cargaran automáticamente en los volumenes del archivo ecosystem.yaml:

``` cmd
|
| - config  -> contiene los archivos de configuración para Airflow.
| - dags    -> Acá estarán los dags.
| - logs    -> En esta carpeta guerdará los logs al momento de ejecución de las máquinas (este irá creciendo y es bueno ir limpiando si no se requiere para seguimientos).
| - plugins -> los plugins que se vayan adicionando al entorno de Airflow
| - secrets -> En esta carpeta se guardarán las llaves necesarias para conexiones con BD o Clouds.
```
Archivos que contiene el proyecto necesarios para su funcionamiento:

``` cmd
|
| - .env              -> Variables de ambiente usadas por Airflow.
| - Dockerfile        -> Contiene las instrucciones para la creación de la imagen de Airflow y lee el archivo de requirements.txt para satisfacer libreriás adicionales.
| - ecosystem.yaml    -> Archivo para la creación de las máquinas usadas para que funcione Airflow, en este se deberán modificar según las necesidades.
                         en image: ${AIRFLOW_IMAGE_NAME:-airflowpts} cambiar airflowpts por el nombre de la imagen asignada cuando se hace el build del Dockerfile
| - requirements.txt  -> En este archivo se adicionan todas las librerías adicionales para ser cargadas al momento de creación de la imagen.
```
Ejemplo de estructura completa de un proyecto:
``` cmd
|
| - config
| - dags
  | - dag1.py
  | - dag2.py
  .
  .
| - logs
  | - Schedule
  .
  .
| - plugins
| - secrets
  | - GCP
    | - key.json
  | - AWS
    | - key.txt
  | - AZ
  | - Postrgres
  .
  .
| - .env
| - Dockerfile
| - ecosystem.yaml
| - requirements.txt
```

Para la creación de la image se está usando docker y la instrucción es la siguiente:
```nginx
docker build -t <nombre para la imagen> .
```
El archivo `Dockerfile` debe estar presente en la carpeta donde se ejecuta el comando `build`.

para la ejecución del ambiente completo se debe ejecutar el siguiente comando ( ` -d ` es para que se ejecute en modo desatendido)
```nginx
 docker compose -f ecosystem.yaml up -d
```

Para detener los contenedores se debe ejecutar el comando
```nginx
 docker compose -f ecosystem.yaml down
```
