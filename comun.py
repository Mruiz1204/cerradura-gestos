"""
Estilo y utilidades compartidas — Miguel Ruiz
Mismo sistema visual de mis apps: azul petróleo + terracota + ámbar,
Montserrat / Inter / IBM Plex Mono.
"""

import json
import uuid

import streamlit as st
from PIL import Image


def configurar_pagina(titulo, icono):
    try:
        _icon = Image.open("logo_mr.png")
    except Exception:
        _icon = icono
    st.set_page_config(
        page_title=f"{titulo} · Miguel Ruiz",
        page_icon=_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    aplicar_estilo()


def aplicar_estilo():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background: linear-gradient(135deg, #1b3a4b 0%, #14303d 100%); }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stToolbar"] { right: 1rem; }
    .block-container { padding-top: 2.6rem !important; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #12272f !important; border-right: 1px solid #2a4b57; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #e07a5f !important; font-family: 'Montserrat', 'Inter', sans-serif !important;
        font-weight: 700 !important; font-size: 0.95rem !important;
        text-transform: uppercase !important; letter-spacing: 0.8px !important;
    }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] label p {
        color: #e8eef0 !important; font-size: 0.85rem !important; font-weight: 500 !important;
    }
    [data-testid="stSidebar"] p { color: #c4d0d6 !important; font-size: 0.88rem !important; }
    [data-testid="stSidebar"] hr { border-color: #2a4b57 !important; margin: 16px 0 !important; }

    /* Navegación entre páginas */
    [data-testid="stSidebarNav"] a, [data-testid="stSidebarNavLink"] {
        border-radius: 8px !important; margin: 2px 0 !important;
    }
    [data-testid="stSidebarNav"] a span, [data-testid="stSidebarNavLink"] span {
        color: #e8eef0 !important; font-family: 'Montserrat', 'Inter', sans-serif !important; font-weight: 600 !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"], [data-testid="stSidebarNavLink"][aria-current="page"] {
        background: #24485a !important; border-left: 3px solid #e07a5f !important;
    }
    [data-testid="stSidebarNavSeparator"] { border-color: #2a4b57 !important; }

    /* Inputs */
    textarea, input[type="text"], input[type="number"] {
        background-color: #ffffff !important; color: #111827 !important;
        font-family: 'Inter', sans-serif !important; font-size: 0.9rem !important;
    }
    [data-testid="stTextInputRootElement"], [data-testid="stNumberInputContainer"] {
        background: #ffffff !important; border: 1px solid #d1d5db !important; border-radius: 6px !important;
    }
    [data-testid="stTextInputRootElement"] input, [data-testid="stNumberInputContainer"] input { border: none !important; }
    [data-testid="stNumberInputContainer"] button { background: #f3f6f7 !important; color: #14303d !important; }
    input::placeholder { color: #6b7280 !important; }
    [data-baseweb="select"] > div, .stSelectbox [role="group"] {
        background: #ffffff !important; border: 1px solid #d1d5db !important; border-radius: 6px !important;
    }
    .stSelectbox [role="group"] input { color: #111827 !important; background: transparent !important; }

    /* Slider */
    [data-testid="stSlider"] [style*="translate(-50%"], [data-testid="stSlider"] [role="slider"] {
        background: #e07a5f !important; border-color: #e07a5f !important;
    }
    [data-testid="stSliderThumbValue"] p { color: #f2cc8f !important; font-weight: 700 !important; }
    [data-testid="stSliderTickBar"] p { color: #a9c0ca !important; }

    /* Títulos */
    h1 { font-family: 'Montserrat', 'Inter', sans-serif !important; color: #f2cc8f !important; font-weight: 700 !important; letter-spacing: -0.5px !important; }
    h2, h3 { font-family: 'Montserrat', 'Inter', sans-serif !important; color: #e07a5f !important; font-weight: 600 !important; }
    h4 { font-family: 'Montserrat', 'Inter', sans-serif !important; color: #f2cc8f !important; font-weight: 600 !important; }
    p, li { color: #e8eef0 !important; font-size: 0.95rem !important; line-height: 1.65 !important; }
    strong { color: #f2cc8f; }

    /* Botones */
    .stButton button {
        background: #e07a5f !important; color: #ffffff !important; border: none !important;
        border-radius: 6px !important; font-family: 'Montserrat', 'Inter', sans-serif !important;
        font-weight: 600 !important; font-size: 0.9rem !important; letter-spacing: 0.3px !important;
        padding: 0.6rem 1.4rem !important; width: 100% !important;
        transition: background 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stButton button p { color: #ffffff !important; font-weight: 600 !important; }
    .stButton button:hover { background: #c9583c !important; box-shadow: 0 2px 12px rgba(224,122,95,0.35) !important; }
    .stButton button[kind="secondary"] {
        background: #24485a !important; border: 1px solid rgba(242,204,143,0.2) !important;
        padding: 0.6rem 0.5rem !important; white-space: nowrap;
    }
    .stButton button[kind="secondary"]:hover { background: #2c5568 !important; box-shadow: none !important; }
    [data-testid="stDownloadButton"] button { background: #c9583c !important; color: #fff !important; border: none !important; border-radius: 6px !important; }
    [data-testid="stDownloadButton"] button p { color: #fff !important; }
    [data-testid="stPageLink"] a {
        background: #e07a5f; border-radius: 6px; padding: 0.55rem 1rem; justify-content: center;
    }
    [data-testid="stPageLink"] a:hover { background: #c9583c; }
    [data-testid="stPageLink"] a span, [data-testid="stPageLink"] a p {
        color: #ffffff !important; font-family: 'Montserrat', 'Inter', sans-serif !important; font-weight: 600 !important;
    }

    /* Métricas */
    [data-testid="stMetric"] {
        background: #1d3f4e; border: 1px solid rgba(242,204,143,0.15); border-top: 3px solid #e07a5f;
        border-radius: 12px; padding: 18px 22px; box-shadow: 0 4px 18px rgba(0,0,0,0.22);
    }
    [data-testid="stMetricLabel"] p {
        color: #a9c0ca !important; font-size: 0.78rem !important; font-weight: 600 !important;
        text-transform: uppercase !important; letter-spacing: 0.6px !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] * {
        color: #f2cc8f !important; font-weight: 700 !important; font-size: 1.35rem !important;
    }

    /* Header */
    .header-card {
        background: linear-gradient(135deg, #1d3f4e 0%, #1a3947 100%);
        border: 1px solid rgba(242,204,143,0.15); border-left: 5px solid #e07a5f;
        border-radius: 14px; padding: 28px 36px; margin-bottom: 24px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.25);
        display: flex; justify-content: space-between; align-items: center; gap: 20px; flex-wrap: wrap;
    }
    .conexion {
        background: #24485a; border: 1px solid rgba(242,204,143,0.25); border-radius: 20px;
        padding: 6px 14px; font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; color: #e8eef0;
    }
    .conexion b { color: #7bd88f; }

    /* Tarjetas: cualquier contenedor con key que empiece por "card" */
    [class*="st-key-card"] {
        background: #1d3f4e; border: 1px solid rgba(242,204,143,0.15); border-radius: 14px;
        padding: 24px 28px; box-shadow: 0 4px 18px rgba(0,0,0,0.20);
    }
    .sub { margin: -6px 0 12px !important; color: #a9c0ca !important; font-size: 0.9rem !important; }

    /* Elementos de información */
    .info-item {
        display: flex; align-items: flex-start; gap: 12px; padding: 12px 16px;
        background: #24485a; border: 1px solid rgba(242,204,143,0.12); border-radius: 10px; margin-bottom: 8px;
    }
    .info-item .ic { font-size: 1.3rem; flex-shrink: 0; }
    .info-item b { color: #f2cc8f; display: block; }
    .info-item span { color: #a9c0ca; font-size: 0.88rem; }
    .uso-tag {
        display: inline-block; background: #24485a; border: 1px solid rgba(242,204,143,0.18);
        border-radius: 20px; padding: 5px 14px; font-size: 0.85rem; font-weight: 500; color: #e8eef0; margin: 4px 3px;
    }
    .rank-tag {
        background: #14303d; border: 1px solid rgba(242,204,143,0.2); border-radius: 6px; padding: 1px 8px;
        font-size: 0.75rem; font-weight: 700; color: #f2cc8f; font-family: 'IBM Plex Mono', monospace;
    }

    /* Filas (historial, resultados) */
    .freq-row {
        display: flex; align-items: center; gap: 12px; padding: 8px 14px; margin: 4px 0;
        background: #24485a; border: 1px solid rgba(242,204,143,0.12); border-radius: 8px;
        color: #e8eef0; font-size: 0.88rem;
    }
    .freq-row .ic-row { font-size: 1.2rem; }
    .freq-row .txt { line-height: 1.3; }
    .freq-row .txt small { display: block; font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; color: #a9c0ca; }
    .freq-row .ok, .freq-row .no {
        margin-left: auto; width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center;
        font-size: 0.75rem; font-weight: 700; flex-shrink: 0;
    }
    .freq-row .ok { background: rgba(123,216,143,0.15); color: #7bd88f; }
    .freq-row .no { background: rgba(224,122,95,0.15); color: #e07a5f; }

    /* Barras de probabilidad */
    .prob { margin: 8px 0 12px; }
    .prob .fila { display: flex; justify-content: space-between; font-size: 0.88rem; color: #e8eef0; margin-bottom: 4px; }
    .prob .fila b { font-family: 'IBM Plex Mono', monospace; color: #f2cc8f; }
    .prob .barra { height: 10px; background: #24485a; border-radius: 6px; overflow: hidden; }
    .prob .barra div { height: 100%; background: linear-gradient(90deg, #e07a5f, #f2cc8f); border-radius: 6px; }
    .prob.top .fila span { color: #f2cc8f; font-weight: 700; }

    /* Resultado destacado */
    .resultado {
        background: #24485a; border: 1px solid rgba(242,204,143,0.2); border-left: 4px solid #f2cc8f;
        border-radius: 10px; padding: 16px 18px; margin: 6px 0 14px;
    }
    .resultado small {
        display: block; font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; color: #a9c0ca;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;
    }
    .resultado span { font-family: 'Montserrat', sans-serif; font-size: 1.5rem; font-weight: 700; color: #f2cc8f; }
    .resultado em { font-style: normal; color: #a9c0ca; font-size: 0.9rem; margin-left: 8px; }

    /* Estado de dispositivos */
    .dispositivos { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .disp {
        background: #24485a; border: 1px solid rgba(242,204,143,0.12); border-radius: 12px;
        padding: 18px 12px; text-align: center; transition: all 0.3s ease;
    }
    .disp .ic { font-size: 2.3rem; display: block; margin-bottom: 6px; filter: grayscale(0.9) opacity(0.55); transition: all 0.3s ease; }
    .disp b { display: block; font-family: 'Montserrat', sans-serif; color: #e8eef0; font-size: 0.92rem; }
    .disp small { font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #a9c0ca; }
    .disp.on { border-color: #f2cc8f; box-shadow: 0 0 24px rgba(242,204,143,0.25), inset 0 0 18px rgba(242,204,143,0.08); }
    .disp.on .ic { filter: none; }
    .disp.on small { color: #f2cc8f; }

    .payload {
        font-family: 'IBM Plex Mono', monospace; font-size: 0.82rem; color: #f2cc8f;
        background: #14303d; border: 1px solid rgba(242,204,143,0.15); border-radius: 8px; padding: 8px 12px;
        word-break: break-word;
    }

    /* Cámara / audio / subida */
    [data-testid="stCameraInput"], [data-testid="stAudioInput"], [data-testid="stFileUploaderDropzone"] {
        background: #24485a !important; border: 1px solid rgba(242,204,143,0.2) !important; border-radius: 12px !important;
    }
    [data-testid="stCameraInput"] *, [data-testid="stAudioInput"] *, [data-testid="stFileUploaderDropzone"] * { color: #e8eef0 !important; }
    [data-testid="stCameraInput"] button, [data-testid="stFileUploaderDropzone"] button {
        background: #e07a5f !important; border: none !important;
    }
    [data-testid="stImage"] img { border-radius: 10px; }
    [data-testid="stFileUploaderFile"], [data-testid="stFileChip"] {
        background: #14303d !important; border: 1px solid rgba(242,204,143,0.2) !important; border-radius: 8px !important;
    }
    [data-testid="stFileUploaderFileName"], [data-testid="stFileUploaderFile"] * { color: #e8eef0 !important; }

    [data-testid="stTabs"] button p { font-family: 'Montserrat', 'Inter', sans-serif !important; font-weight: 600 !important; color: #a9c0ca !important; }
    [data-testid="stTabs"] button[aria-selected="true"] p { color: #f2cc8f !important; }
    [data-testid="stAlert"] { border-radius: 10px !important; }
    div[data-testid="stExpander"] { border: 1px solid rgba(242,204,143,0.15) !important; border-radius: 12px !important; background: #1d3f4e !important; }
    hr { border-color: rgba(242,204,143,0.15) !important; }
    .stMarkdown code, p code {
        background: #14303d !important; color: #f2cc8f !important; border: 1px solid rgba(242,204,143,0.15);
        border-radius: 5px; padding: 1px 6px; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


def encabezado(titulo, subtitulo, etiqueta=""):
    tag = f'<span class="conexion">{etiqueta}</span>' if etiqueta else ""
    st.markdown(f"""
<div class="header-card">
    <div>
        <p style="margin:0 0 4px 0; color:#e07a5f !important; font-family:'Montserrat',sans-serif; font-weight:700; font-size:1.1rem;">Miguel Ruiz</p>
        <h1 style="margin:0; font-size:1.9rem; color:#f2cc8f !important;">{titulo}</h1>
        <p style="margin:6px 0 0 0; color:#a9c0ca !important; font-size:0.97rem;">{subtitulo}</p>
    </div>
    {tag}
</div>
""", unsafe_allow_html=True)


def mostrar_imagen(imagen, pie=""):
    """Muestra una imagen (PIL o arreglo RGB) incrustada en base64.
    Evita el servidor de archivos de Streamlit, que a veces deja la imagen rota en Streamlit Cloud."""
    import base64
    import io

    import numpy as np

    if not isinstance(imagen, Image.Image):
        imagen = Image.fromarray(np.ascontiguousarray(imagen).astype("uint8"))
    imagen = imagen.convert("RGB")
    imagen.thumbnail((1280, 1280))
    buf = io.BytesIO()
    imagen.save(buf, format="JPEG", quality=88)
    b64 = base64.b64encode(buf.getvalue()).decode()
    texto = f'<p class="sub" style="text-align:center; margin-top:6px !important;">{pie}</p>' if pie else ""
    st.markdown(f'<img src="data:image/jpeg;base64,{b64}" style="width:100%; border-radius:10px;">{texto}',
                unsafe_allow_html=True)


def subtitulo(texto):
    st.markdown(f'<p class="sub">{texto}</p>', unsafe_allow_html=True)


def info_items(items):
    """items: lista de (icono, título, descripción)."""
    st.markdown("".join(
        f'<div class="info-item"><span class="ic">{ic}</span><div><b>{t}</b><span>{d}</span></div></div>'
        for ic, t, d in items
    ), unsafe_allow_html=True)


def barras_probabilidad(etiquetas, probs):
    orden = sorted(zip(etiquetas, probs), key=lambda x: -x[1])
    html = ""
    for i, (et, p) in enumerate(orden):
        html += (f'<div class="prob {"top" if i == 0 else ""}"><div class="fila"><span>{et}</span>'
                 f'<b>{p * 100:.1f}%</b></div><div class="barra"><div style="width:{p * 100:.1f}%"></div></div></div>')
    st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MQTT
# ─────────────────────────────────────────────
def publicar_mqtt(broker, puerto, topico, datos):
    """Publica un diccionario como JSON. Devuelve (ok, payload, error)."""
    import paho.mqtt.client as mqtt

    payload = json.dumps(datos, ensure_ascii=False)
    client_id = f"app-miguelruiz-{uuid.uuid4().hex[:6]}"
    try:
        try:
            cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        except AttributeError:  # paho-mqtt 1.x
            cliente = mqtt.Client(client_id=client_id)
        cliente.connect(broker, int(puerto), keepalive=30)
        cliente.loop_start()
        info = cliente.publish(topico, payload, qos=1)
        info.wait_for_publish(timeout=5)
        cliente.loop_stop()
        cliente.disconnect()
        ok = info.is_published()
        return ok, payload, None if ok else "El broker no confirmó la publicación."
    except Exception as e:
        return False, payload, str(e)


def config_mqtt(topicos):
    """Panel lateral de conexión. topicos: dict nombre -> valor por defecto.
    Los valores se guardan en session_state para compartirlos entre páginas."""
    defaults = {"cfg_broker": "broker.mqttdashboard.com", "cfg_puerto": 1883}
    defaults.update({f"cfg_top_{k}": v for k, v in topicos.items()})
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

    def guardar(origen, destino):
        st.session_state[destino] = st.session_state[origen]

    st.markdown("### CONEXIÓN MQTT")
    st.text_input("Broker:", value=st.session_state.cfg_broker, key="w_broker",
                  on_change=guardar, args=("w_broker", "cfg_broker"))
    st.number_input("Puerto:", value=int(st.session_state.cfg_puerto), step=1, key="w_puerto",
                    on_change=guardar, args=("w_puerto", "cfg_puerto"))
    for k in topicos:
        st.text_input(f"Tópico {k}:", value=st.session_state[f"cfg_top_{k}"], key=f"w_top_{k}",
                      on_change=guardar, args=(f"w_top_{k}", f"cfg_top_{k}"),
                      help="Debe ser el mismo tópico al que se suscribe el ESP32 en Wokwi.")
    return st.session_state.cfg_broker, int(st.session_state.cfg_puerto), {
        k: st.session_state[f"cfg_top_{k}"] for k in topicos
    }
