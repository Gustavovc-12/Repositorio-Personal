async function cargarEstado() {
    try {
        const res = await fetch("/status");
        const data = await res.json();

        renderServidor(data.server);
        renderServo(data.servo);
        renderBateria(data.battery);

    } catch (e) {
        document.getElementById("server").innerText = "❌ Sin conexión";
        document.getElementById("servo").innerText = "❌ Sin conexión";
        document.getElementById("battery").innerText = "❌ Sin conexión";
    }
}

/* ========= SERVIDOR ========= */
function renderServidor(d) {
    const estado = d.alive ? "Online" : "Offline";
    const color = d.alive ? "green" : "red";

    document.getElementById("server").innerHTML = `
        <h2>🌐 Servidor</h2>
        <p>
            <span class="led ${color}"></span>
            <b>Estado:</b> ${estado}
        </p>
        <p><b>Hora:</b> ${d.time}</p>
    `;
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
        <p class="muted">Actualizado: ${d.last_update}</p>
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

    const porcentaje = Math.max(0, Math.min(100, d.percentage));
    const nivel = d.low ? "low" : "ok";

    document.getElementById("battery").innerHTML = `
        <h2>🔋 Batería</h2>

        <div class="battery-bar">
            <div class="battery-level ${nivel}" style="width: ${porcentaje}%"></div>
        </div>

        <p><b>Carga:</b> ${porcentaje}%</p>
        <p><b>Voltaje:</b> ${d.voltage.toFixed(2)} V</p>

        ${d.low ? `<p class="warning">⚠️ Batería baja</p>` : ""}

        <p class="muted">Actualizado: ${d.last_update}</p>
    `;
}

/* ========= LOOP ========= */
setInterval(cargarEstado, 1000);
cargarEstado();
