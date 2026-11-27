# Diccionario de datos

## Base de datos 1 — `documentos` (catálogo de directrices)

Archivo `data/raw/documentos.csv`, generado por `scripts/data_acquisition/main.py`. Tiene un registro por cada Directriz Técnica de la DNED (25 registros) con los metadatos de la descarga y de la extracción del texto. Los rangos y valores de la tabla son los que salieron en la ejecución del 26 de noviembre de 2026.

| Variable | Descripción | Tipo de dato | Rango/Valores posibles | Fuente de datos |
| --- | --- | --- | --- | --- |
| num_directriz | Número oficial de la directriz técnica | Entero | 1 – 25 | URL del PDF (`Directriz_{n}_`), `acquisition.py` |
| nombre_archivo | Nombre del PDF descargado | Texto (string) | `Directriz_1.pdf` … `Directriz_25.pdf` | `acquisition.py` |
| url_fuente | URL pública del PDF | Texto (URL) | `https://web.unal.edu.co/direccion/estrategia-digital/cms/uploads/Directriz_{n}_{hash}.pdf` | Lista `URLS` de `acquisition.py` |
| sha256 | Hash del PDF para detectar cambios | Texto (64 caracteres hex) | 25 valores distintos | Calculado en la descarga, `acquisition.py` |
| num_paginas | Número de páginas del PDF | Entero | 2 – 8 (88 en total) | Metadatos del PDF (`pypdf`), `extraction.py` |
| metodo_extraccion | Cómo se obtuvo el texto | Categórica (string) | `texto_nativo`, `ocr`, `sin_ocr`; `ocr` en los 25 documentos | `extraction.py` |
| num_caracteres | Longitud del texto extraído | Entero | 3587 – 20.309 (202.035 en total) | `extraction.py` |
| archivo_texto | Archivo con el texto extraído | Texto (string) | `Directriz_1.txt` … `Directriz_25.txt` | `extraction.py` |
| fecha_descarga | Fecha y hora de la descarga (UTC) | Fecha-hora (ISO 8601) | 2026-11-27T02:57:09+00:00 – 2026-11-27T02:57:18+00:00 | Fecha de modificación del PDF descargado, `acquisition.py` |

- **Variable**: nombre de la variable.
- **Descripción**: breve descripción de la variable.
- **Tipo de dato**: tipo de dato que contiene la variable.
- **Rango/Valores posibles**: rango o valores que puede tomar la variable.
- **Fuente de datos**: fuente de los datos de la variable.

### Listado de documentos del corpus

Los 25 documentos están en **español**. El número de páginas sale de los metadatos de cada PDF; el número de palabras se calculará en el análisis exploratorio (ver `data_summary.md`).

| No. | Nombre del documento | Idioma | Páginas | Archivo |
| --- | --- | --- | --- | --- |
| 1 | Directriz Técnica No. 01 – Solicitud de conceptos técnicos | Español (`es`) | 2 | Directriz_1.pdf |
| 2 | Directriz Técnica No. 02 – Adquisición de licencias de software específicas | Español (`es`) | 3 | Directriz_2.pdf |
| 3 | Directriz Técnica No. 03 – Actualización del sistema operativo Windows y la herramienta Office | Español (`es`) | 3 | Directriz_3.pdf |
| 4 | Directriz Técnica No. 04 – Análisis de viabilidad para la adquisición y/o desarrollo de soluciones informáticas | Español (`es`) | 3 | Directriz_4.pdf |
| 5 | Directriz Técnica No. 05 – Adquisición de servidores e integración a la plataforma de virtualización | Español (`es`) | 2 | Directriz_5.pdf |
| 6 | Directriz Técnica No. 06 – Desarrollo y/o implementación de soluciones informáticas para la gestión de información | Español (`es`) | 2 | Directriz_6.pdf |
| 7 | Directriz Técnica No. 07 – Mantenimiento y soporte de soluciones informáticas | Español (`es`) | 5 | Directriz_7.pdf |
| 8 | Directriz Técnica No. 08 – Acuerdos de Nivel de Servicio (ANS) para servicios alojados en TI | Español (`es`) | 2 | Directriz_8.pdf |
| 9 | Directriz Técnica No. 09 – Implantación de soluciones para la gestión unificada de amenazas a la seguridad de las redes de datos | Español (`es`) | 3 | Directriz_9.pdf |
| 10 | Directriz Técnica No. 10 – Uso de software libre | Español (`es`) | 3 | Directriz_10.pdf |
| 11 | Directriz Técnica No. 11 – Selección de contratistas en asuntos de informática y comunicaciones | Español (`es`) | 2 | Directriz_11.pdf |
| 12 | Directriz Técnica No. 12 – Servicio de telefonía | Español (`es`) | 3 | Directriz_12.pdf |
| 13 | Directriz Técnica No. 13 – Actualización sistema operativo Windows Desktop | Español (`es`) | 4 | Directriz_13.pdf |
| 14 | Directriz Técnica No. 14 – Mantenimiento preventivo y correctivo, ampliaciones, diseños y nuevos proyectos de cableado estructurado | Español (`es`) | 4 | Directriz_14.pdf |
| 15 | Directriz Técnica No. 15 –  no tiene titulo explicito* | Español (`es`) | 3 | Directriz_15.pdf |
| 16 | Directriz Técnica No. 16 – Política de seguridad informática y de la información para backups y recuperaciones | Español (`es`) | 6 | Directriz_16.pdf |
| 17 | Directriz Técnica No. 17 – Implementación de aplicaciones móviles | Español (`es`) | 2 | Directriz_17.pdf |
| 18 | Directriz Técnica No. 18 – Tipos de licenciamiento de software | Español (`es`) | 8 | Directriz_18.pdf |
| 19 | Directriz Técnica No. 19 – Sistema EasyPos para puntos de venta presenciales | Español (`es`) | 4 | Directriz_19.pdf |
| 20 | Directriz Técnica No. 20 – Carné institucional | Español (`es`) | 6 | Directriz_20.pdf |
| 21 | Directriz Técnica No. 21 – Renting de equipos de cómputo para la Universidad Nacional de Colombia | Español (`es`) | 4 | Directriz_21.pdf |
| 22 | Directriz Técnica No. 22 – Control de acceso | Español (`es`) | 5 | Directriz_22.pdf |
| 23 | Directriz Técnica No. 23 – Elementos tecnológicos para la plataforma de comunicaciones unificadas | Español (`es`) | 2 | Directriz_23.pdf |
| 24 | Directriz Técnica No. 24 – Aulas híbridas | Español (`es`) | 5 | Directriz_24.pdf |
| 25 | Directriz Técnica No. 25 – Compra de equipos de cómputo, impresoras y escáner | Español (`es`) | 2 | Directriz_25.pdf |
| | **Total** | **Español** | **88** | 25 PDF |