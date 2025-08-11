window.onload = function() {
    let canvas = document.createElement('canvas');
    canvas.id = 'rainCanvas';
    document.body.appendChild(canvas);
    let ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let raindrops = [];
    for (let i = 0; i < 200; i++) {
        raindrops.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            length: Math.random() * 20 + 10,
            speed: Math.random() * 4 + 2
        });
    }

    function drawRain() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = 'rgba(174,194,224,0.5)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        for (let drop of raindrops) {
            ctx.moveTo(drop.x, drop.y);
            ctx.lineTo(drop.x, drop.y + drop.length);
        }
        ctx.stroke();
        moveRain();
    }

    function moveRain() {
        for (let drop of raindrops) {
            drop.y += drop.speed;
            if (drop.y > canvas.height) {
                drop.y = -drop.length;
                drop.x = Math.random() * canvas.width;
            }
        }
    }

    function animate() {
        drawRain();
        requestAnimationFrame(animate);
    }
    animate();
};
