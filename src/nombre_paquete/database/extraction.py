"""Extracción del texto de las Directrices Técnicas.

Se intenta primero leer el texto nativo del PDF. Si el documento está escaneado
(casi no tiene texto seleccionable) se aplica OCR con Tesseract:

1. Cada página se convierte en imagen con ``pdf2image``.
2. Con OpenCV la imagen se binariza (método de Otsu) y se detectan los bloques
   de texto; se descartan los que caen en el encabezado y el pie de página.
3. Cada bloque se pasa por Tesseract en español.

El OCR requiere tener instalados Tesseract (con el idioma ``spa``) y Poppler.
En Colab: ``apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-spa``.
"""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

# Si un PDF tiene menos caracteres por página que este umbral se considera escaneado.
MIN_CARACTERES_POR_PAGINA = 200

# Región útil de la página a 200 DPI (fuera de ella están el encabezado y el pie).
DPI = 200
Y_MIN, Y_MAX = 150, 2000
X_MIN, X_MAX = 300, 1400

SEPARADOR_PAGINA = "\n\n---\n\n"


def _orden_numerico(path: Path):
    """Ordena ``Directriz_2`` antes que ``Directriz_10``."""
    sufijo = path.stem.split("_")[-1]
    return (0, int(sufijo), "") if sufijo.isdigit() else (1, 0, path.stem)


def numero_paginas(pdf: Path) -> int:
    """Número de páginas de un PDF."""
    return len(PdfReader(str(pdf)).pages)


def extraer_texto_nativo(pdf: Path) -> list[str]:
    """Extrae el texto seleccionable de cada página del PDF."""
    reader = PdfReader(str(pdf))
    return [(pagina.extract_text() or "").strip() for pagina in reader.pages]


def es_escaneado(paginas: list[str]) -> bool:
    """Indica si el PDF no tiene suficiente texto nativo y requiere OCR."""
    if not paginas:
        return True
    caracteres = sum(len(p) for p in paginas)
    return caracteres / len(paginas) < MIN_CARACTERES_POR_PAGINA


def ocr_imagen(imagen, idioma: str = "spa") -> str:
    """Aplica OCR a una imagen (``PIL.Image``) ignorando encabezado y pie de página."""
    import cv2
    import numpy as np
    import pytesseract

    img = np.array(imagen.convert("RGB"))
    gris = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, binaria = cv2.threshold(gris, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Un kernel grande agrupa las palabras en bloques de texto (párrafos).
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
    dilatada = cv2.dilate(binaria, kernel, iterations=1)
    contornos, _ = cv2.findContours(dilatada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Se ordenan los bloques de arriba hacia abajo para conservar el orden de lectura.
    cajas = sorted((cv2.boundingRect(c) for c in contornos), key=lambda b: (b[1], b[0]))

    textos = []
    for x, y, w, h in cajas:
        if y + h > Y_MAX or y < Y_MIN or x + w < X_MIN or x > X_MAX:
            continue  # encabezado o pie de página
        recorte = img[y : y + h, x : x + w]
        textos.append(pytesseract.image_to_string(recorte, lang=idioma).strip())

    return "\n".join(t for t in textos if t)


def extraer_texto_ocr(pdf: Path, idioma: str = "spa") -> list[str]:
    """Extrae el texto de cada página de un PDF escaneado mediante OCR."""
    from pdf2image import convert_from_path

    return [ocr_imagen(pagina, idioma) for pagina in convert_from_path(str(pdf), dpi=DPI)]


def extraer_texto(pdf: Path, forzar_ocr: bool = False, permitir_ocr: bool = True) -> tuple[str, str]:
    """Extrae el texto de un PDF.

    Retorna una tupla ``(texto, metodo_extraccion)`` donde el método es
    ``"texto_nativo"``, ``"ocr"`` o ``"sin_ocr"`` (escaneado, pero se omitió el OCR). Las páginas se separan con ``---``.
    """
    paginas = [] if forzar_ocr else extraer_texto_nativo(pdf)
    metodo = "texto_nativo"

    if forzar_ocr or es_escaneado(paginas):
        if not permitir_ocr:
            print(f"! {pdf.name} parece escaneado; se omitió el OCR")
            metodo = "sin_ocr"
        else:
            paginas = extraer_texto_ocr(pdf)
            metodo = "ocr"

    return SEPARADOR_PAGINA.join(paginas).strip(), metodo


def extraer_corpus(
    directorio_pdf: Path,
    directorio_texto: Path,
    forzar_ocr: bool = False,
    permitir_ocr: bool = True,
) -> dict[str, dict]:
    """Extrae el texto de todos los PDF de una carpeta y lo guarda como ``.txt``.

    Retorna un diccionario ``{nombre_archivo_pdf: metadatos}`` con
    ``num_paginas``, ``metodo_extraccion``, ``num_caracteres`` y ``archivo_texto``.
    """
    directorio_texto = Path(directorio_texto)
    directorio_texto.mkdir(parents=True, exist_ok=True)
    resultados = {}

    for pdf in sorted(Path(directorio_pdf).glob("*.pdf"), key=_orden_numerico):
        texto, metodo = extraer_texto(pdf, forzar_ocr=forzar_ocr, permitir_ocr=permitir_ocr)
        salida = directorio_texto / f"{pdf.stem}.txt"
        salida.write_text(texto, encoding="utf-8")
        print(f"✓ {salida.name} ({metodo}, {len(texto)} caracteres)")

        resultados[pdf.name] = {
            "num_paginas": numero_paginas(pdf),
            "metodo_extraccion": metodo,
            "num_caracteres": len(texto),
            "archivo_texto": salida.name,
        }

    return resultados


def cargar_corpus(directorio_texto: Path, patron: str = "*.txt") -> dict[str, str]:
    """Carga los textos extraídos como ``{nombre_documento: texto}``."""
    archivos = sorted(Path(directorio_texto).glob(patron), key=_orden_numerico)
    return {archivo.stem: archivo.read_text(encoding="utf-8") for archivo in archivos}
