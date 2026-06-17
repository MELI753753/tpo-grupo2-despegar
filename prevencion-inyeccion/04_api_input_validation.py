"""
4. API Input Validation
------------------------
validar_solicitud_canje (el endpoint POST /loyalty/canje) verifica tipo, rango
y lista exacta de campos. Rechaza puntos negativos, campos extra como
admin_override (mass-assignment) y user IDs con SQL embebido.
"""

import re
import logging
from typing import Any

logger = logging.getLogger(__name__)

TIPOS_CANJE_VALIDOS = {"descuento_vuelo", "upgrade_hotel", "voucher_extra"}


def validar_solicitud_canje(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Valida el payload recibido en el endpoint POST /loyalty/canje.
    Retorna el payload limpio o lanza ValueError con el motivo.
    """
    errores = []

    # Campo: usuario_id
    uid = payload.get("usuario_id", "")
    if not re.fullmatch(r"[A-Za-z0-9\-]{1,36}", str(uid)):
        errores.append("usuario_id inválido.")

    # Campo: puntos_a_canjear
    puntos = payload.get("puntos_a_canjear")
    if not isinstance(puntos, int) or not (1 <= puntos <= 500_000):
        errores.append("puntos_a_canjear debe ser un entero entre 1 y 500.000.")

    # Campo: tipo_canje
    tipo = payload.get("tipo_canje", "")
    if tipo not in TIPOS_CANJE_VALIDOS:
        errores.append(f"tipo_canje debe ser uno de {TIPOS_CANJE_VALIDOS}.")

    # Campos extra no permitidos (evita mass-assignment / parameter pollution)
    campos_permitidos = {"usuario_id", "puntos_a_canjear", "tipo_canje"}
    campos_extra = set(payload.keys()) - campos_permitidos
    if campos_extra:
        errores.append(f"Campos no permitidos: {campos_extra}.")

    if errores:
        logger.warning("API validation failed - payload: %r | errores: %s", payload, errores)
        raise ValueError("Payload inválido: " + " | ".join(errores))

    return {k: payload[k] for k in campos_permitidos}


def _demo_api():
    print("\n--- 4. API INPUT VALIDATION (endpoint de canje) ------------")
    casos = [
        # Caso válido
        {"usuario_id": "USR-001", "puntos_a_canjear": 1000, "tipo_canje": "descuento_vuelo"},
        # Puntos negativos
        {"usuario_id": "USR-001", "puntos_a_canjear": -9999, "tipo_canje": "descuento_vuelo"},
        # Campo extra (mass-assignment)
        {"usuario_id": "USR-001", "puntos_a_canjear": 500, "tipo_canje": "upgrade_hotel",
         "admin_override": True},
        # SQL en usuario_id
        {"usuario_id": "' OR '1'='1", "puntos_a_canjear": 100, "tipo_canje": "voucher_extra"},
    ]
    for payload in casos:
        try:
            limpio = validar_solicitud_canje(payload)
            print(f"  [OK]        Payload aceptado: {limpio}")
        except ValueError as e:
            print(f"  [BLOQUEADO]  {e}")


if __name__ == "__main__":
    _demo_api()
