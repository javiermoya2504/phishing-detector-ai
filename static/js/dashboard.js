// Variables globales
let isAnalyzing = false;

// Inicializar dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadStatistics();
    
    // Event listener para Enter en el input
    document.getElementById('urlInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            analyzeURL();
        }
    });
    
    // Actualizar estadísticas cada 30 segundos
    setInterval(loadStatistics, 30000);
});

// Función para analizar URL
async function analyzeURL() {
    if (isAnalyzing) return;
    
    const urlInput = document.getElementById('urlInput');
    const resultDiv = document.getElementById('result');
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Por favor ingresa una URL válida');
        return;
    }
    
    // Validar formato de URL
    if (!isValidURL(url)) {
        showError('Por favor ingresa una URL válida (debe incluir http:// o https://)');
        return;
    }
    
    isAnalyzing = true;
    const button = document.querySelector('button');
    const originalText = button.textContent;
    button.innerHTML = '<span class="loading"></span>Analizando...';
    button.disabled = true;
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResult(data, url);
            loadStatistics(); // Actualizar estadísticas
        } else {
            showError(data.error || 'Error al analizar la URL');
        }
        
    } catch (error) {
        showError('Error de conexión: ' + error.message);
    } finally {
        isAnalyzing = false;
        button.textContent = originalText;
        button.disabled = false;
    }
}

// Función para validar URL
function isValidURL(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// Función para mostrar resultados
function displayResult(data, url) {
    const resultDiv = document.getElementById('result');
    const isPhishing = data.is_phishing;
    const riskScore = Math.round(data.risk_score);
    const confidence = Math.round(data.confidence * 100);
    
    let resultClass, statusIcon, statusText, riskClass;
    
    if (isPhishing) {
        resultClass = 'danger';
        statusIcon = '🚨';
        statusText = 'SITIO PELIGROSO';
        riskClass = 'risk-high';
    } else if (riskScore > 30) {
        resultClass = 'warning';
        statusIcon = '⚠️';
        statusText = 'RIESGO MODERADO';
        riskClass = 'risk-medium';
    } else {
        resultClass = 'safe';
        statusIcon = '✅';
        statusText = 'SITIO SEGURO';
        riskClass = 'risk-low';
    }
    
    const recommendationsHTML = data.recommendations
        .map(rec => `<li>${rec}</li>`)
        .join('');
    
    resultDiv.className = `result ${resultClass}`;
    resultDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div>
                <h3>${statusIcon} ${statusText}</h3>
                <p style="margin: 5px 0; word-break: break-all;"><strong>URL:</strong> ${url}</p>
            </div>
            <div style="text-align: right;">
                <div class="risk-badge ${riskClass}">
                    Riesgo: ${riskScore}%
                </div>
                <div style="margin-top: 5px; font-size: 0.9em; color: #666;">
                    Confianza: ${confidence}%
                </div>
            </div>
        </div>
        
        <div class="recommendations">
            <h4>📋 Recomendaciones:</h4>
            <ul>${recommendationsHTML}</ul>
        </div>
    `;
    
    resultDiv.classList.remove('hidden');
    resultDiv.scrollIntoView({ behavior: 'smooth' });
}

// Función para mostrar errores
function showError(message) {
    const resultDiv = document.getElementById('result');
    resultDiv.className = 'result danger';
    resultDiv.innerHTML = `
        <h3>❌ Error</h3>
        <p>${message}</p>
    `;
    resultDiv.classList.remove('hidden');
}

// Función para cargar estadísticas
async function loadStatistics() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (response.ok) {
            updateStatistics(data);
            updateRecentScans(data.recent_scans);
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Función para actualizar estadísticas
function updateStatistics(stats) {
    document.getElementById('totalScans').textContent = stats.total_scans;
    document.getElementById('phishingDetected').textContent = stats.phishing_detected;
    document.getElementById('legitimateUrls').textContent = stats.legitimate_urls;
    document.getElementById('avgRiskScore').textContent = stats.average_risk_score + '%';
}

// Función para actualizar análisis recientes
function updateRecentScans(recentScans) {
    const container = document.getElementById('recentScans');
    
    if (!recentScans || recentScans.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #666;">No hay análisis recientes</p>';
        return;
    }
    
    const scansHTML = recentScans.map(scan => {
        const [url, isPhishing, riskScore, timestamp] = scan;
        const risk = Math.round(riskScore);
        let riskClass, statusIcon;
        
        if (isPhishing) {
            riskClass = 'risk-high';
            statusIcon = '🚨';
        } else if (risk > 30) {
            riskClass = 'risk-medium';
            statusIcon = '⚠️';
        } else {
            riskClass = 'risk-low';
            statusIcon = '✅';
        }
        
        const date = new Date(timestamp).toLocaleString('es-ES');
        
        return `
            <div class="recent-item">
                <div class="url-info">
                    <div class="url-text">${statusIcon} ${url}</div>
                    <div class="url-meta">${date}</div>
                </div>
                <div class="risk-badge ${riskClass}">
                    ${risk}%
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = scansHTML;
}