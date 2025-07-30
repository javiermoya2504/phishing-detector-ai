document.addEventListener('DOMContentLoaded', function() {
    const statusDiv = document.getElementById('status');
    const urlDiv = document.getElementById('urlDisplay');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    // Obtener la URL actual
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        const currentUrl = tabs[0].url;
        urlDiv.textContent = currentUrl;
        
        // Analizar automáticamente
        analyzeCurrentSite(currentUrl);
    });
    
    analyzeBtn.addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            analyzeCurrentSite(tabs[0].url);
        });
    });
    
    async function analyzeCurrentSite(url) {
        statusDiv.className = 'status loading';
        statusDiv.textContent = 'Analizando sitio...';
        
        try {
            const response = await fetch('http://localhost:5000/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                displayResult(data);
            } else {
                showError(data.error || 'Error al analizar');
            }
        } catch (error) {
            showError('Error de conexión');
        }
    }
    
    function displayResult(data) {
        const riskScore = Math.round(data.risk_score);
        
        if (data.is_phishing) {
            statusDiv.className = 'status danger';
            statusDiv.innerHTML = `🚨 SITIO PELIGROSO<br>Riesgo: ${riskScore}%`;
        } else if (riskScore > 30) {
            statusDiv.className = 'status warning';
            statusDiv.innerHTML = `⚠️ RIESGO MODERADO<br>Riesgo: ${riskScore}%`;
        } else {
            statusDiv.className = 'status safe';
            statusDiv.innerHTML = `✅ SITIO SEGURO<br>Riesgo: ${riskScore}%`;
        }
    }
    
    function showError(message) {
        statusDiv.className = 'status danger';
        statusDiv.textContent = `❌ ${message}`;
    }
});