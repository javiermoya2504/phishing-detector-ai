import re
import requests
from urllib.parse import urlparse
import tldextract
import socket
from datetime import datetime

class URLAnalyzer:
    def __init__(self):
        self.suspicious_keywords = [
            'secure', 'account', 'update', 'confirm', 'verify', 'login',
            'banking', 'paypal', 'amazon', 'microsoft', 'google'
        ]
    
    def extract_features(self, url):
        """Extrae características de una URL para el modelo ML"""
        features = {}
        
        try:
            parsed = urlparse(url)
            extracted = tldextract.extract(url)
            
            # Características básicas de URL
            features['url_length'] = len(url)
            features['num_dots'] = url.count('.')
            features['num_hyphens'] = url.count('-')
            features['num_underscores'] = url.count('_')
            features['num_slashes'] = url.count('/')
            features['num_questionmarks'] = url.count('?')
            features['num_equal'] = url.count('=')
            features['num_at'] = url.count('@')
            features['num_and'] = url.count('&')
            features['num_exclamation'] = url.count('!')
            features['num_space'] = url.count(' ')
            features['num_tilde'] = url.count('~')
            features['num_comma'] = url.count(',')
            features['num_plus'] = url.count('+')
            features['num_asterisk'] = url.count('*')
            features['num_hashtag'] = url.count('#')
            features['num_dollar'] = url.count('$')
            features['num_percent'] = url.count('%')
            
            # Características del dominio
            features['domain_length'] = len(extracted.domain) if extracted.domain else 0
            features['subdomain_length'] = len(extracted.subdomain) if extracted.subdomain else 0
            features['tld_length'] = len(extracted.suffix) if extracted.suffix else 0
            
            # Palabras sospechosas
            features['suspicious_words'] = sum(1 for word in self.suspicious_keywords if word in url.lower())
            
            # IP en lugar de dominio
            features['has_ip'] = 1 if self._is_ip_address(parsed.netloc) else 0
            
            # HTTPS
            features['is_https'] = 1 if parsed.scheme == 'https' else 0
            
            # Subdominios múltiples
            features['num_subdomains'] = url.count('.') - 1 if extracted.suffix else url.count('.')
            
            # URL acortada
            features['is_shortened'] = 1 if self._is_shortened_url(extracted.domain) else 0
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            # Valores por defecto en caso de error
            for key in ['url_length', 'num_dots', 'num_hyphens', 'num_underscores', 
                       'num_slashes', 'num_questionmarks', 'num_equal', 'num_at',
                       'num_and', 'num_exclamation', 'num_space', 'num_tilde',
                       'num_comma', 'num_plus', 'num_asterisk', 'num_hashtag',
                       'num_dollar', 'num_percent', 'domain_length', 'subdomain_length',
                       'tld_length', 'suspicious_words', 'has_ip', 'is_https',
                       'num_subdomains', 'is_shortened']:
                features[key] = 0
        
        return features
    
    def _is_ip_address(self, netloc):
        """Verifica si es una dirección IP"""
        try:
            socket.inet_aton(netloc)
            return True
        except socket.error:
            return False
    
    def _is_shortened_url(self, domain):
        """Verifica si es una URL acortada"""
        shortened_domains = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly']
        return domain in shortened_domains if domain else False