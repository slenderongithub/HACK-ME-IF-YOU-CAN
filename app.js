// Matrix animation
const canvas = document.getElementById('matrix-canvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const binary = '01';
const fontSize = 16;
const columns = canvas.width / fontSize;
const drops = Array(Math.floor(columns)).fill(1);

function drawMatrix() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#00ff00';
    ctx.font = `${fontSize}px monospace`;

    drops.forEach((y, x) => {
        const text = binary[Math.floor(Math.random() * binary.length)];
        ctx.fillText(text, x * fontSize, y * fontSize);

        if (y * fontSize > canvas.height && Math.random() > 0.975) {
            drops[x] = 0;
        }
        drops[x]++;
    });
}

setInterval(drawMatrix, 50);

// Typing animation for the text
const typingText = document.getElementById('typing-text');
typingText.textContent = "Can you survive the internet";

// Navigation logic
const startBtn = document.getElementById('start-btn');
const matrixScreen = document.getElementById('matrix-screen');
const mainScreen = document.getElementById('main-screen');

startBtn.addEventListener('click', () => {
    matrixScreen.classList.add('hidden');
    mainScreen.classList.remove('hidden');
});