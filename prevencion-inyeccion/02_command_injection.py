"""
2. Command Injection
---------------------
generar_reporte_pais valida contra una lista blanca (PAISES_PERMITIDOS).
El payload "Argentina; rm -rf /" es rechazado sin que el string llegue nunca
a un shell.
"""

import logging

logger = logging.getLogger(__name__)

PAISES_PERMITIDOS = {"Argentina", "Brasil", "Chile", "Colombia", "México", "Uruguay"}


def generar_reporte_pais(pais: str) -> str:
    """
    Simula la generación de un reporte de lealtad por país.
    Valida el parámetro contra una lista blanca antes de usarlo.
    """
    pais = pais.strip()
    if pais not in PAISES_PERMITIDOS:
        logger.warning("Command Injection / invalid input blocked - pais: %r", pais)
        raise ValueError(f"País no permitido: {pais!r}. Valores válidos: {PAISES_PERMITIDOS}")

    # CORRECTO: el valor ya está validado; nunca se pasa a shell=True
    # subprocess.run(["generar_reporte", pais], check=True)  <- uso seguro
    return f"[SIMULADO] Reporte Loyalty generado para: {pais}"


def _demo_command():
    print("\n--- 2. COMMAND INJECTION -----------------------------------")
    print("  [OK]      ", generar_reporte_pais("Argentina"))
    try:
        generar_reporte_pais("Argentina; rm -rf /")
    except ValueError as e:
        print(f"  [BLOQUEADO]  {e}")


if __name__ == "__main__":
    _demo_command()
