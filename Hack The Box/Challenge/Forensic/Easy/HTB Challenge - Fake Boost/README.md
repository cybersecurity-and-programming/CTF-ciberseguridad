# HTB Challenge - Fake Boost

El presente análisis documenta el proceso de desarticulación de un flujo de compromiso simulado en el reto
Fake Boost de HackTheBox, articulado en torno a la inspección forense de un volcado de tráfico y la
posterior reconstrucción de un artefacto malicioso distribuido mediante PowerShell. A partir de la
correlación entre distintos TCP streams, se identificó la transferencia de un script ofuscado cuya
descomposición reveló tanto la primera porción de la flag como los parámetros criptográficos empleados
por el servidor atacante. El estudio detallado del código permitió inferir el uso de cifrado simétrico AES
con clave e IV embebidos, lo que habilitó el descifrado del tráfico exfiltrado localizado en un flujo posterior
y la recuperación de la segunda parte de la flag. Finalmente, la elaboración de un script en Python permitió
automatizar el proceso de descifrado y consolidar la evidencia, completando así la resolución íntegra del
desafío mediante una aproximación rigurosa, reproducible y fundamentada en técnicas de análisis de tráfico,
desofuscación y criptoanálisis aplicado.

<p align="center">
<img src="assets/1.png" width="700">
</p>
