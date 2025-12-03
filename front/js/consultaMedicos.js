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
  }

  async function cargarEspecialidades() { /* ... igual que tu código */ }
  async function cargarMedicosPorEspecialidad(idEspecialidad) { /* ... */ }
  async function cargarProgramacionesPorMedico(idMedico) { /* ... */ }
  function aplicarProgramacionSeleccionada() { /* ... */ }

  // Inicialización
  initNiceSelects();
  cargarEspecialidades();

  // Listeners
  $("#especialidadSelect").on("change", function () {
    if (this.value) cargarMedicosPorEspecialidad(this.value);
  });
  $("#medicoSelect").on("change", function () {
    if (this.value) cargarProgramacionesPorMedico(parseInt(this.value, 10));
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
