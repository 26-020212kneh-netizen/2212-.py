import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Stage Pinball",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 Stage Pinball")
st.write("벽돌을 모두 제거하고 다음 스테이지로 진입하세요!")

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
    body {
        margin: 0;
        background: #111827;
        color: white;
        font-family: Arial, sans-serif;
        text-align: center;
    }

    #game {
        background: #020617;
        border: 3px solid #38bdf8;
        border-radius: 10px;
        display: block;
        margin: 10px auto;
    }

    .info {
        display: flex;
        justify-content: center;
        gap: 25px;
        margin: 10px;
        font-size: 18px;
    }

    button {
        background: #2563eb;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
    }

    button:hover {
        background: #1d4ed8;
    }
</style>
</head>

<body>

<div class="info">
    <div>Stage: <span id="stage">1</span></div>
    <div>Score: <span id="score">0</span></div>
    <div>Lives: <span id="lives">3</span></div>
</div>

<canvas id="game" width="480" height="640"></canvas>

<button onclick="restartGame()">Restart</button>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;

let stage = 1;
let score = 0;
let lives = 3;

let gameOver = false;
let stageClear = false;

const keys = {};

document.addEventListener("keydown", e => {
    keys[e.key.toLowerCase()] = true;

    if (e.key.toLowerCase() === "r") {
        restartGame();
    }
});

document.addEventListener("keyup", e => {
    keys[e.key.toLowerCase()] = false;
});


// ==============================
// 공
// ==============================

let ball = {
    x: WIDTH / 2,
    y: HEIGHT - 100,
    radius: 9,
    vx: 3,
    vy: -5
};


// ==============================
// 패들
// ==============================

const paddle = {
    x: WIDTH / 2 - 50,
    y: HEIGHT - 40,
    width: 100,
    height: 12,
    speed: 7
};


// ==============================
// 벽돌
// ==============================

let bricks = [];

function createBricks() {

    bricks = [];

    const rows = 3 + stage;
    const cols = 6;

    const brickWidth = 60;
    const brickHeight = 20;

    const startX = 45;
    const startY = 70;

    for (let row = 0; row < rows; row++) {

        for (let col = 0; col < cols; col++) {

            bricks.push({
                x: startX + col * 65,
                y: startY + row * 30,
                width: brickWidth,
                height: brickHeight,
                alive: true
            });

        }
    }
}


// ==============================
// 게임 초기화
// ==============================

function resetBall() {

    ball.x = WIDTH / 2;
    ball.y = HEIGHT - 100;

    const speed = 4 + stage * 0.7;

    ball.vx = speed * (Math.random() > 0.5 ? 1 : -1);
    ball.vy = -speed;
}


function startStage() {

    stageClear = false;

    createBricks();
    resetBall();

    document.getElementById("stage").textContent = stage;
}


// ==============================
// 충돌 판정
// ==============================

function collision(a, b) {

    return (
        a.x + a.radius > b.x &&
        a.x - a.radius < b.x + b.width &&
        a.y + a.radius > b.y &&
        a.y - a.radius < b.y + b.height
    );
}


// ==============================
// 업데이트
// ==============================

