#  Hack The Box - Caption

El objetivo del ejercicio fue evaluar la seguridad de una arquitectura web multicapa que integra un proxy
inverso (HAProxy), un acelerador de caché (Varnish) y varios servicios internos expuestos únicamente a
nivel local. A lo largo del proceso se emplearon técnicas avanzadas de enumeración, manipulación de
encabezados, HTTP/2 cleartext smuggling, análisis de repositorios, explotación de vulnerabilidades en
servicios internos y desarrollo de herramientas personalizadas para interactuar con componentes no
documentados.
La intrusión se articuló en torno a una cadena de fallos que combinaba filtraciones de credenciales en el
historial de commits, configuraciones laxas en la negociación de protocolos, un servicio interno vulnerable
a path traversal y un componente RPC escrito en Go que carecía de validaciones adecuadas. La explotación
coordinada de estos elementos permitió atravesar las distintas capas defensivas, obtener acceso inicial
mediante SSH y, finalmente, escalar privilegios hasta comprometer por completo el sistema.
