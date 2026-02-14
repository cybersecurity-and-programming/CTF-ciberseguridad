# Hack The Box - APT

Este informe documenta de manera estructurada el proceso completo de análisis, explotación y post explotación de la máquina APT, abordando tanto la superficie de ataque inicial como las técnicas avanzadas empleadas 
para obtener control total del dominio. El objetivo principal es mostrar un flujo de trabajo realista, fundamentado en la comprensión profunda de los protocolos subyacentes —Kerberos, NTLM, DCE/RPC y Active Directory— 
y en la aplicación de metodologías ofensivas reproducibles.

La intrusión se inicia con la enumeración remota de servicios RPC y la obtención de network bindings mediante el método ServerAlive2, lo que permite descubrir interfaces expuestas únicamente en IPv6.
A partir de esta información, se realiza un análisis exhaustivo de servicios críticos como SMB, Kerberos y WinRM, identificando configuraciones débiles y recursos sensibles, entre ellos un volcado de NTDS.dit 
acompañado de los hives de registro necesarios para descifrar credenciales.

El informe detalla el uso combinado de herramientas como Impacket, Kerbrute, Responder, evil winrm y Seatbelt, así como técnicas de password spraying, forced authentication y explotación de NTLMv1. 
Además, se incluye una aportación propia desarrollada durante la investigación: una implementación alternativa basada exclusivamente en Impacket para automatizar parte del proceso de enumeración y validación de credenciales, 
demostrando la viabilidad de enfoques más directos y controlados que las herramientas tradicionales.

La explotación culmina con la obtención de privilegios de Domain Administrator mediante un ataque DCSync, validando la cadena completa de compromiso y evidenciando el impacto real de las debilidades identificadas. 
El resultado es un recorrido técnico completo que combina investigación, análisis protocolar, scripting personalizado y técnicas avanzadas de post explotación, ofreciendo una visión integral del compromiso de un
entorno Active Directory.

<p align="center">
<img src="assets/1.png" width="700">
</p>
