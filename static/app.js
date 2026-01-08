async function cargarServo() {
    try {
        const res = await fetch("/servo/state");
        const d = await res.json();

        let extra = "";

        if (d.mode === "manual") {
            extra = `<p><b>Posición:</b> ${d.pos}°</p>`;
        } else {
            extra = `
                <p><b>Máx:</b> ${d.max_pos}°</p>
                <p><b>Periódico:</b> ${d.periodic ? "Sí" : "No"}</p>
                <p><b>Duración:</b> ${d.duration_s}s</p>
            `;
        }

        document.getElementById("servo").innerHTML = `
            <h2>🤖 Servomotores</h2>
            <p><b>Grupo:</b> ${d.group}</p>
            <p><b>Modo:</b> ${d.mode}</p>
            ${extra}
            <p class="muted">Actualizado por: ${d.last_update}</p>
        `;
    } catch (e) {
        document.getElementById("servo").innerText = "Error de conexión";
    }
}

async function cargarBateria() {
    try {
        const res = await fetch("/battery/state");
        const d = await res.json();

        if (d.percentage === null) {
            document.getElementById("battery").innerHTML = `
                <h2>🔋 Batería</h2>
                <p>Sin datos aún</p>
            `;
            return;
        }

        document.getElementById("battery").innerHTML = `
            <h2>🔋 Batería</h2>
            <p><b>Carga:</b> ${d.percentage}%</p>
            <p><b>Voltaje:</b> ${d.voltage.toFixed(2)} V</p>
            <p class="muted">Actualizado por: ${d.last_update}</p>
        `;
    } catch (e) {
        document.getElementById("battery").innerText = "Error de conexión";
    }
}

function cargarEstado() {
    cargarServo();
    cargarBateria();
}

setInterval(cargarEstado, 1000);
cargarEstado();
