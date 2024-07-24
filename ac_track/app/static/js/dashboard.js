document.getElementById('startMonitoring').addEventListener('click', async function() {
    const response = await fetch('/start_tracking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const result = await response.json();
    const feedback = document.getElementById('feedback');

    if (result.success) {
        feedback.textContent = 'Monitoring started.';
        feedback.style.color = '#00e676';
    } else {
        feedback.textContent = 'Failed to start monitoring: ' + result.message;
        feedback.style.color = '#ff4081';
    }
});

document.getElementById('stopMonitoring').addEventListener('click', async function() {
    const response = await fetch('/stop_tracking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const result = await response.json();
    const feedback = document.getElementById('feedback');

    if (result.success) {
        feedback.textContent = 'Monitoring stopped.';
        feedback.style.color = '#00e676';
    } else {
        feedback.textContent = 'Failed to stop monitoring: ' + result.message;
        feedback.style.color = '#ff4081';
    }
});

document.getElementById('logout').addEventListener('click', function() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/login';
});
