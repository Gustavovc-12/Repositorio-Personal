console.log("APP.JS CARGADO");

async function cargarEstado() {
    try {
        console.log("ANTES DEL FETCH");
        const res = await fetch(window.location.origin + "/status");
        console.log("DESPUÉS DEL FETCH", res.status);

        const data = await res.json();
        console.log("DATA:", data);

        // -------- SERVO --------
        const s = data.servo;

        let extra = "";
        if (s.mode === "manual") {
            extra = `<p><b>Comando:</b> ${s.command}</p>`;
        } else {
            extra = `
                <p><b>Máx:</b> ${s.max_pos}°</p>
                <p><b>Periódico:</b> ${s.periodic ? "Sí" : "No"}</p>
                <p><b>Duración:</b> ${s.duration_s}s</p>
            `;
        }

        document.getElementById("servo").innerHTML = `
            <h2>🤖 Servomotores</h2>
            <p><b>Grupo:</b> ${s.group}</p>
            <p><b>Modo:</b> ${s.mode}</p>
            ${extra}
            <p class="muted">Actualizado por: ${s.last_update}</p>
        `;

        // -------- BATERÍA --------
        const b = data.battery;

        if (b.percentage === null) {
            document.getElementById("battery").innerHTML = `
                <h2>🔋 Batería</h2>
                <p>Sin datos aún</p>
            `;
        } else {
            document.getElementById("battery").innerHTML = `
                <h2>🔋 Batería</h2>
                <p><b>Carga:</b> ${b.percentage}%</p>
                <p><b>Voltaje:</b> ${b.voltage.toFixed(2)} V</p>
                <p class="muted">Actualizado por: ${b.last_update}</p>
            `;
        }

    } catch (e) {
        document.getElementById("servo").innerText = "Error de conexión";
        document.getElementById("battery").innerText = "Error de conexión";
    }
}

setInterval(cargarEstado, 1000);
cargarEstado();
