document.addEventListener("DOMContentLoaded", () => {
  const especialidadSelect = document.getElementById("especialidadSelect");
  const horarioSelect = document.getElementById("horarioSelect");
  const fechaInput = document.getElementById("datepicker");
  const submitBtn = document.getElementById("submitBtn");

  // Utilidad: convertir segundos a HH:MM
  function segundosAHora(segundos) {
    const h = Math.floor(segundos / 3600).toString().padStart(2, "0");
    const m = Math.floor((segundos % 3600) / 60).toString().padStart(2, "0");
    return `${h}:${m}`;
  }

  // 1) Cargar especialidades
  async function cargarEspecialidades() {
    try {
      const resp = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/especialidad/todas");
      const data = await resp.json();
      especialidadSelect.innerHTML = "<option>Seleccione una especialidad</option>";
      data.forEach(([id, nombre]) => {
        const opt = document.createElement("option");
        opt.value = id;
        opt.textContent = nombre;
        especialidadSelect.appendChild(opt);
      });
    } catch (err) {
      console.error("Error cargando especialidades", err);
    }
  }

  // 2) Cargar horarios (programaciones)
  async function cargarHorarios() {
    try {
      const resp = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/api/programacion/listar");
      const data = await resp.json();
      horarioSelect.innerHTML = "<option>Seleccione un horario</option>";
      data.forEach(p => {
        // Filtrar por fecha si el usuario seleccionó una
        if (fechaInput.value && p.fecha !== fechaInput.value) return;
        const opt = document.createElement("option");
        opt.value = p.id_programacion;
        opt.textContent = `${p.fecha} ${segundosAHora(p.hora_inicio)} - ${segundosAHora(p.hora_fin)} (Medico ${p.id_medico})`;
        horarioSelect.appendChild(opt);
      });
    } catch (err) {
      console.error("Error cargando horarios", err);
    }
  }

  // 3) Enviar cita
  submitBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const payload = {
      id_programacion: horarioSelect.value,
      id_paciente: 2, // ⚠️ aquí deberías poner el paciente logueado
      estado: "programada"
    };

    try {
      const resp = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/api/cita_medica/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
      alert("Cita agendada con éxito. ID: " + data.id_cita);
    } catch (err) {
      console.error("Error creando cita", err);
      alert("Error al agendar la cita");
    }
  });

  // Inicializar
  cargarEspecialidades();
  fechaInput.addEventListener("change", cargarHorarios);
  especialidadSelect.addEventListener("change", cargarHorarios);
});
