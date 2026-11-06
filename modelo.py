"""Carga del modelo de Teachable Machine y sus etiquetas."""

import os

import numpy as np
import streamlit as st
from PIL import Image, ImageOps


def leer_etiquetas(ruta="labels.txt"):
    """labels.txt de Teachable Machine: una clase por línea, con formato '0 Nombre'."""
    if not os.path.exists(ruta):
        return []
    etiquetas = []
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                partes = linea.split(" ", 1)
                etiquetas.append(partes[1] if len(partes) == 2 and partes[0].isdigit() else linea)
    return etiquetas


@st.cache_resource(show_spinner="Cargando el modelo de Teachable Machine...")
def cargar_modelo(ruta="keras_model.h5"):
    from tensorflow.keras.models import load_model
    return load_model(ruta, compile=False)


def clasificar(modelo, imagen):
    """Mismo preprocesamiento que exporta Teachable Machine: recorte central 224×224 y valores en [-1, 1]."""
    img = ImageOps.fit(imagen.convert("RGB"), (224, 224), Image.Resampling.LANCZOS)
    datos = (np.asarray(img, dtype=np.float32) / 127.5) - 1
    pred = modelo.predict(datos[np.newaxis, ...], verbose=0)[0]
    return [float(p) for p in pred]
