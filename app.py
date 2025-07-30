from flask import Flask, request, jsonify, render_template
import os
import json
from datetime import datetime
from ml_model import PhishingDetector
from database import Database

app = Flask(__name__)
detector = PhishingDetector()
db = Database()

# Inicializar modelo
if not detector.load_model():
    print("Entrenando nuevo modelo...")
    detector.train_model()
else:
    print("Modelo cargado exitosamente")

@app.route('/')
def dashboard():
    """Dashboard principal"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_url():
    """API para analizar URLs"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL es requerida'}), 400
        
        # Analizar URL
        result = detector.predict(url)
        
        # Guardar en base de datos
        user_agent = request.headers.get('User-Agent')
        ip_address = request.remote_addr
        db.save_analysis(url, result, user_agent, ip_address)
        
        # Agregar recomendaciones
        result['recommendations'] = get_security_recommendations(result)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """API para obtener estadísticas"""
    try:
        stats = db.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """API para analizar múltiples URLs"""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if not urls:
            return jsonify({'error': 'Lista de URLs es requerida'}), 400
        
        results = []
        for url in urls:
            result = detector.predict(url)
            result['url'] = url
            result['recommendations'] = get_security_recommendations(result)
            
            # Guardar en base de datos
            user_agent = request.headers.get('User-Agent')
            ip_address = request.remote_addr
            db.save_analysis(url, result, user_agent, ip_address)
            
            results.append(result)
        
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_security_recommendations(result):
    """Genera recomendaciones de seguridad basadas en el análisis"""
    recommendations = []
    
    if result['is_phishing']:
        recommendations.extend([
            "⚠️ NO ingreses datos personales en este sitio",
            "🚫 NO hagas clic en enlaces sospechosos",
            "🔒 Verifica la URL oficial del servicio",
            "📞 Contacta directamente a la empresa si es necesario",
            "🛡️ Usa un antivirus actualizado"
        ])
    else:
        if result['risk_score'] > 30:
            recommendations.extend([
                "⚡ Sitio con riesgo moderado, procede con cautela",
                "🔍 Verifica que sea el sitio oficial",
                "🔒 Asegúrate de que use HTTPS"
            ])
        else:
            recommendations.append("✅ Sitio aparentemente seguro")
    
    return recommendations

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)