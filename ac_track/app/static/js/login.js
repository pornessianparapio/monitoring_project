document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    const result = await response.json();
    const feedback = document.getElementById('feedback');

    if (response.ok) {
            feedback.textContent = result.message;
            feedback.style.color = '#00e676'; // Success color

            // Redirect to the appropriate page
            if (result.redirect_url) {
                window.location.href = result.redirect_url;
            }
        } else {
            feedback.textContent = result.message;
            feedback.style.color = '#ff4081'; // Error color

        }
});