function update() {

    if (gameOver || stageClear) {
        return;
    }

    // 패들 이동
    if (keys["arrowleft"] || keys["a"]) {
        paddle.x -= paddle.speed;
    }

    if (keys["arrowright"] || keys["d"]) {
        paddle.x += paddle.speed;
    }

    paddle.x = Math.max(
        0,
        Math.min(WIDTH - paddle.width, paddle.x)
    );


    // 공 이동
    ball.x += ball.vx;
    ball.y += ball.vy;


    // 벽 충돌

    if (ball.x - ball.radius < 0) {
        ball.x = ball.radius;
        ball.vx *= -1;
    }

    if (ball.x + ball.radius > WIDTH) {
        ball.x = WIDTH - ball.radius;
        ball.vx *= -1;
    }

    if (ball.y - ball.radius < 0) {
        ball.y = ball.radius;
        ball.vy *= -1;
    }


    // 패들 충돌

    if (collision(ball, paddle) && ball.vy > 0) {

        ball.y = paddle.y - ball.radius;

        ball.vy *= -1;

        // 패들의 어느 위치에 맞았는지에 따라 방향 변경
        const hitPosition =
            (ball.x - paddle.x) / paddle.width;

        ball.vx = (hitPosition - 0.5) * 10;
    }


    // 벽돌 충돌

    for (let brick of bricks) {

        if (!brick.alive) continue;

        if (collision(ball, brick)) {

            brick.alive = false;

            ball.vy *= -1;

            score += 100;

            document.getElementById("score")
                .textContent = score;

            break;
        }
    }


    // 모든 벽돌 제거
    const remaining = bricks.filter(
        brick => brick.alive
    ).length;

    if (remaining === 0) {

        stageClear = true;

        setTimeout(() => {

            if (stage < 5) {

                stage++;

                startStage();

            } else {

                gameOver = true;

            }

        }, 1500);
    }


    // 공이 바닥으로 떨어짐

    if (ball.y > HEIGHT) {

        lives--;

        document.getElementById("lives")
            .textContent = lives;

        if (lives <= 0) {

            gameOver = true;

        } else {

            resetBall();
        }
    }
}


// ==============================
// 그리기
// ==============================

function draw() {

    ctx.clearRect(
        0,
        0,
        WIDTH,
        HEIGHT
    );


    // 배경

    ctx.fillStyle = "#020617";

    ctx.fillRect(
        0,
        0,
        WIDTH,
        HEIGHT
    );


    // 벽돌

    for (let brick of bricks) {

        if (!brick.alive) continue;

        const colors = [
            "#ef4444",
            "#f97316",
            "#eab308",
            "#22c55e",
            "#06b6d4",
            "#3b82f6"
        ];

        ctx.fillStyle =
            colors[stage % colors.length];

        ctx.fillRect(
            brick.x,
            brick.y,
            brick.width,
            brick.height
        );
    }


    // 패들

    ctx.fillStyle = "#38bdf8";

    ctx.fillRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height
    );


    // 공

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#ffffff";

    ctx.fill();

    ctx.closePath();


    // 스테이지 클리어

    if (stageClear) {

        ctx.fillStyle =
            "rgba(0,0,0,0.7)";

        ctx.fillRect(
            0,
            0,
            WIDTH,
            HEIGHT
        );

        ctx.fillStyle = "#22c55e";

        ctx.font = "32px Arial";

        ctx.textAlign = "center";

        ctx.fillText(
            "STAGE CLEAR!",
            WIDTH / 2,
            HEIGHT / 2
        );
    }


    // 게임 오버

    if (gameOver) {

        ctx.fillStyle =
            "rgba(0,0,0,0.75)";

        ctx.fillRect(
            0,
            0,
            WIDTH,
            HEIGHT
        );

        ctx.fillStyle = "#ef4444";

        ctx.font = "36px Arial";

        ctx.textAlign = "center";

        if (stage >= 5) {

            ctx.fillText(
                "🎉 YOU WIN!",
                WIDTH / 2,
                HEIGHT / 2
            );

        } else {

            ctx.fillText(
                "GAME OVER",
                WIDTH / 2,
                HEIGHT / 2
            );
        }
    }
}


// ==============================
// 게임 루프
// ==============================

function gameLoop() {

    update();
    draw();

    requestAnimationFrame(gameLoop);
}


// ==============================
// 재시작
// ==============================

function restartGame() {

    stage = 1;
    score = 0;
    lives = 3;

    gameOver = false;
    stageClear = false;

    document.getElementById("stage")
        .textContent = stage;

    document.getElementById("score")
        .textContent = score;

    document.getElementById("lives")
        .textContent = lives;

    startStage();
}


// 시작
startStage();
gameLoop();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=750,
    scrolling=False
)
