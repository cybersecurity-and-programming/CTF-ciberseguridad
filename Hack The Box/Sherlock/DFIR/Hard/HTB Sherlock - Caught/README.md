# HTB Sherlock - Caught

Este análisis forense reconstruye, paso a paso, la cadena completa de compromiso sufrida por el dominio
MEGACORP, desde la intrusión inicial hasta la obtención de privilegios de administrador local y la
instalación de un mecanismo de persistencia basado en WMI. A lo largo de la investigación se correlacionan
múltiples fuentes de evidencia —artefactos de Mimikatz, relaciones de privilegios en Active Directory
extraídas mediante BloodHound, registros del controlador de dominio, el repositorio WMI y la base de
datos ntds.dit— con el objetivo de identificar las acciones del atacante, los vectores de escalada y los
objetos manipulados para mantener acceso persistente.
El proceso revela un compromiso metódico: primero, la explotación de una estación de trabajo que permitió
la ejecución de Mimikatz con privilegios elevados; después, el abuso de delegaciones mal configuradas en
Active Directory que facilitaron movimientos laterales y escaladas de privilegios; y finalmente, la
implantación de un mecanismo de persistencia mediante un objeto WMI malicioso que ejecutaba código
remoto a través de mshta. Cada fase del ataque se documenta con precisión, destacando tanto las técnicas
empleadas por el adversario como las debilidades estructurales que hicieron posible su avance.

<p align="center">
<img src="assets/1.png" width="700">
</p>
