"""
1. SQL Injection
-----------------
La función consultar_saldo_puntos usa placeholders (?) en lugar de concatenar
strings. Un input como "1 OR 1=1 --" es bloqueado antes de llegar a la base
transaccional de saldos de puntos.
"""

import re
import sqlite3
import logging

logger = logging.getLogger(__name__)


def consultar_saldo_puntos(conn: sqlite3.Connection, usuario_id: str) -> list[dict]:
    """
    Devuelve el saldo de puntos de un usuario del programa Loyalty.
    Usa consulta parametrizada para evitar SQL Injection.
    """
    # Validación previa: el ID solo puede ser alfanumérico (máx. 36 chars / UUID)
    if not re.fullmatch(r"[A-Za-z0-9\-]{1,36}", usuario_id):
        logger.warning("SQL Injection attempt blocked - usuario_id: %r", usuario_id)
        raise ValueError("ID de usuario inválido.")

    # CORRECTO: placeholder - el driver escapa el valor automáticamente
    query = "SELECT usuario_id, puntos_acumulados FROM loyalty_saldos WHERE usuario_id = ?"
    cursor = conn.execute(query, (usuario_id,))
    rows = cursor.fetchall()
    return [{"usuario_id": r[0], "puntos": r[1]} for r in rows]


def _demo_sql():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE loyalty_saldos (usuario_id TEXT, puntos_acumulados INTEGER)")
    conn.execute("INSERT INTO loyalty_saldos VALUES ('USR-001', 4500)")
    conn.commit()

    print("\n--- 1. SQL INJECTION ---------------------------------------")
    # Caso normal
    resultado = consultar_saldo_puntos(conn, "USR-001")
    print(f"  [OK]  Saldo para USR-001: {resultado}")

    # Intento de inyección
    try:
        consultar_saldo_puntos(conn, "1 OR 1=1 --")
    except ValueError as e:
        print(f"  [BLOQUEADO]  {e}")


if __name__ == "__main__":
    _demo_sql()
