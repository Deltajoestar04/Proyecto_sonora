
document.addEventListener('DOMContentLoaded', function() {


    const realtimeCardsContainer = document.getElementById('realtime-cards');

    if (realtimeCardsContainer) {

        function fetchAndRenderData() {
            fetch('/api/realtime_data/')
                .then(response => response.json())
                .then(data => {
                    realtimeCardsContainer.innerHTML = '';

                    const keys = Object.keys(data);
                    if (keys.length === 0) {
                        realtimeCardsContainer.innerHTML = `
                            <div class="col-12 text-center py-5">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Cargando...</span>
                                </div>
                                <p class="mt-2">Esperando datos MQTT en el tópico **sonora/#**...</p>
                            </div>
                        `;
                        return;
                    }

                    keys.forEach(key => {
                        const sensorData = data[key];
                        const { municipio, tipo_dato, value, timestamp } = sensorData;

                        let unit = '';
                        let colorClass = 'text-secondary';

                        if (tipo_dato.toLowerCase().includes('temp')) {
                            unit = '°C';
                            colorClass = 'text-danger';
                        } else if (tipo_dato.toLowerCase().includes('humedad')) {
                            unit = '%';
                            colorClass = 'text-info';
                        } else if (tipo_dato.toLowerCase().includes('luz') || tipo_dato.toLowerCase().includes('iluminacion')) {
                            unit = 'lux';
                            colorClass = 'text-warning';
                        }

                     
                        let cleanedMunicipio = municipio.replace(/[^\x00-\x7F]/g, "").trim();
                        cleanedMunicipio = cleanedMunicipio.charAt(0).toUpperCase() + cleanedMunicipio.slice(1);

                        const cardHtml = `
                            <div class="col">
                                <div class="card shadow-sm h-100">
                                    <div class="card-body">
                                        <h5 class="card-title">${cleanedMunicipio}</h5>
                                        <h6 class="card-subtitle mb-2 text-muted">${tipo_dato.charAt(0).toUpperCase() + tipo_dato.slice(1)}</h6>
                                        <p class="display-4 ${colorClass} fw-bold">${parseFloat(value).toFixed(2)}${unit}</p>
                                        <p class="card-text"><small class="text-muted">Actualizado: ${new Date(timestamp).toLocaleTimeString()}</small></p>
                                    </div>
                                </div>
                            </div>
                        `;
                        realtimeCardsContainer.innerHTML += cardHtml;
                    });

                })
                .catch(error => {
                    console.error('Error al obtener datos en tiempo real:', error);
                    realtimeCardsContainer.innerHTML = '<p class="text-danger w-100 text-center">Error al conectar con la API de datos en tiempo real.</p>';
                });
        }

        fetchAndRenderData();
        setInterval(fetchAndRenderData, 3000);
    }


    if (document.getElementById('historialChart')) {
        const chartCtx = document.getElementById('historialChart').getContext('2d');
        const chartDataElement = document.getElementById('chart-data');

        let rawData = [];
        if (chartDataElement) {
            const jsonText = chartDataElement.textContent;
            try {
                rawData = JSON.parse(jsonText);
            } catch (e) {
                console.error("🚨 ERROR AL PARSEAR DATOS JSON DEL HISTORIAL:", e);
                chartCtx.canvas.parentNode.innerHTML = '<p class="text-center text-danger">🚨 Error al procesar datos para la gráfica. Verifique la serialización de datos en views.py.</p>';
                return;
            }
        }

        const groupedData = rawData.reduce((acc, item) => {
            if (!item.tipo_dato || item.value === undefined) return acc;

            const tipo = item.tipo_dato.toLowerCase();
            if (!acc[tipo]) {
                acc[tipo] = {
                    labels: [],
                    data: [],
                };
            }

            acc[tipo].labels.unshift(new Date(item.timestamp).toLocaleTimeString());
            acc[tipo].data.unshift(item.value);
            return acc;
        }, {});

        const datasets = Object.keys(groupedData).map((type, index) => {
            const colors = ['#dc3545', '#007bff', '#ffc107', '#28a745', '#6f42c1', '#fd7e14'];

            return {
                label: type.charAt(0).toUpperCase() + type.slice(1),
                data: groupedData[type].data,
                borderColor: colors[index % colors.length],
                backgroundColor: colors[index % colors.length] + '40',
                fill: false,
                tension: 0.3
            };
        });

        if (datasets.length > 0 && groupedData[Object.keys(groupedData)[0]].labels.length > 0) {
            new Chart(chartCtx, {
                type: 'line',
                data: {
                    labels: groupedData[Object.keys(groupedData)[0]].labels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Tendencia Histórica de Sensores'
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Tiempo (Últimas horas)'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Valor Registrado'
                            }
                        }
                    }
                }
            });
        } else {
            chartCtx.canvas.parentNode.innerHTML = '<p class="text-center text-muted">No hay suficientes datos históricos para generar la gráfica.</p>';
        }
    }
});