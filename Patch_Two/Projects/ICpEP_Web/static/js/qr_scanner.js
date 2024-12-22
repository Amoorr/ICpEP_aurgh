const html5Qrcode = new Html5Qrcode('reader');

const qrCodeSuccessCallback = (decodedText, decodedResult) => {
    if (decodedText) {
        document.getElementById('show').style.display = 'block';
        document.getElementById('result').textContent = decodedText;

        // Send scanned text to the Django backend
        fetch('/event/qr_scanner/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken') // CSRF token for security
            },
            body: `scanned_text=${encodeURIComponent(decodedText)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(data.message);
            } else {
                console.error(data.message);
            }
        })
        .catch(error => console.error('Error:', error));

        html5Qrcode.stop(); // Stop the scanner after a successful scan
    }
};

// Helper function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const config = { fps: 10, qrbox: { width: 250, height: 250 } };
html5Qrcode.start({ facingMode: "environment" }, config, qrCodeSuccessCallback);
