# 🔐 Cerradura por Gestos — Miguel Ruiz

Sistema ciberfísico del curso *Creación de Interfaces Multimodales* (Clase 14).
Haces un gesto frente a la cámara, un modelo de **Teachable Machine** lo reconoce y la app publica por **MQTT**
la orden para que un **ESP32 en Wokwi** abra o cierre la cerradura.

```
Cámara → Teachable Machine → {"gesto": "Abre"} → broker.mqttdashboard.com (cerradura_miguelruiz) → ESP32 en Wokwi
```

| Gesto | ESP32 |
|---|---|
| Abre | Servo (pin 13) a 180°, LED pin 18 encendido |
| Cierra | Servo a 0°, LED pin 5 encendido |

- Cada clase del modelo se puede asignar a *Abrir*, *Cerrar* o *Ninguna* desde el panel lateral.
- Envío automático con umbral de confianza, y botones manuales de respaldo.
- Código del ESP32 en [`wokwi/sketch.ino`](wokwi/sketch.ino) para el proyecto https://wokwi.com/projects/377066087789108225

## Tu propio modelo
En Teachable Machine crea una clase por gesto (p. ej. **Abre** = mano abierta, **Cierra** = puño), entrena,
exporta en *Tensorflow → Keras* y reemplaza `keras_model.h5` y `labels.txt`.

## Desplegar en Streamlit Cloud
Archivo principal `app.py` y **Python 3.11** en *Advanced settings*.
