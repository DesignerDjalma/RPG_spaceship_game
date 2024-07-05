// game.js

export function initGame() {
    // Obtém o contexto do canvas
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    // Carrega o sprite do jogador
    const playerSprite = new Image();
    playerSprite.src = 'ship103.png';

    // Dimensões do sprite e do frame
    const spriteWidth = 225; // largura de cada frame do sprite
    const spriteHeight = 225; // altura de cada frame do sprite
    const cols = 9; // número de colunas no sprite
    const rows = 8; // número de linhas no sprite
    let frameIndex = 0; // índice inicial do frame
    let angle = 0; // ângulo inicial do jogador

    // Posição inicial do jogador
    let playerX = canvas.width / 2 - spriteWidth / 2;
    let playerY = canvas.height / 2 - spriteHeight / 2;

    // Velocidade de movimento do jogador
    const playerSpeed = 4;

    // Função para calcular o ângulo entre dois pontos
    function getAngle(x1, y1, x2, y2) {
        return Math.atan2(y2 - y1, x2 - x1);
    }

    // Função para atualizar o jogo
    function update() {
        // Limpar o canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Calcular o ângulo entre o jogador e o ponto do mouse
        angle = getAngle(playerX + spriteWidth / 2, playerY + spriteHeight / 2, mouseX, mouseY);

        // Converter o ângulo para graus
        let degreeAngle = -angle * (180 / Math.PI);
        if (degreeAngle < 0) {
            degreeAngle = 360 + degreeAngle;
        }


        // Determinar o índice do frame com base no ângulo
        frameIndex = Math.floor((degreeAngle / 360) * (cols * rows));

        // Desenhar o jogador na posição atual com o frame correspondente
        const col = frameIndex % cols;
        const row = Math.floor(frameIndex / cols);
        ctx.drawImage(playerSprite, col * spriteWidth, row * spriteHeight, spriteWidth, spriteHeight, playerX, playerY, spriteWidth, spriteHeight);

        // Movimentar o jogador em direção ao alvo (opcional, para movimentação)
        // if (playerX !== targetX || playerY !== targetY) {
        //     const dx = targetX - playerX;
        //     const dy = targetY - playerY;
        //     const distance = Math.sqrt(dx * dx + dy * dy);
        //     const velocityX = (dx / distance) * playerSpeed;
        //     const velocityY = (dy / distance) * playerSpeed;
        //     if (distance < playerSpeed) {
        //         playerX = targetX;
        //         playerY = targetY;
        //     } else {
        //         playerX += velocityX;
        //         playerY += velocityY;
        //     }
        // }

        // Solicitar a próxima atualização
        requestAnimationFrame(update);
    }

    // Atualizar a posição do mouse
    let mouseX = playerX + spriteWidth / 2;
    let mouseY = playerY + spriteHeight / 2;

        // Atualizar a posição do alvo quando o mouse é clicado


    // Atualizar posição do mouse quando ele se move
    canvas.addEventListener('mousemove', function(event) {
        mouseX = event.clientX - canvas.getBoundingClientRect().left;
        mouseY = event.clientY - canvas.getBoundingClientRect().top;
    });
    canvas.addEventListener('click', function(event) {
        targetX = event.clientX - canvas.getBoundingClientRect().left - playerImg.width / 2;
        targetY = event.clientY - canvas.getBoundingClientRect().top - playerImg.height / 2;
    });

    // Iniciar o jogo
    playerSprite.onload = function() {
        update();
    };
}