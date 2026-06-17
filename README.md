# TPO Ingeniería de Software — Grupo 2

Caso **Despegar.com** — Programa de fidelización integrado con **Comarch Loyalty Management (CLM)**.
Universidad Argentina de la Empresa (UADE) · Ingeniería de Software · 2026.

Este repositorio contiene el código fuente de la **Etapa 3** del trabajo, presentado como evidencia técnica de la propuesta de consultoría de IT.

## Prevención de ataques por inyección de código

Carpeta [`prevencion-inyeccion/`](./prevencion-inyeccion). Cuatro defensas, cada una con su demo ejecutable que muestra un caso legítimo aceptado y un intento de ataque bloqueado.

| Archivo | Ataque que previene | Técnica |
|---|---|---|
| `01_sql_injection.py` | SQL Injection | Consultas parametrizadas (placeholders) + validación de formato |
| `02_command_injection.py` | Command Injection | Lista blanca de valores permitidos, sin `shell=True` |
| `03_xss.py` | Cross-Site Scripting (XSS) | `html.escape` + límite de longitud |
| `04_api_input_validation.py` | Abuso de API / mass-assignment | Validación de tipo, rango y campos exactos |

### Cómo ejecutar

Requiere Python 3.10 o superior. No usa dependencias externas (solo librería estándar).

```bash
# Correr una defensa puntual
python prevencion-inyeccion/01_sql_injection.py

# Correr las cuatro juntas
python prevencion-inyeccion/run_all.py
```

## Integrantes

Grupo 2 — Melinda Selles (PM), Facundo Camilotto, Javier Renna, Julián Armagno, Nicolás Tombolán, Juan Manuel Pla.
