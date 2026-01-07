async function cargarServo() {
    try {
        const res = await fetch("/servo/state");
        const data = await res.json();

        document.getElementById("servo").innerHTML = `
            <h2>Servo</h2>
            <p>Posición objetivo: <b>${data.pos}°</b></p>
            <p>Última actualización: ${data.last_update}</p>
        `;
    } catch (e) {
        document.getElementById("servo").innerText = "Error de conexión";
    }
}

async function cargarBateria() {
    try {
        const res = await fetch("/battery/state");
        const data = await res.json();

        if (data.percentage === null) {
            document.getElementById("battery").innerHTML = `
                <h2>🔋 Batería</h2>
                <p>Sin datos aún</p>
            `;
            return;
        }

        document.getElementById("battery").innerHTML = `
            <h2>🔋 Batería</h2>
            <p>Carga: <b>${data.percentage}%</b></p>
            <p>Voltaje: ${data.voltage.toFixed(2)} V</p>
            <p>Tiempo restante: ${data.time_remaining_h.toFixed(2)} h</p>
            <p>Eficiencia: ${(data.efficiency * 100).toFixed(1)} %</p>
            <p>Última actualización: ${data.last_update}</p>
        `;
    } catch (e) {
        document.getElementById("battery").innerText = "Error de conexión";
    }
}

function cargarEstado() {
    cargarServo();
    cargarBateria();
}

// refresco
setInterval(cargarEstado, 1000);
cargarEstado();
