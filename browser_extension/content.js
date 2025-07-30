// Script que se ejecuta en todas las páginas web
(function() {
    // Verificar si ya se ejecutó
    if (window.phishDetectorLoaded) return;
    window.phishDetectorLoaded = true;
    
    // Analizar la página actual al cargar
    setTimeout(function() {
        analyzeCurrentPage();
    }, 2000);
    
    async function analyzeCurrentPage() {
        const currentUrl = window.location.href;
        
        try {
            const response = await fetch('http://localhost:5000/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: currentUrl })
            });
            
            const data = await response.json();
            
            if (response.ok && data.is_phishing) {
                showPhishingWarning(data);
            }
        } catch (error) {
            console.log('Phish Detector: Error checking URL');
        }
    }
    
    function showPhishingWarning(data) {
        // Crear overlay de advertencia
        const overlay = document.createElement('div');
        overlay.id = 'phish-detector-warning';
        overlay.innerHTML = `
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.8);
                z-index: 999999;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
            ">
                <div style="
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    max-width: 500px;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                ">
                    <h2 style="color: #dc3545; margin-bottom: 20px;">
                        🚨 ¡ADVERTENCIA DE SEGURIDAD!
                    </h2>
                    <p style="margin-bottom: 20px; font-size: 16px;">
                        Este sitio ha sido identificado como potencialmente peligroso.
                        <br><strong>Riesgo: ${Math.round(data.risk_score)}%</strong>
                    </p>
                    <div style="margin-bottom: 20px; text-align: left;">
                        <strong>Recomendaciones:</strong>
                        <ul style="margin-top: 10px;">
                            ${data.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>
                    <div style="display: flex; gap: 10px; justify-content: center;">
                        <button onclick="this.parentElement.parentElement.parentElement.parentElement.remove()" 
                                style="padding: 10px 20px; background: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">
                            Continuar (No recomendado)
                        </button>
                        <button onclick="window.close()" 
                                style="padding: 10px 20px; background: #dc3545; color: white; border: none; border-radius: 5px; cursor: pointer;">
                            Cerrar Pestaña
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(overlay);
    }
})();