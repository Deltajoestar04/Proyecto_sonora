(function(){
  const municipioInput = document.getElementById('municipio');
  const tipoInput = document.getElementById('tipo');
  const ctx = document.getElementById('chart').getContext('2d');
  let chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{ label: 'valor', data: [], fill: false }]
    },
    options: { animation: false }
  });

  async function fetchAndUpdate(){
    const municipio = municipioInput.value || '';
    const tipo = tipoInput.value || '';
    const url = `/api/latest/?municipio=${encodeURIComponent(municipio)}&tipo=${encodeURIComponent(tipo)}&limit=50`;
    try {
      const res = await fetch(url);
      if(!res.ok) throw new Error('fetch');
      const json = await res.json();
      const data = json.data;
      chart.data.labels = data.map(d => new Date(d.recibido_en).toLocaleTimeString());
      chart.data.datasets[0].data = data.map(d => d.valor);
      chart.update();
    } catch(e) {
      console.error('Error fetching data', e);
    }
  }

  fetchAndUpdate();
  setInterval(fetchAndUpdate, 3000);
})();
