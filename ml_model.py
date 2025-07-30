import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
from url_analyzer import URLAnalyzer

class PhishingDetector:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.analyzer = URLAnalyzer()
        self.feature_names = [
            'url_length', 'num_dots', 'num_hyphens', 'num_underscores',
            'num_slashes', 'num_questionmarks', 'num_equal', 'num_at',
            'num_and', 'num_exclamation', 'num_space', 'num_tilde',
            'num_comma', 'num_plus', 'num_asterisk', 'num_hashtag',
            'num_dollar', 'num_percent', 'domain_length', 'subdomain_length',
            'tld_length', 'suspicious_words', 'has_ip', 'is_https',
            'num_subdomains', 'is_shortened'
        ]
    
    def create_sample_data(self):
        """Crea datos de muestra para entrenamiento"""
        # URLs legítimas
        legitimate_urls = [
            "https://www.google.com",
            "https://www.facebook.com",
            "https://www.amazon.com",
            "https://www.microsoft.com",
            "https://www.apple.com",
            "https://www.github.com",
            "https://www.stackoverflow.com",
            "https://www.wikipedia.org",
            "https://www.youtube.com",
            "https://www.twitter.com",
            "https://www.linkedin.com",
            "https://www.instagram.com",
            "https://www.reddit.com",
            "https://www.netflix.com",
            "https://www.spotify.com"
        ]
        
        # URLs de phishing (simuladas)
        phishing_urls = [
            "http://secure-amazon-update.com/verify",
            "https://paypal-security-check.net/login",
            "http://microsoft-account-verify.org/update",
            "https://google-security-alert.com/confirm",
            "http://facebook-security-team.net/verify",
            "https://apple-id-locked.com/unlock",
            "http://banking-security-update.org/login",
            "https://account-verification-required.net/verify",
            "http://urgent-security-notice.com/update",
            "https://confirm-your-identity-now.org/verify",
            "http://192.168.1.100/phishing",
            "https://bit.ly/fake-bank-login",
            "http://account-suspended-verify-now.com",
            "https://immediate-action-required.net/login",
            "http://security-breach-update-account.org"
        ]
        
        # Crear dataset
        data = []
        labels = []
        
        # Procesar URLs legítimas
        for url in legitimate_urls:
            features = self.analyzer.extract_features(url)
            data.append([features[name] for name in self.feature_names])
            labels.append(0)  # 0 = legítimo
        
        # Procesar URLs de phishing
        for url in phishing_urls:
            features = self.analyzer.extract_features(url)
            data.append([features[name] for name in self.feature_names])
            labels.append(1)  # 1 = phishing
        
        return np.array(data), np.array(labels)
    
    def train_model(self):
        """Entrena el modelo con datos de muestra"""
        print("Creando datos de entrenamiento...")
        X, y = self.create_sample_data()
        
        print("Dividiendo datos en entrenamiento y prueba...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print("Entrenando modelo...")
        self.model.fit(X_train, y_train)
        
        print("Evaluando modelo...")
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Precisión del modelo: {accuracy:.2f}")
        print("\nReporte de clasificación:")
        print(classification_report(y_test, y_pred, target_names=['Legítimo', 'Phishing']))
        
        # Guardar modelo
        os.makedirs('data', exist_ok=True)
        joblib.dump(self.model, 'data/model.pkl')
        print("Modelo guardado en data/model.pkl")
    
    def load_model(self):
        """Carga el modelo entrenado"""
        if os.path.exists('data/model.pkl'):
            self.model = joblib.load('data/model.pkl')
            return True
        return False
    
    def predict(self, url):
        """Predice si una URL es phishing"""
        features = self.analyzer.extract_features(url)
        feature_vector = np.array([[features[name] for name in self.feature_names]])
        
        prediction = self.model.predict(feature_vector)[0]
        probability = self.model.predict_proba(feature_vector)[0]
        
        return {
            'is_phishing': bool(prediction),
            'confidence': float(max(probability)),
            'risk_score': float(probability[1]) * 100,  # Probabilidad de phishing en %
            'features': features
        }