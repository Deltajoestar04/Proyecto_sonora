const ctx = document.getElementById('lecturasChart').getContext('2d');
let lecturasChart = null;

function isoToDate(iso) {
  try {
    return new Date(iso);
  } catch (e) {
    return null;
  }
}

function fetchAndRender() {
  fetch('/api/lecturas/')
    .then(resp => {
      if (!resp.ok) throw new Error('network response was not ok');
      return resp.json();
    })
    .then(data => {
      const labels = [];
      const values = [];

      data.forEach(item => {
        let dateValue = null;
        if (item.timestamp) {
          dateValue = isoToDate(item.timestamp);
        } else {
          for (const k in item) {
            if (/time|date|timestamp/i.test(k) && item[k]) {
              dateValue = isoToDate(item[k]);
              break;
            }
          }
        }
        let numeric = null;
        if (item.valor !== undefined) numeric = parseFloat(item.valor);
        else if (item.value !== undefined) numeric = parseFloat(item.value);
        else {
          for (const k in item) {
            if (/valor|value|lectura|reading|sensor_value/i.test(k) && item[k] !== null) {
              numeric = parseFloat(item[k]);
              break;
            }
          }
        }

        if (dateValue && !isNaN(numeric)) {
          labels.push(dateValue.toLocaleString());
          values.push(numeric);
        }
      });

      if (values.length === 0) {
        console.log('No hay datos para dibujar.');
        if (lecturasChart) {
          lecturasChart.data.labels = [];
          lecturasChart.data.datasets[0].data = [];
          lecturasChart.update();
        }
        return;
      }

      const cfg = {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Lectura',
            data: values,
            fill: false,
            tension: 0.1,
          }]
        },
        options: {
          responsive: true,
          scales: {
            x: { display: true, title: { display: true, text: 'Fecha' } },
            y: { display: true, title: { display: true, text: 'Valor' } }
          }
        }
      };

      if (!lecturasChart) {
        lecturasChart = new Chart(ctx, cfg);
      } else {
        lecturasChart.data = cfg.data;
        lecturasChart.options = cfg.options;
        lecturasChart.update();
      }
    })
    .catch(err => {
      console.error('Error al obtener lecturas:', err);
    });
}

fetchAndRender();
