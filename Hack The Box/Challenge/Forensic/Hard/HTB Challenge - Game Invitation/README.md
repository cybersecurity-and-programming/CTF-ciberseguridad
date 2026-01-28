# HTB Challenge - Game Invitation

El presente análisis documenta de manera exhaustiva el proceso de desarticulación técnica del desafío Game Invitation de Hack The Box, centrado en la disección de un documento ofimático malicioso 
y en la reconstrucción completa de su cadena de infección. A lo largo del estudio se examinan las macros incrustadas en el fichero inicial, se identifican los mecanismos de ofuscación empleados por 
el atacante y se detalla la extracción, descifrado y posterior interpretación del payload embebido. El análisis combina técnicas de ingeniería inversa, revisión criptográfica y desarrollo de herramientas 
defensivas propias, con el objetivo de comprender no solo el comportamiento observable del artefacto, sino también la lógica operativa que articula su ejecución condicionada y su comunicación con la infraestructura 
de mando y control.

Este write up pretende reflejar un enfoque metodológico riguroso, propio de un analista de seguridad que aborda cada fase del proceso con precisión terminológica, criterio técnico y una clara orientación 
a la reproducibilidad. La inclusión de un script de análisis desarrollado ad hoc permite ilustrar cómo la automatización y la ingeniería defensiva pueden complementar el estudio manual, reforzando 
la capacidad de detectar, interpretar y neutralizar amenazas similares en entornos reales. El resultado es una visión integral del ataque, desde la macro inicial hasta el beacon C2 final, que evidencia 
la importancia de comprender en profundidad tanto las técnicas ofensivas como las defensivas en el ámbito de la ciberseguridad contemporánea.

<p align="center">
<img src="assets/2.png" width="700">
</p>
