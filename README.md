# SGB — Sistema de Gestión Bibliotecaria

Trabajo Final de Semestre · **Programación Orientada a Objetos — Ingeniería de Software**.
Software en Python (Google Colab) para gestionar una biblioteca: usuarios, libros y categorías, préstamos y devoluciones, reservas, multas, historial de usuario y análisis de datos.

## Integrantes

- Carlos Santiago Merchan Centeno
- Daniel Fernando Vesga Tarazona

## Archivos del proyecto

| Archivo | Contenido |
|---------|-----------|
| `SGB.ipynb` | Notebook de Google Colab con todo el sistema |
| `SGB/datos/*.txt` | Datos de prueba (usuarios, categorías, libros, préstamos, multas, reservas) |
| `SGB_Diagramas_UML.pdf` | Diagramas UML: dominio, dominio parcial, clases, objetos, estructurados y secuencia |

## Tecnologías

- Python 3.10 o superior, solo librería estándar (`os`, `datetime`, `collections`)
- Google Colab + Google Drive (también corre localmente en VS Code/Jupyter)
- Persistencia en archivos `.txt` con campos delimitados por `|`; los campos vacíos se guardan como `NINGUNO`

## Arquitectura (3 capas, implementada solo con funciones)

El sistema **no usa clases ni objetos**: cada entidad es un diccionario y cada "clase" del diseño es un grupo de funciones con un prefijo común.

| Capa | Sección del notebook | Funciones |
|------|----------------------|-----------|
| Modelo (dominio) | 1 | Enums (`TIPO_USUARIO_ENUM`, `ESTADO_PRESTAMO_ENUM`…) y `crear_*`, `*_to_linea`, `*_from_linea` |
| Repositorios (persistencia) | 2 | ArchivoUtil (`leer_lineas`, `escribir_linea`, `reescribir`, `generar_codigo`) y `repo_<entidad>_*` |
| Servicios (lógica) | 3 | `usuario_*`, `libro_*`, `prestamo_*`, `multa_*`, `reserva_*`, `analisis_*` |
| Interfaz | 4 | `menu_principal`, `menu_usuarios`, `menu_libros`, `menu_prestamos`, `menu_reservas_multas`, `menu_analisis` |

## Reglas de negocio

| Tipo de usuario | Plazo de préstamo | Cupo de libros |
|-----------------|-------------------|----------------|
| Estudiante | 7 días | 3 |
| Docente | 15 días | 5 |
| Externo | 5 días | 2 |

- Solo pueden pedir prestado usuarios **activos**, sin multas pendientes y dentro de su cupo.
- Multa por retraso: **COP 1.000 por cada día**, calculada automáticamente al devolver.
- Solo se reserva un libro sin ejemplares libres; las reservas se atienden por orden de llegada.

## Cómo ejecutar en Colab

1. Crear la carpeta `SGB/datos/` en *Mi unidad* de Google Drive y subir allí los `.txt` de `SGB/datos/` (opcional: si la carpeta está vacía, el notebook carga datos de prueba automáticamente).
2. Abrir `SGB.ipynb` en Colab y ejecutar *Entorno de ejecución → Ejecutar todo* (autorizar el acceso a Drive).
3. La celda 5.0 corre las pruebas de integración en una carpeta temporal; la celda 5.1 abre el menú principal.
