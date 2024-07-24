document.getElementById('registrationForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const is_admin = document.getElementById('is_admin').checked;

    const response = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password, is_admin })
    });

    const result = await response.json();
    const feedback = document.getElementById('feedback');

    if (result.success) {
        feedback.textContent = 'Registration successful!';
        feedback.style.color = '#00e676';
    } else {
        feedback.textContent = 'Registration failed: ' + result.message;
        feedback.style.color = '#ff4081';
    }
});
