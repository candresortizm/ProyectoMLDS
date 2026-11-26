"""Carga de datos: descarga las Directrices Técnicas de la DNED y extrae su texto.

Uso (desde la raíz del repositorio):

    uv run python scripts/data_acquisition/main.py
    uv run python scripts/data_acquisition/main.py --sin-ocr      # sin Tesseract
    uv run python scripts/data_acquisition/main.py --forzar-ocr   # OCR en todos

Salidas:

    data/raw/pdf/Directriz_{n}.pdf   PDF originales
    data/raw/text/Directriz_{n}.txt  texto extraído (páginas separadas por ---)
    data/raw/documentos.csv          metadatos de cada documento
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from nombre_paquete.database import cargar_corpus, descargar_directrices, extraer_corpus

RAIZ = Path(__file__).resolve().parents[2]
DATA_DIR = RAIZ / "data" / "raw"

COLUMNAS = [
    "num_directriz",
    "nombre_archivo",
    "url_fuente",
    "sha256",
    "num_paginas",
    "metodo_extraccion",
    "num_caracteres",
    "archivo_texto",
    "fecha_descarga",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR, help="carpeta de salida")
    parser.add_argument("--sobrescribir", action="store_true", help="vuelve a descargar los PDF")
    parser.add_argument("--forzar-ocr", action="store_true", help="aplica OCR a todos los documentos")
    parser.add_argument("--sin-ocr", action="store_true", help="no aplica OCR (solo texto nativo)")
    args = parser.parse_args()

    pdf_dir = args.data_dir / "pdf"
    text_dir = args.data_dir / "text"

    print("1. Descargando directrices...")
    registros = descargar_directrices(pdf_dir, sobrescribir=args.sobrescribir)

    print("\n2. Extrayendo texto...")
    extraccion = extraer_corpus(
        pdf_dir, text_dir, forzar_ocr=args.forzar_ocr, permitir_ocr=not args.sin_ocr
    )

    for registro in registros:
        registro.update(extraccion.get(registro["nombre_archivo"], {}))

    metadatos = args.data_dir / "documentos.csv"
    with metadatos.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS)
        writer.writeheader()
        writer.writerows(registros)

    corpus = cargar_corpus(text_dir)
    ocr = sum(r.get("metodo_extraccion") == "ocr" for r in registros)
    print(f"\n✅ {len(corpus)} documentos cargados ({ocr} con OCR)")
    print(f"   Textos: {text_dir}")
    print(f"   Metadatos: {metadatos}")


if __name__ == "__main__":
    main()
