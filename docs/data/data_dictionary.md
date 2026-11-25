# Diccionario de datos

## Base de datos 1 — `documentos` (catálogo de directrices)

Tabla con un registro por cada Directriz Técnica de la DNED (25 registros). Contiene los metadatos que se extraen de cada PDF y sirve para filtrar los resultados y citar la fuente en la búsqueda semántica.

| Variable | Descripción | Tipo de dato | Rango/Valores posibles | Fuente de datos |
| --- | --- | --- | --- | --- |
| num_directriz | Número oficial de la directriz técnica | Entero | 1 – 25 | Encabezado del PDF ("DIRECTRIZ TÉCNICA No. XX") |
| nombre_documento | Nombre oficial de la directriz (número + tema) | Texto (string) | p. ej. "Directriz Técnica No. 07 – Mantenimiento y soporte de soluciones informáticas" (ver el listado al final de esta sección) | Encabezado del PDF |
| titulo | Título o tema de la directriz | Texto (string) | Texto libre, p. ej. "Mantenimiento y soporte de soluciones informáticas" | Encabezado del PDF |
| idioma | Idioma en que está escrito el documento | Categórica (código ISO 639-1) | `es` (español) en los 25 documentos | Detección automática (`langdetect`) y verificación manual |
| texto_completo | Texto íntegro de la directriz ya limpio (sin pies de página ni encabezados repetidos) | Texto (string) | Longitud variable; se mide en el análisis exploratorio | PDF tras la extracción y la limpieza |
| palabras | Palabras (tokens) que componen el documento, en orden | Lista de texto | Tokens en español, incluidas siglas (ANS, TI, UTM, RAM) y nombres propios (Windows, Office, EasyPos) | Tokenización de `texto_completo` (spaCy `es_core_news_sm`) |
| vocabulario | Palabras únicas del documento (lematizadas, sin *stopwords*), con su frecuencia | Diccionario {palabra: frecuencia} | Depende del documento | Calculado a partir de `palabras` |
| num_palabras_unicas | Tamaño del vocabulario del documento | Entero | **[PENDIENTE — análisis exploratorio]** | Calculado a partir de `vocabulario` |
| fecha_expedicion | Fecha de expedición de la directriz | Fecha (YYYY-MM-DD) | 2024-10-01 (23 docs), 2025-03-06 (No. 15), 2025-06-18 (No. 22) | Encabezado del PDF |
| categoria | Área temática asignada para filtrar | Categórica (string) | `contratacion_adquisiciones`, `software_licenciamiento`, `desarrollo_soporte`, `infraestructura_redes`, `seguridad_informacion`, `identidad_servicios` | Etiquetado manual del equipo del proyecto |
| url_fuente | URL pública del PDF | Texto (URL) | `https://web.unal.edu.co/direccion/estrategia-digital/cms/uploads/Directriz_{n}_{hash}.pdf` | Lista de URL del proyecto |
| nombre_archivo | Nombre del archivo descargado | Texto (string) | `Directriz_1.pdf` … `Directriz_25.pdf` | `scripts/data_acquisition/main.py` |
| sha256 | Hash del PDF para detectar cambios | Texto (64 caracteres hex) | Hexadecimal | Calculado en la descarga |
| num_paginas | Número de páginas del PDF | Entero | 2 – 8 | Metadatos del PDF |
| num_palabras | Palabras del texto ya limpio | Entero | **[PENDIENTE — análisis exploratorio]** | Calculado en el preprocesamiento |
| tiene_tablas | Indica si el documento contiene tablas | Booleano | `true` / `false` (true en No. 7, 13, 19, 20, 21) | Extracción de tablas (`pdfplumber`) |
| metodo_extraccion | Cómo se obtuvo el texto | Categórica (string) | `texto_nativo`, `ocr` (No. 15) | `extract_text.py` |
| fecha_descarga | Fecha y hora de la descarga | Fecha-hora (ISO 8601) | — | `scripts/data_acquisition/main.py` |

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