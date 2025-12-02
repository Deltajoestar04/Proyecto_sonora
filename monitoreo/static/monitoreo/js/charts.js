// monitoreo/static/monitoreo/js/charts.js

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
                                <div class="spinner-border text-primary" role="status"></div>
                                <p class="mt-2">Esperando datos MQTT en el tópico **sonora/#**...</p>                            </div>`;
                        return;
                    }

                    keys.forEach(key => {
                        const { municipio, tipo_dato, value, timestamp } = data[key];

                        let unit = '';
                        let colorClass = 'text-secondary';
                        let icon = '?';

                        if (tipo_dato.toLowerCase().includes('temp')) {
                            unit = '°C'; colorClass = 'text-danger';
                        } else if (tipo_dato.toLowerCase().includes('humedad')) {
                            unit = '%'; colorClass = 'text-info';
                        } else if (tipo_dato.toLowerCase().includes('luz')) {
                            unit = 'lux'; colorClass = 'text-warning';
                        }

                        const cardHtml = `
                            <div class="col">
                                <div class="card shadow-sm h-100">
                                    <div class="card-body">
                                        <h5 class="card-title">${icon} ${municipio.charAt(0).toUpperCase() + municipio.slice(1)}</h5>
                                        <h6 class="card-subtitle mb-2 text-muted">${tipo_dato}</h6>
                                        <p class="display-4 ${colorClass} fw-bold">${value.toFixed(2)}${unit}</p>
                                        <p class="card-text"><small class="text-muted">Actualizado: ${new Date(timestamp).toLocaleTimeString()}</small></p>
                                    </div>
                                </div>
                            </div>`;
                        realtimeCardsContainer.innerHTML += cardHtml;
                    });
                })
                .catch(() => {
                    realtimeCardsContainer.innerHTML =
                        '<p class="text-danger w-100 text-center">Error al conectar con la API.</p>';
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
            try {
                rawData = JSON.parse(chartDataElement.textContent);
            } catch {
                return;
            }
        }

        const groupedData = rawData.reduce((acc, item) => {
            if (!item.tipo_dato || item.value === undefined) return acc;
            const tipo = item.tipo_dato.toLowerCase();

            if (!acc[tipo]) acc[tipo] = { labels: [], data: [] };

            acc[tipo].labels.unshift(new Date(item.timestamp).toLocaleTimeString());
            acc[tipo].data.unshift(item.value);
            return acc;
        }, {});

        const colors = ['#dc3545', '#007bff', '#ffc107', '#28a745', '#6f42c1', '#fd7e14'];

        const datasets = Object.keys(groupedData).map((type, index) => ({
            label: type.charAt(0).toUpperCase() + type.slice(1),
            data: groupedData[type].data,
            borderColor: colors[index % colors.length],
            backgroundColor: colors[index % colors.length] + '40',
            fill: false,
            tension: 0.3
        }));

        if (datasets.length > 0) {
            new Chart(chartCtx, {
                type: 'line',
                data: {
                    labels: groupedData[Object.keys(groupedData)[0]].labels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: { title: { display: true, text: 'Tendencia Histórica' } },
                    scales: {
                        x: { title: { display: true, text: 'Tiempo' } },
                        y: { title: { display: true, text: 'Valor' } }
                    }
                }
            });
        } else {
            chartCtx.canvas.parentNode.innerHTML =
                '<p class="text-center text-muted">Sin datos para generar la gráfica.</p>';
        }
    }
});
