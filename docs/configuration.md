#Configuración del entorno de trabajo
En primer lugar, he descargado git para Mac desde la línea de comandos. Una vez instalado, he añadido mi nombre y correo electrónico.

##Creación de un par de claves SSH
Utilizo el siguiente comando para crear el par de claves pública y privada de SSH:
![captura1](img/c1.png)

A continuación copio la clave pública
![captura2](img/c2.png)

Añado mi clave pública a GitHub (Settings > SSH and GPG keys > New SSH Key)
![captura3](img/c3.png)

##Configuración de Git
Configuro mi nombre y correo electrónico para que aparezca en los commits. 

	git config --global user.name "Cristina del Aguila" 
	git config --global user.email "cristinadam@correo.ugr.es"
