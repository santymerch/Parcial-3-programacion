# SGB — Sistema de Gestión de Biblioteca

Proyecto del curso de **Programación Orientada a Objetos (POO)**.
Software en Python para la gestión de una biblioteca: usuarios, libros y categorías, préstamos y devoluciones, reservas, multas, historial de usuario y análisis de datos.

## Integrantes

- Carlos Santiago Merchan Centeno
- Daniel Fernando Vesga Tarazona

## Descripción

Sistema de información que centraliza el ciclo completo de préstamo y devolución de una biblioteca, reemplazando fichas de papel y hojas de cálculo dispersas, y generando indicadores estadísticos de uso de la colección.

## Tecnologías

- Python 3.10 o superior (solo librería estándar)
- Jupyter Notebook (VS Code o Jupyter)
- Persistencia en archivos `.txt` con campos delimitados por `|`

## Arquitectura (3 capas)

| Capa | Contenido |
|------|-----------|
| Modelo (dominio) | `Usuario`, `Categoria`, `Libro`, `Prestamo`, `Multa`, `Reserva` y enums |
| Repositorios (persistencia) | `ArchivoUtil`, `UsuarioRepository`, `CategoriaRepository`, `LibroRepository`, `PrestamoRepository`, `MultaRepository`, `ReservaRepository` |
| Servicios (lógica) | `UsuarioService`, `LibroService`, `PrestamoService`, `MultaService`, `ReservaService`, `AnalisisDatosService` |

La interfaz de usuario se implementa con menús `print()` / `input()` dentro de celdas del notebook.

## Estructura del notebook (`SGB_Biblioteca.ipynb`)

- **Celda 0** — Configuración: carpeta local `datos/` y constantes
- **Sección 1** — Modelo (dominio)
- **Sección 2** — Repositorios
- **Sección 3** — Servicios
- **Sección 4** — Interfaz de usuario
- **Sección 5** — Ejecución principal

## Reglas de negocio

| Tipo de usuario | Plazo de préstamo | Cupo de libros |
|-----------------|-------------------|----------------|
| Estudiante | 7 días | 3 |
| Docente | 15 días | 5 |
| Externo | 5 días | 2 |

- Solo pueden pedir prestado usuarios **activos**, sin multas pendientes y dentro de su cupo.
- Multa por retraso: **COP 1.000 por cada día**.
- Las reservas se atienden por orden de llegada.

## Cómo ejecutar

1. Abrir `SGB_Biblioteca.ipynb` en VS Code o Jupyter.
2. Ejecutar las celdas en orden. Los datos se guardan en la carpeta `datos/` (se crea sola).
3. La última celda abre el menú.

## Estado del proyecto

- [x] Commit 1 — Configuración y capa de Modelo
- [ ] Commit 2 — Repositorios
- [ ] Commit 3 — Servicios
- [ ] Commit 4 — Interfaz de usuario y ejecución principal
