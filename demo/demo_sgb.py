"""Demostración automática del SGB.

Ejecuta el notebook SGB.ipynb con entradas simuladas (como si alguien escribiera en el menú) y guarda
toda la sesión en demo/demo_sesion.txt. Usa una carpeta temporal con los datos de prueba, así que
NO modifica los archivos reales de SGB/datos/.

Uso (desde la carpeta del proyecto):
    python demo/demo_sgb.py            -> ejecución rápida
    python demo/demo_sgb.py --lento    -> pausas y "tecleo" visible, ideal para grabar la pantalla
"""
import builtins
import json
import os
import sys
import tempfile
import time
from datetime import date, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
NOTEBOOK = os.path.join(AQUI, '..', 'SGB.ipynb')
LOG = os.path.join(AQUI, 'demo_sesion.txt')
LENTO = '--lento' in sys.argv

# Códigos de los datos de prueba (cargar_datos_prueba usa fechas relativas a hoy)
HOY = date.today()
PRESTAMO_VENCIDO_MARIA = f'PRE-{HOY - timedelta(days=12):%Y%m%d}090000007'
MULTA_PENDIENTE_CARLOS = f'MUL-{HOY - timedelta(days=30):%Y%m%d}090000002'

# Guion: los textos que empiezan por '##' son narración (no se escriben en el programa).
GUION = [
    '## PARTE 1. GESTIÓN DE USUARIOS (RF-01)',
    '1',
    '## Listar los usuarios registrados',
    '5',
    '## Registrar un usuario con errores a propósito: el sistema valida cada campo en el momento',
    '1',
    'abc123', '55566677',                # documento: letras -> error, luego válido
    'Pedro 2', 'Pedro Ramírez',          # nombre: número -> error, luego válido
    '7', '1',                            # tipo: opción inexistente -> error, luego 1 = ESTUDIANTE
    'pedro.correo', 'pedro@correo.com',  # correo inválido -> error, luego válido
    '300-12',                            # teléfono con símbolos -> error
    '## Con "<" se vuelve al campo anterior; Enter conserva el valor ya escrito',
    '<', '', '3105556677',
    '## En el resumen se corrige el campo 3 (tipo) escribiendo su número y luego se guarda con "s"',
    '3', '2', '', '', 's',
    '## Consultar el usuario recién creado',
    '2', '55566677',
    '## Con "*" se cancela cualquier operación',
    '4', '55566677', '*',
    '0',

    '## PARTE 2. LIBROS Y CATEGORÍAS (RF-02)',
    '2',
    '## Registrar una categoría (el código debe tener solo letras)',
    '1', 'L1', 'FIL', 'Filosofía', '', 's',
    '## Registrar un libro: ISBN, año y ejemplares se validan; la categoría se elige de una lista',
    '3', '123', '9780140449136', 'Meditaciones', 'Marco Aurelio', '2', '2030', '2006', 'dos', '1', 's',
    '## Buscar por título, listar por categoría y listar disponibles',
    '5', 'cien',
    '6', '4',
    '7',
    '0',

    '## PARTE 3. PRÉSTAMOS (RF-03)',
    '3',
    '5',
    '## Prestar: Carlos tiene una multa pendiente y Laura está suspendida -> el sistema no lo permite',
    '1', '1005556677', '1102223344', '79888777', '9780140449136',
    '## La fecha del préstamo no puede ser futura; Enter = hoy',
    '2099-01-01', '', 's',
    '## Préstamos vencidos a hoy',
    '6', '',
    '## Devolver el préstamo vencido de María: se calcula la multa automáticamente (COP 1.000 por día)',
    '2', 'PRE-123', PRESTAMO_VENCIDO_MARIA, '', 's',
    '4', '1098765432',
    '0',

    '## PARTE 4. RESERVAS, MULTAS E HISTORIAL (RF-04)',
    '4',
    '## Reservar un libro que sí tiene ejemplares -> el sistema indica que se puede prestar directamente',
    '1', '1098765432', '9789585001234', 's',
    '## Reservar un libro sin ejemplares: queda en la cola por orden de llegada',
    '1', '1005556677', '9789588886095', 's',
    '3', '9789588886095',
    '## Consultar y pagar la multa pendiente de Carlos',
    '4', '1005556677',
    '5', MULTA_PENDIENTE_CARLOS, 's',
    '5', MULTA_PENDIENTE_CARLOS, '*',
    '## Historial cronológico de Carlos',
    '6', '1005556677',
    '0',

    '## PARTE 5. ANÁLISIS DE DATOS (RF-05)',
    '5',
    '1', '', '', '5',
    '2', '3', '4', '5',
    '0',
    '0',
]


class Registro:
    """Escribe en pantalla y en el archivo de registro a la vez."""

    def __init__(self, archivo):
        self.archivo = archivo
        self.pantalla = sys.__stdout__

    def write(self, texto):
        self.pantalla.write(texto)
        self.archivo.write(texto)

    def flush(self):
        self.pantalla.flush()
        self.archivo.flush()


def main():
    try:
        sys.__stdout__.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    celdas = [''.join(c['source']) for c in json.load(open(NOTEBOOK, encoding='utf-8'))['cells']
              if c['cell_type'] == 'code']
    pasos = iter(GUION)

    def entrada_simulada(mensaje=''):
        for paso in pasos:
            if paso.startswith('##'):
                print(f'\n{"=" * 78}\n  {paso[2:].strip()}\n{"=" * 78}')
                if LENTO:
                    time.sleep(2.5)
                continue
            print(mensaje, end='', flush=True)
            if LENTO:
                time.sleep(0.6)
                for ch in paso:
                    print(ch, end='', flush=True)
                    time.sleep(0.07)
                print(flush=True)
                time.sleep(0.4)
            else:
                print(paso)
            return paso
        raise SystemExit('\n[Fin del guion de demostración]')

    with open(LOG, 'w', encoding='utf-8') as log:
        sys.stdout = Registro(log)
        carpeta = tempfile.mkdtemp(prefix='sgb_demo_')
        os.chdir(carpeta)           # Celda 0 usa ./SGB/datos/ fuera de Colab -> datos temporales
        print(f'DEMOSTRACIÓN SGB — {HOY}  (datos temporales en {carpeta})\n')
        ns = {'__name__': '__main__'}
        for i, codigo in enumerate(celdas[:-1]):
            exec(compile(codigo, f'celda_{i}', 'exec'), ns)
        builtins.input = entrada_simulada
        ns['limpiar_pantalla'] = lambda: None   # no borrar la salida durante la demo
        try:
            exec(compile(celdas[-1], 'celda_5_1', 'exec'), ns)
        finally:
            sys.stdout = sys.__stdout__
    print(f'\nSesión guardada en {LOG}')


if __name__ == '__main__':
    main()
