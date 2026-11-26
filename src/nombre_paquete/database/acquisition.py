"""Descarga de las Directrices Técnicas de la DNED.

Los PDF se descargan desde la página de la Dirección Nacional de Estrategia
Digital y se guardan como ``Directriz_{n}.pdf``. Por cada documento se registran
los metadatos definidos en ``docs/data/data_dictionary.md``.
"""

from __future__ import annotations

import hashlib
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE_URL = "https://web.unal.edu.co/direccion/estrategia-digital/cms/uploads"

# Página pública donde se listan las directrices:
# https://web.unal.edu.co/direccion/estrategia-digital/estructura-dned/directrices-tecnicas
URLS = [
    f"{BASE_URL}/Directriz_1_6f071dbcbc.pdf",
    f"{BASE_URL}/Directriz_2_fa406e2219.pdf",
    f"{BASE_URL}/Directriz_3_a91ee78d02.pdf",
    f"{BASE_URL}/Directriz_4_f0a23b94e5.pdf",
    f"{BASE_URL}/Directriz_5_500869ada0.pdf",
    f"{BASE_URL}/Directriz_6_b5c037e81b.pdf",
    f"{BASE_URL}/Directriz_7_5755844f38.pdf",
    f"{BASE_URL}/Directriz_8_e4a6f93d0c.pdf",
    f"{BASE_URL}/Directriz_9_3322b6fd83.pdf",
    f"{BASE_URL}/Directriz_10_c648893449.pdf",
    f"{BASE_URL}/Directriz_11_97cd17b4f8.pdf",
    f"{BASE_URL}/Directriz_12_c4e46d27ce.pdf",
    f"{BASE_URL}/Directriz_13_51386f9405.pdf",
    f"{BASE_URL}/Directriz_14_5b370d3ceb.pdf",
    f"{BASE_URL}/Directriz_15_0c596598b6.pdf",
    f"{BASE_URL}/Directriz_16_d6a8cec713.pdf",
    f"{BASE_URL}/Directriz_17_e6b031dba8.pdf",
    f"{BASE_URL}/Directriz_18_5c83e09421.pdf",
    f"{BASE_URL}/Directriz_19_68c9c711ac.pdf",
    f"{BASE_URL}/Directriz_20_f1e5d9ae42.pdf",
    f"{BASE_URL}/Directriz_21_3381f003e5.pdf",
    f"{BASE_URL}/Directriz_22_b9e75e53c7.pdf",
    f"{BASE_URL}/Directriz_23_4cef5654ec.pdf",
    f"{BASE_URL}/Directriz_24_fa980e8699.pdf",
    f"{BASE_URL}/Directriz_25_331f9f6dca.pdf",
]


def numero_directriz(url: str) -> int:
    """Obtiene el número de la directriz a partir de su URL."""
    match = re.search(r"Directriz_(\d+)_", url)
    if match is None:
        raise ValueError(f"No se pudo obtener el número de directriz de: {url}")
    return int(match.group(1))


def sha256(path: Path) -> str:
    """Calcula el hash SHA-256 de un archivo para detectar cambios."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def descargar_pdf(url: str, destino: Path, reintentos: int = 3, timeout: int = 60) -> Path:
    """Descarga un PDF y lo guarda en ``destino``. Reintenta ante errores de red."""
    for intento in range(1, reintentos + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            if not response.content.startswith(b"%PDF"):
                raise ValueError("la respuesta no es un archivo PDF")
            destino.write_bytes(response.content)
            return destino
        except (requests.RequestException, ValueError) as error:
            if intento == reintentos:
                raise RuntimeError(f"No se pudo descargar {url}: {error}") from error
            time.sleep(2 * intento)
    return destino


def descargar_directrices(
    directorio: Path, urls: list[str] | None = None, sobrescribir: bool = False
) -> list[dict]:
    """Descarga todas las directrices y retorna sus metadatos.

    Parámetros
    ----------
    directorio:
        Carpeta donde se guardan los PDF.
    urls:
        Lista de URL a descargar. Por defecto, las 25 directrices.
    sobrescribir:
        Si es ``False`` no se vuelven a descargar los archivos que ya existen.

    Retorna
    -------
    Lista de diccionarios con ``num_directriz``, ``nombre_archivo``,
    ``url_fuente``, ``sha256`` y ``fecha_descarga``.
    """
    directorio = Path(directorio)
    directorio.mkdir(parents=True, exist_ok=True)
    registros = []

    for url in urls or URLS:
        numero = numero_directriz(url)
        destino = directorio / f"Directriz_{numero}.pdf"

        if destino.exists() and not sobrescribir:
            print(f"= {destino.name} (ya existe)")
        else:
            descargar_pdf(url, destino)
            print(f"✓ {destino.name}")

        registros.append(
            {
                "num_directriz": numero,
                "nombre_archivo": destino.name,
                "url_fuente": url,
                "sha256": sha256(destino),
                "fecha_descarga": datetime.fromtimestamp(
                    destino.stat().st_mtime, tz=timezone.utc
                ).isoformat(timespec="seconds"),
            }
        )

    return sorted(registros, key=lambda r: r["num_directriz"])
