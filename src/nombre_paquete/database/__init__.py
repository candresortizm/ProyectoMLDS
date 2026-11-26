"""Adquisición y carga del corpus de Directrices Técnicas de la DNED."""

from .acquisition import URLS, descargar_directrices
from .extraction import cargar_corpus, extraer_corpus, extraer_texto

__all__ = ["URLS", "descargar_directrices", "extraer_corpus", "extraer_texto", "cargar_corpus"]
