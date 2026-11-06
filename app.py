"""
Cerradura por Gestos — Miguel Ruiz
Clase 14 · Sistemas ciberfísicos: un gesto frente a la cámara, reconocido con un modelo
de Teachable Machine, abre o cierra una cerradura (ESP32 en Wokwi) por MQTT.
"""

import hashlib
import unicodedata
from datetime import datetime

import streamlit as st
from PIL import Image

from comun import configurar_pagina, encabezado, barras_probabilidad, info_items, config_mqtt, publicar_mqtt
from modelo import leer_etiquetas, cargar_modelo, clasificar

configurar_pagina("Cerradura por Gestos", "🔐")

for k, v in {"abierta": False, "historial": [], "ultima_foto": ""}.items():
    st.session_state.setdefault(k, v)

ACCIONES = {"🔓 Abrir": "Abre", "🔒 Cerrar": "Cierra", "— Ninguna": None}


def accion_por_defecto(nombre, indice):
    n = unicodedata.normalize("NFD", nombre.lower())
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    if "abr" in n or "abiert" in n or "open" in n:
        return "🔓 Abrir"
    if "cierr" in n or "cerr" in n or "close" in n:
        return "🔒 Cerrar"
    return ["🔓 Abrir", "🔒 Cerrar"][indice] if indice < 2 else "— Ninguna"


etiquetas = leer_etiquetas()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔐 Cerradura por Gestos")
    st.divider()
    broker, puerto, topicos = config_mqtt({"cerradura": "cerradura_miguelruiz"})
    topico = topicos["cerradura"]
    st.divider()
    st.markdown("### GESTOS DEL MODELO")
    st.caption("Qué hace la cerradura con cada clase de tu modelo de Teachable Machine.")
    mapa = {}
    for i, e in enumerate(etiquetas):
        opcion = st.selectbox(f"{e}:", list(ACCIONES), index=list(ACCIONES).index(accion_por_defecto(e, i)),
                              key=f"mapa_{i}")
        mapa[e] = ACCIONES[opcion]
    st.divider()
    st.markdown("### PARÁMETROS")
    umbral = st.slider("Confianza mínima", 0.0, 1.0, 0.7, 0.05,
                       help="Solo se envía el gesto si el modelo está así de seguro.")
    auto = st.toggle("Enviar automáticamente", value=True,
                     help="Al tomar la foto, envía el gesto a Wokwi sin presionar nada más.")


def enviar(gesto, origen, detalle=""):
    ok, payload, error = publicar_mqtt(broker, puerto, topico, {"gesto": gesto})
    st.session_state.historial.insert(0, {
        "hora": datetime.now().strftime("%H:%M:%S"), "gesto": gesto, "origen": origen,
        "detalle": detalle, "payload": payload, "ok": ok,
    })
    if ok:
        st.session_state.abierta = gesto == "Abre"
    return ok, error


def detalle_gesto(clase, gesto, prob):
    return f"{prob * 100:.0f}%" if clase.lower() == gesto.lower() else f"«{clase}» {prob * 100:.0f}%"


def manual(gesto):
    """Botones de control manual: se ejecutan antes de dibujar la página, así el estado se ve al instante."""
    ok, error = enviar(gesto, "botón")
    st.session_state.aviso_manual = ("success", f"Cerradura: «{gesto}»") if ok else ("error", f"No se pudo enviar: {error}")


# ─────────────────────────────────────────────
# ENCABEZADO
# ─────────────────────────────────────────────
encabezado(
    "🔐 Cerradura por Gestos",
    "Haz un gesto frente a la cámara: tu modelo lo reconoce y la cerradura del ESP32 se abre o se cierra",
    f"<b>●</b> {broker} · {topico}",
)

try:
    modelo = cargar_modelo()
except Exception as e:
    st.error(f"No se pudo cargar keras_model.h5: {e}")
    st.stop()

col_izq, col_der = st.columns([1.1, 1], gap="large")
aviso = st.session_state.pop("aviso_manual", None)
prediccion = None

with col_izq:
    with st.container(key="card_camara"):
        st.markdown("### 📸 Muestra tu gesto")
        st.markdown('<p class="sub">Ponte frente a la cámara, haz el gesto que entrenaste y toma la foto.</p>',
                    unsafe_allow_html=True)
        foto = st.camera_input("Gesto", label_visibility="collapsed")

    if foto is not None:
        imagen = Image.open(foto)
        with st.spinner("Reconociendo el gesto..."):
            probs = clasificar(modelo, imagen)
        nombres = etiquetas if len(etiquetas) == len(probs) else [f"Clase {i}" for i in range(len(probs))]
        i_max = max(range(len(probs)), key=lambda i: probs[i])
        gesto = mapa.get(nombres[i_max])
        seguro = probs[i_max] >= umbral
        prediccion = (nombres, probs, i_max, gesto, seguro)

        huella = hashlib.md5(foto.getvalue()).hexdigest()
        if huella != st.session_state.ultima_foto:
            st.session_state.ultima_foto = huella
            if auto and gesto and seguro:
                ok, error = enviar(gesto, "gesto", detalle_gesto(nombres[i_max], gesto, probs[i_max]))
                aviso = ("success", f"Gesto reconocido: {nombres[i_max]} → cerradura «{gesto}»") if ok \
                    else ("error", f"No se pudo enviar: {error}")
            elif not seguro:
                aviso = ("warning", f"No estoy seguro del gesto ({probs[i_max] * 100:.0f}%). Intenta de nuevo con mejor luz.")
            elif not gesto:
                aviso = ("info", f"«{nombres[i_max]}» no tiene acción asignada en el panel lateral.")

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        with st.container(key="card_lectura"):
            st.markdown("### 🧠 Lectura del modelo")
            st.markdown(
                f'<div class="resultado"><small>{"Gesto reconocido" if seguro else "No estoy seguro · lo más parecido"}</small>'
                f'<span>{nombres[i_max]}</span><em>{probs[i_max] * 100:.1f}%'
                f'{" → " + gesto if gesto else ""}</em></div>',
                unsafe_allow_html=True,
            )
            barras_probabilidad(nombres, probs)
            if prediccion and gesto and not auto:
                if st.button(f"ENVIAR «{gesto.upper()}» ↗", type="primary", use_container_width=True):
                    ok, error = enviar(gesto, "gesto", detalle_gesto(nombres[i_max], gesto, probs[i_max]))
                    aviso = ("success", f"Cerradura: «{gesto}»") if ok else ("error", f"No se pudo enviar: {error}")

