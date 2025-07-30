import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_path='phish_detector.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de análisis de URLs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS url_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                is_phishing BOOLEAN NOT NULL,
                confidence REAL NOT NULL,
                risk_score REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_agent TEXT,
                ip_address TEXT
            )
        ''')
        
        # Tabla de estadísticas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                total_scans INTEGER DEFAULT 0,
                phishing_detected INTEGER DEFAULT 0,
                legitimate_detected INTEGER DEFAULT 0,
                avg_risk_score REAL DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_analysis(self, url, result, user_agent=None, ip_address=None):
        """Guarda el resultado de un análisis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO url_analysis 
            (url, is_phishing, confidence, risk_score, user_agent, ip_address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            url,
            result['is_phishing'],
            result['confidence'],
            result['risk_score'],
            user_agent,
            ip_address
        ))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self):
        """Obtiene estadísticas generales"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total de análisis
        cursor.execute('SELECT COUNT(*) FROM url_analysis')
        total_scans = cursor.fetchone()[0]
        
        # Phishing detectado
        cursor.execute('SELECT COUNT(*) FROM url_analysis WHERE is_phishing = 1')
        phishing_count = cursor.fetchone()[0]
        
        # URLs legítimas
        cursor.execute('SELECT COUNT(*) FROM url_analysis WHERE is_phishing = 0')
        legitimate_count = cursor.fetchone()[0]
        
        # Puntuación promedio de riesgo
        cursor.execute('SELECT AVG(risk_score) FROM url_analysis')
        avg_risk = cursor.fetchone()[0] or 0
        
        # URLs más analizadas
        cursor.execute('''
            SELECT url, COUNT(*) as count 
            FROM url_analysis 
            GROUP BY url 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        top_urls = cursor.fetchall()
        
        # Análisis recientes
        cursor.execute('''
            SELECT url, is_phishing, risk_score, timestamp 
            FROM url_analysis 
            ORDER BY timestamp DESC 
            LIMIT 20
        ''')
        recent_scans = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_scans': total_scans,
            'phishing_detected': phishing_count,
            'legitimate_urls': legitimate_count,
            'average_risk_score': round(avg_risk, 2),
            'top_urls': top_urls,
            'recent_scans': recent_scans
        }