# 🛡️ Phishing Detector AI

Detector de **URLs de phishing** usando **Machine Learning (Random Forest)** integrado con **Flask** y una base de datos **SQLite** para almacenar resultados y estadísticas.

## 📌 Características principales

- 🔍 **Análisis de URLs en tiempo real** con modelo entrenado.
- 🤖 **Modelo de Machine Learning** basado en Random Forest.
- 🧩 **Extracción de características (features)** de URLs (longitud, dominios, HTTPS, palabras sospechosas, etc.).
- 📊 **Dashboard** con estadísticas y análisis recientes.
- 💾 **Almacenamiento en SQLite** de resultados, con IP y User-Agent del cliente.
- 🛡️ **Recomendaciones automáticas de seguridad** según el nivel de riesgo detectado.
- 🚀 **API REST** lista para integrarse con otras aplicaciones.

---

## 📂 Estructura del Proyecto

phishing-detector-ai/
│
├── app.py              # Servidor Flask (rutas y APIs)
├── ml_model.py         # Entrenamiento y predicción con Random Forest
├── url_analyzer.py     # Extracción de características de las URLs
├── db.py               # Conexión y operaciones en SQLite
├── templates/
│   └── index.html      # Dashboard principal
├── data/
│   └── model.pkl       # Modelo entrenado (se genera tras entrenar)
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación del proyecto

---

##🛠️ Tecnologías Utilizadas
	•	Python 3
	•	Flask
	•	scikit-learn
	•	pandas
	•	NumPy
	•	tldextract
	•	SQLite3
---

## ⚙️ Instalación y Configuración

1. Clonar el repositorio:

```bash
git clone https://github.com/javiermoya2504/phishing-detector-ai
cd phishing-detector-ai
```

🏋️ Entrenamiento del Modelo
Ejecuta este comando para entrenar el modelo y generar data/model.pkl:
```bash
python -c "from ml_model import PhishingDetector; detector = PhishingDetector(); detector.train_model()"
```

Salida esperada (ejemplo):

Creando datos de entrenamiento...
Dividiendo datos en entrenamiento y prueba...
Entrenando modelo...
Evaluando modelo...
Precisión del modelo: 1.00

⚠️ Nota: La precisión es 1.00 porque el dataset inicial es pequeño y simulado.
Para producción se recomienda usar un dataset real (ejemplo: PhishTank).


