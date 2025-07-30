#Instalacióny configuración: 
1. git clone https://github.com/SamuelVeytia/phish-detector-ai
2. cd phish-detector-ai
3. python -m venv venv
4. venv\Scripts\activate
5. pip install -r requirements.txt
6. Verificar instalación de requerimientos con pip list

#Entrenar el modelo:

7. python -c "from ml_model import PhishingDetector; detector = PhishingDetector();detector.train_model()"

#Ejecutar la aplicación:
8.python app.py

#Probar la app (localhost):

http://127.0.0.1:5000

http://192.168.0.13:5000
