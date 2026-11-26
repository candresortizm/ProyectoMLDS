# Team Data Science Project Template

Esta plantilla es una implementación de la plantilla de proyecto de Team Data Science Process que actualmente se utiliza en el "Programa de Formación en Machine Learning y Data Science" en la Universidad Nacional de Colombia.

Esta plantilla proporciona las siguientes carpetas y archivos:

* `src`: acá debe ir el código o implementación del proyecto en Python.
* `docs`: en esta carpeta se encuentran las plantillas de los documentos definidos en la metodología.
* `scripts`: esta carpeta debe contener los scripts/notebooks que se ejecutarán.
* `pyproject.toml`: archivo de definición del proyecto en Python.

## Proyecto: búsqueda semántica en las Directrices Técnicas de la DNED

Grupo 3: Miguel Alejandro Bermúdez Claros, Camilo Andrés Ortiz Morales y José Ricardo Cepeda Cepeda.

El marco del proyecto está en [`docs/business_understanding/project_charter.md`](docs/business_understanding/project_charter.md).

### Carga de datos

Las directrices son PDF escaneados, por lo que la extracción usa OCR (Tesseract en español).

**En Google Colab:**

```bash
!apt-get install -y -qq poppler-utils tesseract-ocr tesseract-ocr-spa
!git clone https://github.com/candresortizm/ProyectoMLDS.git
%cd ProyectoMLDS
!pip install -q -e ".[ocr]"
!python scripts/data_acquisition/main.py
```

**En local** (requiere [uv](https://docs.astral.sh/uv/), Tesseract y Poppler instalados):

```bash
uv sync --extra ocr
uv run python scripts/data_acquisition/main.py
```

El script descarga los 25 PDF en `data/raw/pdf/`, guarda el texto de cada directriz en `data/raw/text/` y los metadatos (URL, hash SHA-256, páginas, método de extracción) en `data/raw/documentos.csv`. Opciones: `--sin-ocr`, `--forzar-ocr`, `--sobrescribir`.
