"""
Demo conjunta — Prevención de ataques por inyección de código
Caso Despegar · Programa de fidelización (Comarch Loyalty Management)
TPO Ingeniería de Software · Grupo 2

Ejecuta las cuatro defensas:
  1. SQL Injection
  2. Command Injection
  3. XSS
  4. API Input Validation
"""

import importlib.util
import pathlib

BASE = pathlib.Path(__file__).parent


def _cargar(nombre_archivo, nombre_funcion):
    ruta = BASE / nombre_archivo
    spec = importlib.util.spec_from_file_location(ruta.stem, ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    getattr(modulo, nombre_funcion)()


if __name__ == "__main__":
    print("=" * 60)
    print(" PREVENCIÓN DE INYECCIÓN DE CÓDIGO - DESPEGAR LOYALTY")
    print("=" * 60)
    _cargar("01_sql_injection.py", "_demo_sql")
    _cargar("02_command_injection.py", "_demo_command")
    _cargar("03_xss.py", "_demo_xss")
    _cargar("04_api_input_validation.py", "_demo_api")
    print("\n" + "=" * 60)
