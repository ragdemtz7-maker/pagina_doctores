
document.addEventListener("DOMContentLoaded", async () => {
  const tablaCitas = document.getElementById("tablaCitas");

  // Utilidad: convertir segundos a HH:MM
  function segundosAHora(segundos) {
    const h = Math.floor(segundos / 3600).toString().padStart(2, "0");
    const m = Math.floor((segundos % 3600) / 60).toString().padStart(2, "0");
    return `${h}:${m}`;
  }

  // Decodificar JWT base64url-safe
  function decodeJWT(token) {
    try {
      const parts = token.split(".");
      if (parts.length !== 3) return null;
      let base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
      while (base64.length % 4) base64 += "=";
      return JSON.parse(atob(base64));
    } catch (err) {
      console.error("Error decodificando JWT", err);
      return null;
    }
  }

  // Obtener token y paciente
  const token = localStorage.getItem("userPatient");
  if (!token) {
    tablaCitas.innerHTML = "<tr><td colspan='7'>No hay sesión activa</td></tr>";
    return;
  }
  const userData = decodeJWT(token);
  if (!userData || !userData.id_paciente) {
    tablaCitas.innerHTML = "<tr><td colspan='7'>JWT inválido o sin id_paciente</td></tr>";
    return;
  }

  const idPaciente = userData.id_paciente;
  console.log("Paciente autenticado:", idPaciente);

  try {
    const resp = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/cita_medica/");
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const citas = await resp.json();
    console.log("Citas recibidas:", citas);

    // Filtrar por paciente
    const citasPaciente = citas.filter(c => c.id_paciente === idPaciente);

    if (citasPaciente.length === 0) {
      tablaCitas.innerHTML = "<tr><td colspan='7'>No hay citas para este paciente</td></tr>";
      return;
    }

    // Llenar tabla
    tablaCitas.innerHTML = "";
    citasPaciente.forEach(c => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
        <td>${c.id_cita}</td>
        <td>${c.fecha}</td>
        <td>${segundosAHora(c.hora_inicio)}</td>
        <td>${segundosAHora(c.hora_fin)}</td>
        <td>${c.estado}</td>
        <td>${c.paciente_nombre}</td>
        <td>${c.paciente_apellido}</td>
      `;
      tablaCitas.appendChild(fila);
    });
  } catch (err) {
    console.error("Error cargando citas", err);
    tablaCitas.innerHTML = "<tr><td colspan='7'>Error al cargar citas</td></tr>";
  }
});
