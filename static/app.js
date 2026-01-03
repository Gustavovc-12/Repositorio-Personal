async function cargarEstado() {
    const res = await fetch("/status");
    const data = await res.json();

    document.getElementById("status").innerHTML = `
        <h2>Estado del Sistema</h2>
        <p>Conexión: ${data.conexion}</p>
        <p>Servidores: ${data.servidores}</p>
        <p>${data.recomendacion}</p>
    `;
}

async function cargarBateria() {
    const res = await fetch("/battery");
    const data = await res.json();

    document.getElementById("battery").innerHTML = `
        <h2>Batería</h2>
        <p>Porcentaje: ${data.porcentaje}%</p>
        <p>Estado: ${data.estado}</p>
        <p>Autonomía: ${data.autonomia_estimada}</p>
    `;
}

cargarEstado();
cargarBateria();
