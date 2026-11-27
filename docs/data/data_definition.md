# Definición de los datos

## Origen de los datos

Los datos del proyecto son las **25 Directrices Técnicas** publicadas por la Dirección Nacional de Estrategia Digital (DNED) de la Universidad Nacional de Colombia. La DNED las expide en ejercicio de la función que le asigna el artículo 3 del Acuerdo 316 de 2019 del Consejo Superior Universitario, y son de cumplimiento obligatorio para las dependencias.

- **Fuente:** página oficial de la DNED, sección [Directrices técnicas](https://web.unal.edu.co/direccion/estrategia-digital/estructura-dned/directrices-tecnicas).
- **Formato:** un archivo PDF por directriz.
- **Idioma:** español (`es`) en los 25 documentos.
- **Tamaño:** 25 documentos, 88 páginas en total (entre 2 y 8 páginas por directriz).
- **Fechas de expedición:** 2024-10-01 (23 directrices), 2025-03-06 (No. 15) y 2025-06-18 (No. 22).
- **Características:** los 25 PDF tienen al menos una página escaneada, por lo que en la ejecución del 26 de noviembre de 2026 todos se procesaron con OCR. En las páginas escaneadas el único texto nativo es el pie de página (entre 0 y 169 caracteres). La No. 13 mezcla páginas escaneadas con páginas que tienen parte de una tabla como texto nativo. Los documentos No. 7, 13, 19, 20 y 21 contienen tablas.

**Forma de obtención:** los PDF se descargan de forma automatizada por HTTP a partir de una lista de 25 URL (una por directriz) definida en el código, y después se extrae el texto de cada documento (texto nativo del PDF u OCR con Tesseract).

Quedan por fuera del alcance otros documentos de la Universidad (resoluciones, acuerdos, circulares u otras normas) y la actualización automática del corpus cuando la DNED publique nuevas directrices.

## Especificación de los scripts para la carga de datos

| Archivo | Función |
| --- | --- |
| `scripts/data_acquisition/main.py` | Punto de entrada. Ejecuta la descarga y la extracción de texto. |
| `src/nombre_paquete/database/acquisition.py` | Descarga de los PDF. Contiene la lista `URLS` de las 25 directrices y las funciones `numero_directriz`, `sha256`, `descargar_pdf` y `descargar_directrices`. |
| `src/nombre_paquete/database/extraction.py` | Extracción del texto. Funciones `extraer_texto_nativo` (`pypdf`), `es_escaneado`, `ocr_imagen` y `extraer_texto_ocr` (`pdf2image` + OpenCV + Tesseract), `extraer_texto`, `extraer_corpus` y `cargar_corpus`. |
| `src/nombre_paquete/database/__init__.py` | Expone `URLS`, `descargar_directrices`, `extraer_corpus`, `extraer_texto` y `cargar_corpus`. |

**Dependencias** (declaradas en `pyproject.toml`):

- Base: `numpy`, `requests`, `pypdf`.
- Extra `ocr`: `pdf2image`, `pytesseract`, `opencv-python-headless`, `pillow`.
- Del sistema: Tesseract con el idioma español (`spa`) y Poppler.

**Ejecución:**

En Google Colab:

```bash
!apt-get install -y -qq poppler-utils tesseract-ocr tesseract-ocr-spa
!git clone https://github.com/candresortizm/ProyectoMLDS.git
%cd ProyectoMLDS
!pip install -q -e ".[ocr]"
!python scripts/data_acquisition/main.py
```

En local (con [uv](https://docs.astral.sh/uv/), Tesseract y Poppler instalados):

```bash
uv sync --extra ocr
uv run python scripts/data_acquisition/main.py
```

**Opciones del script:**

| Opción | Efecto |
| --- | --- |
| `--data-dir RUTA` | Carpeta de salida. |
| `--sobrescribir` | Vuelve a descargar los PDF aunque ya existan. |
| `--forzar-ocr` | Aplica OCR a todos los documentos. |
| `--sin-ocr` | No aplica OCR (solo texto nativo). |

## Referencias a rutas o bases de datos origen y destino

### Rutas de origen de datos

**Ubicación.** Los PDF están en `https://web.unal.edu.co/direccion/estrategia-digital/cms/uploads/`, con el patrón `Directriz_{n}_{hash}.pdf`, donde `{n}` es el número de la directriz (1 a 25), por ejemplo `Directriz_7_5755844f38.pdf`. La lista completa está en la constante `URLS` de `src/nombre_paquete/database/acquisition.py`.

**Estructura de los archivos de origen.** Cada PDF corresponde a una directriz. El encabezado contiene el número ("DIRECTRIZ TÉCNICA No. XX"), el título y la fecha de expedición, y cada página tiene encabezado y pie de página. El listado de los 25 documentos (número, nombre, idioma, páginas y archivo) está en `docs/data/data_dictionary.md`.

**Procedimientos de transformación y limpieza en la carga** (según `acquisition.py` y `extraction.py`):

1. **Descarga y validación.** Cada URL se descarga con `requests` (tiempo límite de 60 s y hasta 3 reintentos). Se verifica que el contenido empiece por `%PDF`. Si el archivo ya existe no se vuelve a descargar, salvo con `--sobrescribir`.
2. **Nombre del archivo.** El número de la directriz se obtiene de la URL con la expresión regular `Directriz_(\d+)_` y el archivo se guarda como `Directriz_{n}.pdf`.
3. **Hash.** Se calcula el SHA-256 de cada PDF para detectar cambios.
4. **Detección de documentos escaneados.** Se lee el texto nativo con `pypdf`. Si alguna página tiene menos de 200 caracteres, el documento se considera escaneado y se le aplica OCR completo. Al principio la regla usaba el promedio por página, pero con ella la No. 13 (310 caracteres por página en promedio) quedaba sin OCR y perdía el cuerpo del documento. Por eso se cambió para mirar cada página.
5. **OCR.** Cada página se convierte en imagen a 200 DPI (`pdf2image`). Con OpenCV se binariza (método de Otsu), se dilata con un kernel de 30×30 para agrupar el texto en bloques, se ordenan los bloques de arriba hacia abajo y se descartan los que quedan fuera de la región útil (y entre 150 y 2000, x entre 300 y 1400), que corresponden al encabezado y el pie de página. Cada bloque se procesa con Tesseract en español.
6. **Unión de páginas.** El texto de las páginas se une con el separador `---`.

La limpieza lingüística (normalización, *stopwords*, lematización y segmentación) corresponde a la fase de preparación del corpus.

**Resultados de la ejecución** (26 de noviembre de 2026, macOS, Tesseract con idioma `spa` y Poppler instalados con Homebrew, `uv run python scripts/data_acquisition/main.py`):

- Se descargaron los 25 PDF sin errores (17 MB en total) y suman 88 páginas, igual que el listado del diccionario de datos.
- El script terminó con "25 documentos cargados (25 con OCR)". Con la primera versión de la regla de detección (promedio por página), la extracción completa tardó cerca de 81 segundos.
- **Pie de página:** en los 25 textos no aparece ninguna línea del pie ("Página X de Y", "Elaboró: DNED", el teléfono o el correo `dned@unal.edu.co`).
- **Encabezado:** la línea "Dirección Nacional de Estrategia Digital" se conserva solo una vez por documento, como primera línea de la página 1.
- **Errores del OCR encontrados:**
  - "Unidad Estratégica TI" se reconoce como "Unidad Estratégica Tl" en los 25 documentos.
  - Las palabras partidas por guion al final de línea se conservan partidas (p. ej. "DE-" / "PENDENCIAS"), y hay líneas que terminan en guion en los 25 textos.
  - En las tablas, el OCR lee las celdas por bloques y mezcla las columnas (p. ej. en la tabla de requisitos de Windows de la No. 13).

### Base de datos de destino

**Destino.** Los datos cargados se guardan como archivos en `data/raw/`, dentro del repositorio local. Esa carpeta está en `.gitignore`, así que no se sube a GitHub y se regenera con el script. Según el project charter, en la fase de modelamiento el corpus se indexará en una base de datos vectorial para la búsqueda por similitud.

**Estructura generada:**

```
data/raw/
├── pdf/              # 25 archivos: Directriz_1.pdf … Directriz_25.pdf (17 MB)
├── text/             # 25 archivos: Directriz_1.txt … Directriz_25.txt (256 KB)
└── documentos.csv    # encabezado + 25 filas, una por directriz
```

Columnas de `documentos.csv` (ejemplo de la primera fila):

| Columna | Descripción | Ejemplo (Directriz No. 1) |
| --- | --- | --- |
| `num_directriz` | Número de la directriz | `1` |
| `nombre_archivo` | Nombre del PDF descargado | `Directriz_1.pdf` |
| `url_fuente` | URL de origen | `https://web.unal.edu.co/direccion/estrategia-digital/cms/uploads/Directriz_1_6f071dbcbc.pdf` |
| `sha256` | Hash SHA-256 del PDF | `90e81aadcb9c17d3366d2245547418f6abcc3586ccd8735416cadcfd73b19231` |
| `num_paginas` | Páginas del PDF | `2` |
| `metodo_extraccion` | `texto_nativo`, `ocr` o `sin_ocr` | `ocr` |
| `num_caracteres` | Caracteres del texto extraído | `5403` |
| `archivo_texto` | Archivo `.txt` con el texto | `Directriz_1.txt` |
| `fecha_descarga` | Fecha y hora de la descarga (UTC) | `2026-11-27T02:57:09+00:00` |

El texto extraído suma 202.035 caracteres. El documento más corto es la No. 17 (3587 caracteres) y el más largo la No. 18 (20.309 caracteres).

**Procedimiento de carga.** `main.py` une los registros de `descargar_directrices` (número, archivo, URL, hash y fecha de descarga) con los de `extraer_corpus` (páginas, método, caracteres y archivo de texto) por el nombre del PDF, y escribe `documentos.csv` en UTF-8. Al final, `cargar_corpus` lee los 25 `.txt` como un diccionario `{nombre_documento: texto}`, que es la entrada de las fases de análisis exploratorio y preprocesamiento.
