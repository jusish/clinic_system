document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('patientsChart').getContext('2d');
    const patientsData = JSON.parse(document.getElementById('patientsData').textContent);
    const patientsLabels = JSON.parse(document.getElementById('patientsLabels').textContent);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: patientsLabels,
            datasets: [{
                label: 'Patients Treated',
                data: patientsData,
                borderColor: '#4A628A',
                backgroundColor: 'rgba(74, 98, 138, 0.2)',
                borderWidth: 2,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
