document.addEventListener("DOMContentLoaded", () => {
  const especialidadSelect = document.getElementById("especialidadSelect");
  const medicoSelect = document.getElementById("medicoSelect");
  const programacionSelect = document.getElementById("programacionSelect");
  const horarioSelect = document.getElementById("horarioSelect");
  const fechaInput = document.getElementById("datepicker");
  const submitBtn = document.getElementById("agendar");
  const appointmentBox = document.querySelector(".appointment_box");

  const emailInput = document.getElementById("citaCorreo");
  const nameInput = document.getElementById("citaNombre");
  const telefonoInput = document.getElementById("citaTelefono");

  let programacionesCache = [];

  function segundosAHora(segundos) {
    const h = Math.floor(segundos / 3600).toString().padStart(2, "0");
    const m = Math.floor((segundos % 3600) / 60).toString().padStart(2, "0");
    return `${h}:${m}`;
  }

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

  function initNiceSelects() {
    $("#especialidadSelect").niceSelect();
    $("#medicoSelect").niceSelect();
    $("#programacionSelect").niceSelect();
    $("#horarioSelect").niceSelect();

    // Bridge: propagar change desde nice-select al select real
    $(document).on("click", "#especialidadSelect + .nice-select .option", function () {
      $("#especialidadSelect").val($(this).data("value")).trigger("change");
    });
    $(document).on("click", "#medicoSelect + .nice-select .option", function () {
      $("#medicoSelect").val($(this).data("value")).trigger("change");
    });
    $(document).on("click", "#programacionSelect + .nice-select .option", function () {
      $("#programacionSelect").val($(this).data("value")).trigger("change");
    });
    $(document).on("click", "#horarioSelect + .nice-select .option", function () {
      $("#horarioSelect").val($(this).data("value")).trigger("change");
    });
  }

  // Sesión
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

  // Cargar especialidades
  async function cargarEspecialidades() {
    try {
      const resp = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/especialidad/todas");
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();

      especialidadSelect.innerHTML = "<option value=''>Seleccione una especialidad</option>";
      data.forEach((item) => {
        const [id, nombre] = Array.isArray(item) ? item : [item.id_especialidad || item.id, item.nombre];
        if (id && nombre) {
          const opt = document.createElement("option");
          opt.value = id;
          opt.textContent = nombre;
          especialidadSelect.appendChild(opt);
        }
      });
      $("#especialidadSelect").niceSelect("update");
    } catch (err) {
      console.error("Error cargando especialidades", err);
    }
  }

  // Filtrar médicos por especialidad (evitar duplicados)
  async function cargarMedicosPorEspecialidad(idEspecialidad) {
    try {
      const respMed = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/medico");
      if (!respMed.ok) throw new Error(`HTTP ${respMed.status}`);
      const medicos = await respMed.json();

      medicoSelect.innerHTML = "<option value=''>Seleccione un médico</option>";
      const seen = new Set();

      for (const m of medicos) {
        const respEsp = await fetch(`https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/especialidad/medico/${m.id_medico}`);
        if (!respEsp.ok) continue;
        const especialidades = await respEsp.json(); // [[id, nombre], ...]
        const match = especialidades.find(e => String(e[0]) === String(idEspecialidad));
        if (match && !seen.has(m.id_medico)) {
          seen.add(m.id_medico);
          const opt = document.createElement("option");
          opt.value = m.id_medico;
          opt.textContent = `${m.nombre} ${m.apellido ?? ""}`.trim();
          medicoSelect.appendChild(opt);
        }
      }
      $("#medicoSelect").niceSelect("update");

      // Reset dependientes
      programacionSelect.innerHTML = "<option value=''>Seleccione una programación</option>";
      $("#programacionSelect").niceSelect("update");
      horarioSelect.innerHTML = "<option value=''>Seleccione un horario</option>";
      $("#horarioSelect").niceSelect("update");
      fechaInput.value = "";
      programacionesCache = [];
    } catch (err) {
      console.error("Error cargando médicos", err);
    }
  }

  // Programaciones por médico
  async function cargarProgramacionesPorMedico(idMedico) {
    try {
      const resp = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/programacion/listar");
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();

      programacionesCache = data.filter(p => p.id_medico === idMedico);
      programacionSelect.innerHTML = "<option value=''>Seleccione una programación</option>";

      programacionesCache.forEach((p) => {
        const opt = document.createElement("option");
        opt.value = p.id_programacion;
        opt.textContent = `${p.id_programacion} | ${p.fecha} ${segundosAHora(p.hora_inicio)} - ${segundosAHora(p.hora_fin)}`;
        opt.dataset.fecha = p.fecha;
        opt.dataset.horaInicio = p.hora_inicio;
        opt.dataset.horaFin = p.hora_fin;
        programacionSelect.appendChild(opt);
      });

      $("#programacionSelect").niceSelect("update");

      fechaInput.value = "";
      horarioSelect.innerHTML = "<option value=''>Seleccione un horario</option>";
      $("#horarioSelect").niceSelect("update");
    } catch (err) {
      console.error("Error cargando programaciones", err);
    }
  }

  // Aplicar programación seleccionada
  function aplicarProgramacionSeleccionada() {
    const idProg = programacionSelect.value;
    if (!idProg) return;

    const sel = programacionSelect.querySelector(`option[value="${idProg}"]`);
    if (!sel) return;

    const fecha = sel.dataset.fecha;
    const hIni = parseInt(sel.dataset.horaInicio, 10);
    const hFin = parseInt(sel.dataset.horaFin, 10);

    if (fecha) fechaInput.value = fecha;

    horarioSelect.innerHTML = "<option value=''>Seleccione un horario</option>";
    if (!Number.isNaN(hIni) && !Number.isNaN(hFin)) {
      const opt = document.createElement("option");
      opt.value = idProg; // Postearemos el id_programacion
      opt.textContent = `${segundosAHora(hIni)} - ${segundosAHora(hFin)}`;
      horarioSelect.appendChild(opt);
    }
    $("#horarioSelect").niceSelect("update");
  }

  // Agendar y redirigir
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

  // Inicialización
  initNiceSelects();
  cargarEspecialidades();

  // Listeners
  $("#especialidadSelect").on("change", function () {
    const idEspecialidad = this.value;
    if (idEspecialidad) {
      cargarMedicosPorEspecialidad(idEspecialidad);
    } else {
      $("#medicoSelect").html("<option value=''>Seleccione un médico</option>").niceSelect("update");
      $("#programacionSelect").html("<option value=''>Seleccione una programación</option>").niceSelect("update");
      $("#horarioSelect").html("<option value=''>Seleccione un horario</option>").niceSelect("update");
      fechaInput.value = "";
      programacionesCache = [];
    }
  });

  $("#medicoSelect").on("change", function () {
    const idMedico = parseInt(this.value, 10);
    if (idMedico) {
      cargarProgramacionesPorMedico(idMedico);
    } else {
      $("#programacionSelect").html("<option value=''>Seleccione una programación</option>").niceSelect("update");
      $("#horarioSelect").html("<option value=''>Seleccione un horario</option>").niceSelect("update");
      fechaInput.value = "";
      programacionesCache = [];
    }
  });

  $("#programacionSelect").on("change", function () {
    aplicarProgramacionSeleccionada();
  });

  $(fechaInput).on("change", function () {
    const fechaSel = this.value;
    if (!fechaSel || programacionesCache.length === 0) return;

    const matches = programacionesCache.filter(p => p.fecha === fechaSel);
    horarioSelect.innerHTML = "<option value=''>Seleccione un horario</option>";
    matches.forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.id_programacion;
      opt.textContent = `${segundosAHora(p.hora_inicio)} - ${segundosAHora(p.hora_fin)}`;
      horarioSelect.appendChild(opt);
    });
    $("#horarioSelect").niceSelect("update");
  });
});
