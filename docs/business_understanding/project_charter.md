# Project Charter - Entendimiento del Negocio

## Nombre del Proyecto

Sistema de búsqueda semántica sobre las Directrices Técnicas de la Dirección Nacional de Estrategia Digital (DNED) de la Universidad Nacional de Colombia.

## Objetivo del Proyecto

Desarrollar un sistema de búsqueda semántica basado en procesamiento de lenguaje natural (NLP) que permita a la DNED y a las dependencias de la Universidad acceder rápidamente a las Directrices Técnicas mediante consultas en lenguaje natural.

### Trasfondo del negocio

La DNED fue creada por el Consejo Superior Universitario (CSU) mediante el Acuerdo 316 de 2019 y actúa como el máximo ente coordinador, regulador y asesor de las iniciativas digitales, la seguridad informática y la gobernanza de las Tecnologías de la Información y las Comunicaciones (TIC) de la Universidad. Su estructura interna está compuesta por tres oficinas (Arquitectura Organizacional, Gestión de la Información y Gobierno y Gestión Administrativa) y dos divisiones (Universidad Laboratorio y Gestión Tecnológica, esta última con las secciones de Seguridad de la Información, Aplicaciones, Infraestructura y Gestión de Servicios de TI e Identidades Digitales).

El artículo 3 del mismo acuerdo le asigna, entre otras, la función de:

> "Definir lineamientos sobre Tecnologías de la Información y las Comunicaciones para el cumplimiento de estándares de seguridad, privacidad, calidad y oportunidad de la información en la Universidad Nacional de Colombia." (Consejo Superior Universitario, 2019)

Estos lineamientos se publican como **Directrices Técnicas**, de cumplimiento obligatorio para las dependencias, y cubren un espectro amplio: desde cómo hacer el *backup* de una base de datos o una instalación de red, hasta las características mínimas (RAM, procesador, disco, etc.) para la compra de bienes y servicios de tecnología.

Aunque las directrices son públicas, en muchas ocasiones no son conocidas por las dependencias, ya sea por desconocimiento o por la dificultad para encontrar la información dentro de los documentos. Como consecuencia, la DNED recibe constantemente llamadas y correos solicitando información que ya está contenida en las directrices.

### Objetivos específicos

- Implementar rutinas de OCR y preprocesamiento de textos para digitalizar las Directrices Técnicas en español.
- Entrenar y evaluar diferentes modelos de *embeddings* para representar semánticamente el corpus documental.
- Desarrollar un sistema de búsqueda por similitud semántica que recupere los documentos y fragmentos relevantes según la consulta del usuario.
- Evaluar sistemáticamente el rendimiento del sistema en términos de precisión y relevancia de los resultados, comparándolo con métodos de búsqueda léxica (TF-IDF, BM25).

## Alcance del Proyecto

### Incluye:

