# EjercicioPractico1-TestingYCodificación

Análisis de Ventajas:
En este proyecto se aplicó una estrategia de pruebas Top-Down para validar primero el caso de uso completo de “prestar libro” y, a partir de ahí, ir cubriendo las dependencias con stubs. Se inyecto AuthStub y DatabaseStub para simular autenticación, disponibilidad y registro sin necesidad de una base de datos real ni de un servicio externo. Esto permitió obtener retroalimentación inmediata sobre las reglas de negocio y asegurar el flujo correcto (autorización → disponibilidad → registro) desde el primer día. Al trabajar con stubs, los tests fueron muy rápidos y deterministas, lo que aceleró las iteraciones y evitó intermitencias típicas de I/O o red. Además, el enfoque ayudó a definir contratos claros entre la lógica de la biblioteca y sus colaboradores, reduciendo el acoplamiento y facilitando futuros cambios. Se pudo cubrir escenarios difíciles de reproducir en producción, como errores al registrar un préstamo, usuarios bloqueados o libros no disponibles, y verificar que el sistema respondiera con los mensajes esperados. El diagnóstico de fallos fue más simple porque cualquier desviación quedaba acotada a la orquestación y las reglas, no a la infraestructura. En paralelo, esta estrategia permitió que la implementación real de la base de datos o de notificaciones avanzara sin bloquear las pruebas funcionales. Finalmente, los tests actuaron como documentación ejecutable del comportamiento esperado.

Testing de top_down.py

<img width="1212" height="304" alt="Captura de pantalla 2025-09-24 194356" src="https://github.com/user-attachments/assets/3adcb779-04f6-407b-926f-ea03ecb8e5d4" />


Testing de Stubs con venv (virtual.env) 

<img width="1214" height="146" alt="Captura de pantalla 2025-09-24 194516" src="https://github.com/user-attachments/assets/0ee7d482-ec62-45ca-9482-e67589149ae8" />

