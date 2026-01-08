async function cargarServo() {
    try {
        const res = await fetch("/servo/state");
        const data = await res.json();

        document.getElementById("servo").innerHTML = `
            <h2>Control de Servomotores</h2>

            <p><b>Grupo activo:</b> ${data.group}</p>
            <p><b>Modo:</b> ${data.mode}</p>

            <p><b>Posición actual:</b> ${data.pos}°</p>

            ${
                data.mode === "auto"
                ? `
                    <p><b>Posición máxima:</b> ${data.max_pos}°</p>
                    <p><b>Movimiento periódico:</b> ${data.periodic ? "Sí" : "No"}</p>
                    <p><b>Duración:</b> ${data.duration_s} s</p>
                  `
                : ""
            }

            <p><b>Última actualización:</b> ${data.last_update}</p>
        `;
    } catch (e) {
        document.getElementById("servo").innerHTML =
            "<h2>Control de Servomotores</h2><p>Error de conexión</p>";
    }
}

async function cargarBateria() {
    try {
        const res = await fetch("/battery/state");
        const data = await res.json();

        if (data.percentage === null) {
            document.getElementById("battery").innerHTML = `
                <h2>Estado de Batería</h2>
                <p>Sin datos disponibles</p>
            `;
            return;
        }

        document.getElementById("battery").innerHTML = `
            <h2>Estado de Batería</h2>

            <p><b>Carga:</b> ${data.percentage}%</p>
            <p><b>Voltaje:</b> ${data.voltage.toFixed(2)} V</p>
            <p><b>Última actualización:</b> ${data.last_update}</p>
        `;
    } catch (e) {
        document.getElementById("battery").innerHTML =
            "<h2>Estado de Batería</h2><p>Error de conexión</p>";
    }
}

function cargarEstado() {
    cargarServo();
    cargarBateria();
}

// Refresco automático
setInterval(cargarEstado, 1000);
cargarEstado();
