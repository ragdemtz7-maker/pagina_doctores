document.addEventListener("DOMContentLoaded", () => {
  const especialidadSelect = document.getElementById("especialidadSelect");
  const medicoSelect = document.getElementById("medicoSelect");
  const programacionSelect = document.getElementById("programacionSelect");
  const horarioSelect = document.getElementById("horarioSelect");
  const fechaInput = document.getElementById("datepicker");

  let programacionesCache = [];

  function segundosAHora(segundos) {
    const h = Math.floor(segundos / 3600).toString().padStart(2, "0");
    const m = Math.floor((segundos % 3600) / 60).toString().padStart(2, "0");
    return `${h}:${m}`;
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

  // Filtrar médicos por especialidad
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
        const especialidades = await respEsp.json();
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
      opt.value = idProg;
      opt.textContent = `${segundosAHora(hIni)} - ${segundosAHora(hFin)}`;
      horarioSelect.appendChild(opt);
    }
    $("#horarioSelect").niceSelect("update");
  }

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
