async function cargarEstado() {
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

setInterval(cargarEstado, 500);
cargarEstado();