async function cargarServo() {
    const res = await fetch("/servo/state", {
        headers: {
            "X-Device-Token": "ESP32_TOKEN_ABC123"
        }
    });

    const d = await res.json();

    document.getElementById("servo").innerHTML = `
        <h2>Servomotores</h2>
        <p>Grupo activo: <b>${d.group}</b></p>
        <p>Modo: <b>${d.mode}</b></p>
        <p>Posición actual: <b>${d.pos}°</b></p>
        <p>Última actualización: ${d.last_update}</p>
    `;
}

async function cargarBateria() {
    const res = await fetch("/battery/state");
    const d = await res.json();

    if (d.percentage === null) {
        document.getElementById("battery").innerHTML = `
            <h2>Batería</h2>
            <p>Sin datos disponibles</p>
        `;
        return;
    }

    document.getElementById("battery").innerHTML = `
        <h2>Batería</h2>
        <p>Carga: <b>${d.percentage}%</b></p>
        <p>Voltaje: <b>${d.voltage.toFixed(2)} V</b></p>
        <p>Última actualización: ${d.last_update}</p>
    `;
}

function refrescar() {
    cargarServo();
    cargarBateria();
}

setInterval(refrescar, 1000);
refrescar();
