# Trabajo de Fin de Grado de Matemáticas, en Criptografía.

En el cual analizo un esquema de cifrado simétrico basado en cuasigrupos. Como apoyo, he desarrollado unas utilidades en código Python.

## cripto_cuasigrupos.py

Se encuentra la funcionalidad para calcular las tablas de los cuasigrupos y operar con los principales cifrados que se estudian y/o proponen a lo largo del trabajo.

## quasi_group_descriptions.txt

Archivo de texto en el cual se pueden introducir distintos cuasigrupos o cuerpos y generar sus tablas de operación, asi como operar con los cifrados que se van operar con los principales cifrados que se van estudiando y/o proponiendo a lo largo del trabajo.
La descripcion consta de lo siguiente:
- La primera linea tiene 3 elementos: QG ó F (segun sea Cuasigrupo o Cuerpo), Nombre y N, el número de elementos; todo separado por espacios
- La segunda linea: el nombre de los elementos de la estructura, separados por comas
- Las siguientes N lineas constan de la tabla de operación del cuasigrupo (o la operacion suma del cuerpo)
- En el caso de estar describiendo un cuerpo, hay N lineas mas indicando la operación producto del cuerpo.

## probabilidad.py

Sencillo algoritmo voraz para calcular la probabilidad que tiene que un atacante IND-CPA o IND-CCA para superar los retos de indistinguibilidad en un entorno de realeatorización de algoritmos de cifrado deterministas.
