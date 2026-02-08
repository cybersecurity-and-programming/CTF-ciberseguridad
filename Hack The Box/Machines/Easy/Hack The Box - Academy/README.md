# Hack The Box - Academy

El análisis comenzó con la inspección del servicio web principal, cuyo comportamiento aparentemente estático ocultaba
funcionalidades adicionales accesibles tras el registro de usuarios. La manipulación de parámetros en el
flujo de alta permitió identificar una deficiencia en el control de privilegios que habilitó el acceso al panel
administrativo, donde se reveló la existencia de un entorno de desarrollo adicional.

La exploración de este subdominio expuso un stack trace propio de Laravel con el modo de depuración
activado, circunstancia que facilitó la obtención de información sensible y permitió inferir la presencia de
una versión antigua del framework vulnerable a problemas históricos de deserialización. El análisis de la
configuración interna, unido a la exposición de variables de entorno, permitió comprender la arquitectura
de la aplicación y localizar credenciales asociadas a servicios internos.

La enumeración del sistema de archivos y la correlación de credenciales condujeron a la identificación de
un usuario local con acceso válido, cuya pertenencia al grupo adm abrió la puerta a la inspección de los
registros del sistema. La revisión del subsistema de auditoría del kernel reveló trazas de actividad TTY que
permitieron reconstruir interacciones previas de otros usuarios, incluyendo credenciales adicionales. Este
hallazgo posibilitó el acceso a una cuenta con permisos delegados en sudo, desde la cual fue posible
identificar un binario legítimo —composer— configurado para ejecutarse con privilegios elevados.

El análisis de este binario, ampliamente documentado en repositorios de referencia por su capacidad para
ejecutar comandos del sistema mediante su mecanismo de scripts, permitió comprender cómo su invocación
bajo sudo constituía un vector de escalada de privilegios. La combinación de estos elementos culminó en
la obtención de un entorno de ejecución con permisos de superusuario y el acceso completo al sistema.

<p align="center">
<img src="assets/1.png" width="700">
</p>
