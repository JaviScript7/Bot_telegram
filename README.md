# 🤖 Bot para Reparación de Celulares 📱

## Descripción

**Mobile Repair Bot** es un bot desarrollado en Python para Telegram, diseñado para asistir a personas que reparan celulares. Este bot facilita el registro y la consulta de equipos por medio de folios, así como se contempla añadir las funciones para la gestión de inventarios, ganancias y estadísticas.

## Funcionalidades

- 📋 **Registro de Equipos:** Permite registrar cada equipo de reparación con su respectivo folio  -> ✅
- 🔍 **Consulta por Folio:** Busca y muestra información de los equipos mediante un folio  -> ✅
- 📦 **Gestión de Inventarios:** Administra el inventario de piezas y herramientas ->🚧 EN PROCESO 🚧
- 💰 **Dinero Ganado:** Lleva un registro de las ganancias obtenidas -> 🚧 EN PROCESO 🚧
- 📊 **Estadísticas:** Proporciona estadísticas sobre el rendimiento del taller -> ✅

 ## <img src="https://skillicons.dev/icons?i=docker" width="30" height="30"  /> Despegar Bot con Docker

 ### 🏗️ Vamos a construir el contenedor

 ### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/JaviScript7/Bot_telegram.git
```

### Paso 2: Navegar al directorio del proyecto
```bash
cd Bot_telegram
```
### Paso 3: Crear el archivo .env y colocar el token de tu bot sin " "
```bash
API_TOKEN= --- TU TOKEN ---
```
### Paso 4: Ejecutar el contenedor Docker
```bash
docker-compose -f docker-compose.yml up -d --build 
```
### Paso 5: Verificar que los contenedores esten corriendo
```bash
docker ps 
```
### Paso 6: Verificar los logs 
```bash
docker logs <nombre del contenedor> 
```
### Paso 7: Para detener 
```bash
docker-compose -f docker-compose.yml down 
```

## Licencia ⚖️
Este proyecto está bajo la [Licencia Apache 2.0](LICENSE)


