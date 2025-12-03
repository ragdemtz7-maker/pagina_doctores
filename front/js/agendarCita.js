document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.getElementById("agendar");
  const horarioSelect = document.getElementById("horarioSelect");
  const appointmentBox = document.querySelector(".appointment_box");

  const emailInput = document.getElementById("citaCorreo");
  const nameInput = document.getElementById("citaNombre");
  const telefonoInput = document.getElementById("citaTelefono");

  function decodeJWT(token) {
    try {
      const parts = token.split(".");
      if (parts.length !== 3) return null;
      let base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
      while (base64.length % 4) base64 += "=";
      return JSON.parse(atob(base64));
    } catch {
      return null;
    }
  }

  const token = localStorage.getItem("userPatient");
  if (!token) {
    appointmentBox.style.display = "none";
    return;
  }
  appointmentBox.style.display = "block";

  const userData = decodeJWT(token);
  if (userData) {
    emailInput.value = userData.correo || userData.email || "";
    nameInput.value = userData.nombre || "";
    telefonoInput.value = userData.telefono || "";
  }

  submitBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    if (!userData || !userData.id_paciente) {
      alert("No hay sesión de paciente válida");
      return;
    }
    if (!horarioSelect.value) {
      alert("Selecciona un horario (programación)");
      return;
    }

    const payload = {
      id_programacion: parseInt(horarioSelect.value, 10),
      id_paciente: userData.id_paciente,
      estado: "programada",
    };

    try {
      const resp = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/cita_medica/", {
        method: "POST",
        headers: { "Content-Type": "application/json", accept: "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await resp.json();
      if (!resp.ok) {
        alert("Error al agendar la cita");
        return;
      }
      alert("Cita agendada con éxito. ID: " + (data.id_cita ?? payload.id_programacion));
      window.location.href = "citas_agendadas.html";
    } catch (err) {
      console.error("Error creando cita", err);
      alert("Error al agendar la cita");
    }
  });
});
