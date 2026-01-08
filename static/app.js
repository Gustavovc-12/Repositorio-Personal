async function cargarEstado() {
    try {
        const res = await fetch("/status");
        const data = await res.json();

        renderServo(data.servo);
        renderBateria(data.battery);
        renderServidor(data.server);

    } catch (e) {
        document.getElementById("servo").innerText = "❌ Sin conexión";
        document.getElementById("battery").innerText = "❌ Sin conexión";
        document.getElementById("server").innerText = "❌ Servidor caído";
    }
}

/* ========= SERVO ========= */
function renderServo(d) {
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
        <h2>🦾 Servo</h2>
        <p><b>Grupo:</b> ${d.group}</p>
        <p><b>Modo:</b> ${d.mode}</p>
        ${extra}
        <p class="muted">Última actualización: ${d.last_update}</p>
    `;
}

/* ========= BATERÍA ========= */
function renderBateria(d) {
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
        <p class="muted">Última actualización: ${d.last_update}</p>
    `;
}

/* ========= SERVIDOR ========= */
function renderServidor(d) {
    document.getElementById("server").innerHTML = `
        <h2>🌐 Servidor</h2>
        <p><b>Estado:</b> ${d.alive ? "🟢 Online" : "🔴 Offline"}</p>
        <p><b>Hora:</b> ${d.time}</p>
    `;
}

/* ========= LOOP ========= */
setInterval(cargarEstado, 1000);
cargarEstado();