- **Datos disponibles:** las 25 Directrices Técnicas publicadas en formato PDF en la página de la DNED ([directrices técnicas](https://web.unal.edu.co/direccion/estrategia-digital/estructura-dned/directrices-tecnicas)). Todos los documentos están en español y son escaneados (casi no tienen texto seleccionable), por lo que requieren reconocimiento óptico de caracteres (OCR). El detalle de las variables está en `docs/data/data_dictionary.md`.
- **Procesamiento de documentos:** descarga automatizada de los PDF, extracción del texto (texto nativo u OCR con Tesseract), limpieza de encabezados y pies de página, normalización y segmentación por secciones o páginas.
- **Modelamiento:** vectorización del corpus con diferentes modelos de *embeddings*, indexación en una base de datos vectorial y búsqueda por similitud, con un ranking de resultados por relevancia semántica.
- **Resultados esperados:** un sistema en el que el usuario escribe una consulta natural, por ejemplo *"Especificaciones técnicas para aulas de informática"*, y obtiene de inmediato los documentos relevantes ordenados por similitud, junto con los fragmentos específicos que responden la pregunta y la referencia al PDF de origen. La consulta se hará mediante una interfaz sencilla (*input*, API o página web simple).
- **Criterios de éxito:**
  - El 100 % de las directrices se descarga y se convierte a texto de forma reproducible mediante los scripts del repositorio.
  - Sobre un conjunto de consultas de prueba construido por el equipo, el sistema semántico supera al modelo base léxico (TF-IDF/BM25) en métricas de recuperación como Precision@k y MRR.
  - El documento correcto aparece entre los primeros resultados (top 3) para la mayoría de las consultas de prueba.
  - Las respuestas se entregan en pocos segundos y siempre citan la directriz de origen.
  - Interfaz para interacción con la herramienta, sea API o una interfaz gráfica sencilla.

### Excluye:

- Documentos distintos a las Directrices Técnicas de la DNED (resoluciones, acuerdos, circulares u otras normas de la Universidad).
- Actualización automática del corpus cuando la DNED publique nuevas directrices (el sistema queda preparado para escalar, pero la sincronización periódica no hace parte del alcance).
- Interpretación jurídica o validación normativa del contenido de las directrices.

## Metodología

El proyecto sigue la metodología **Team Data Science Process (TDSP)**, apoyada en las fases de **CRISP-DM**, ampliamente usada en proyectos de datos. El trabajo se organiza en entregas semanales, cada una con los documentos de la carpeta `docs/` y el código correspondiente en `scripts/` y `src/`:

1. **Entendimiento del negocio y carga de datos:** contexto del negocio, definición del problema y descarga y extracción de texto del corpus (`scripts/data_acquisition/`).
2. **Entendimiento y preparación del corpus:** análisis exploratorio (idioma, tamaño, categorías gramaticales, longitud de palabras, temas con LDA), limpieza de ruido de encabezados y pies de página, eliminación de *stopwords* y lematización. Se preparan distintas versiones del corpus: una normalizada para los métodos léxicos y otra que conserva el contexto para los modelos de *embeddings*.
3. **Extracción de características:** tokenización y segmentación del corpus en fragmentos que conserven el mejor contexto para la búsqueda.
4. **Modelamiento y evaluación:** modelo base léxico (TF-IDF/BM25), modelos de *embeddings* e indexación vectorial; comparación de las estrategias sobre las mismas consultas de prueba.
5. **Despliegue y entrega final:** interfaz de consulta, consolidación del proyecto, informe de salida y presentación.

El código se versiona en GitHub con commits semanales, y los experimentos de modelamiento se registran con MLflow.

## Cronograma

Entregas semanales a partir del inicio del proyecto (21 de noviembre de 2026). Las fechas se ajustarán al calendario oficial del curso.

| Etapa | Duración Estimada | Fechas |
|------|---------|-------|
| Entendimiento del negocio y carga de datos | 1 semana | del 21 al 27 de noviembre |
| Entendimiento y preparación del corpus (EDA y limpieza) | 1 semana | del 28 de noviembre al 4 de diciembre |
| Modelamiento y extracción de características (búsqueda semántica) | 1 semana | del 5 al 11 de diciembre |
| Despliegue | 1 semana | del 12 al 18 de diciembre |
| Evaluación y entrega final | 3 días | del 19 al 21 de diciembre |

## Equipo del Proyecto

**Grupo 3 – Programa de Formación en Machine Learning y Data Science, Universidad Nacional de Colombia**

- Miguel Alejandro Bermúdez Claros – Científico de datos
- Camilo Andrés Ortiz Morales – Científico de datos
- José Ricardo Cepeda Cepeda – Científico de datos

## Presupuesto

El proyecto se desarrolla en el marco académico del curso y no tiene un presupuesto monetario asignado. Se usan únicamente herramientas gratuitas y de código abierto:

- Cómputo en Google Colab (capa gratuita) y equipos personales del equipo.
- Bibliotecas de código abierto: Tesseract OCR, pdf2image, OpenCV, spaCy, NLTK, gensim, scikit-learn, sentence-transformers, MLflow.
- Repositorio y control de versiones en GitHub.

El principal recurso del proyecto es el tiempo de los tres integrantes del equipo durante las semanas del cronograma.

## Stakeholders

- **Dirección Nacional de Estrategia Digital (DNED):** propietaria de las directrices y principal beneficiaria. Espera reducir las consultas repetitivas por correo y teléfono y contar con un acceso centralizado e inteligente a sus lineamientos.
- **Dependencias de la Universidad (áreas de contratación, compras y TI de las sedes):** usuarias finales que deben cumplir las directrices. Esperan encontrar de forma rápida y confiable los requisitos técnicos que aplican a sus procesos.
- **Docentes del Programa de Formación en Machine Learning y Data Science:** evalúan el proyecto. Esperan la aplicación correcta de la metodología TDSP, entregas semanales y resultados reproducibles.

## Aprobaciones

- [Nombre y cargo del aprobador del proyecto]
- [Firma del aprobador]
- [Fecha de aprobación]

## Referencias

- Dirección Nacional de Estrategia Digital (DNED), Universidad Nacional de Colombia. *Misión y visión*. https://web.unal.edu.co/direccion/estrategia-digital/quienes-somos/mision-y-vision
- Dirección Nacional de Estrategia Digital (DNED), Universidad Nacional de Colombia. *Directrices técnicas*. https://web.unal.edu.co/direccion/estrategia-digital/estructura-dned/directrices-tecnicas
- Universidad Nacional de Colombia, Consejo Superior Universitario. (2019, 3 de diciembre). *Acuerdo 316 de 2019*. https://legal.unal.edu.co/rlunal/home/doc.jsp?d_i=94762
