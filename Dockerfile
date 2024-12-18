#Esto es un dockerfile para entorno de desarrollo y pruebas 

#Elegimos la imagen base y especificamos la version
FROM python:3.12

#Indicamos quien es el responsable de mantener el contenedor
LABEL Maintainer="JaviScript"

#Creamos el directorio de la aplicacion
RUN mkdir -p /home/app

#Instalacion de paquetes necesarios para trabajar en nuestro entorno
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    nano \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

#Modificar el bash -> Esto es por gusto personal
RUN rm /root/.bashrc
COPY .bashrc /root

#Copiar los archivos de la aplicacion
COPY . /home/app

#Establecemos el espacio de trabajo 
WORKDIR /home/app

#Instalar las dependencias
RUN pip install  --no-cache-dir -r /home/app/requirements.txt

#Establemos lo que hara al iniciar el contenedor
CMD [ "python","src/bot_main.py" ]