with col_der:
    abierta = st.session_state.abierta
    with st.container(key="card_cerradura"):
        st.markdown("### 🏠 Estado de la cerradura")
        st.markdown(f"""
        <style>
            .candado {{ text-align: center; padding: 18px 10px 8px; }}
            .candado .ic {{ font-size: 4.2rem; display: block; transition: transform .3s ease; }}
            .candado b {{ display: block; font-family: 'Montserrat', sans-serif; font-size: 1.5rem; margin-top: 6px;
                          color: {'#7bd88f' if abierta else '#f2cc8f'}; }}
            .candado small {{ font-family: 'IBM Plex Mono', monospace; color: #a9c0ca; font-size: 0.78rem; }}
            .leds {{ display: flex; justify-content: center; gap: 22px; margin: 14px 0 4px; }}
            .led {{ display: flex; align-items: center; gap: 8px; font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #a9c0ca; }}
            .led i {{ width: 14px; height: 14px; border-radius: 50%; background: #24485a; display: inline-block; }}
            .led.verde.on i {{ background: #7bd88f; box-shadow: 0 0 12px #7bd88f; }}
            .led.rojo.on i {{ background: #e07a5f; box-shadow: 0 0 12px #e07a5f; }}
        </style>
        <div class="candado">
            <span class="ic">{'🔓' if abierta else '🔒'}</span>
            <b>{'ABIERTA' if abierta else 'CERRADA'}</b>
            <small>servo · pin 13 → {'180°' if abierta else '0°'}</small>
            <div class="leds">
                <span class="led verde {'on' if abierta else ''}"><i></i>pin 18</span>
                <span class="led rojo {'' if abierta else 'on'}"><i></i>pin 5</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<p class="sub" style="text-align:center;">Control manual, por si la cámara falla:</p>',
                    unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        b1.button("🔓  Abrir", type="secondary", use_container_width=True, on_click=manual, args=("Abre",))
        b2.button("🔒  Cerrar", type="secondary", use_container_width=True, on_click=manual, args=("Cierra",))

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if aviso:
        getattr(st, aviso[0])(aviso[1])

    with st.container(key="card_historial"):
        st.markdown("### 📡 Mensajes enviados")
        hist = st.session_state.historial
        if hist:
            st.markdown(f'<div class="payload">tópico: {topico}<br>{hist[0]["payload"]}</div>'
                        "<div style='height:6px'></div>", unsafe_allow_html=True)
            st.markdown("".join(
                f'<div class="freq-row"><span class="ic-row">{"🔓" if h["gesto"] == "Abre" else "🔒"}</span>'
                f'<div class="txt">{h["gesto"]}{" · " + h["detalle"] if h["detalle"] else ""}'
                f'<small>{h["hora"]} · {h["origen"]}</small></div>'
                f'<span class="{"ok" if h["ok"] else "no"}">{"✓" if h["ok"] else "✕"}</span></div>'
                for h in hist[:6]
            ), unsafe_allow_html=True)
        else:
            st.markdown('<p class="sub">Todavía no has enviado gestos.</p>', unsafe_allow_html=True)

st.divider()
hist = st.session_state.historial
m1, m2, m3, m4 = st.columns(4)
m1.metric("Gestos enviados", sum(1 for h in hist if h["ok"] and h["origen"] == "gesto"))
m2.metric("Aperturas", sum(1 for h in hist if h["ok"] and h["gesto"] == "Abre"))
m3.metric("Cierres", sum(1 for h in hist if h["ok"] and h["gesto"] == "Cierra"))
m4.metric("Clases del modelo", len(etiquetas))

with st.expander("¿Cómo funciona y cómo entreno mi propio modelo?"):
    info_items([
        ("📸", "1 · Cámara", "Tomas una foto haciendo un gesto."),
        ("🧠", "2 · Teachable Machine", "Tu modelo la clasifica (por ejemplo «Abre» o «Cierra»)."),
        ("📮", "3 · MQTT", f'La app publica {{"gesto": "Abre"}} en {broker}, tópico {topico}.'),
        ("🔌", "4 · ESP32 en Wokwi", "Recibe el mensaje y mueve el servo y los LEDs de la cerradura."),
    ])
    st.markdown("""
**Tu propio modelo:** en *teachablemachine.withgoogle.com* crea un *Proyecto de imagen*, haz una clase por gesto
(por ejemplo **Abre** = mano abierta, **Cierra** = puño) con unas 50 fotos cada una, entrena y exporta en
*Tensorflow → Keras*. Reemplaza `keras_model.h5` y `labels.txt` en GitHub: las clases aparecen solas en el panel lateral.
""")
