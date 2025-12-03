document.addEventListener("DOMContentLoaded", () => {
  const tablaCitas = document.getElementById("tablaCitas");
  const medicoModal = document.getElementById("medicoModal");
  const medicoModalBody = document.getElementById("medicoModalBody");

  // Cache
  let programacionesCache = null;
  const medicoCache = new Map(); // id_medico -> datos

  // Utilidad para convertir segundos a hora
  function segundosAHora(segundos) {
    const h = Math.floor(segundos / 3600)
      .toString()
      .padStart(2, "0");
    const m = Math.floor((segundos % 3600) / 60)
      .toString()
      .padStart(2, "0");
    return `${h}:${m}`;
  }

  async function obtenerProgramaciones() {
    if (programacionesCache) return programacionesCache;
    const resp = await fetch(
      "https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/programacion/listar"
    );
    if (!resp.ok) throw new Error("Error cargando programaciones");
    programacionesCache = await resp.json();
    return programacionesCache;
  }

  async function obtenerMedico(idMedico) {
    if (medicoCache.has(idMedico)) return medicoCache.get(idMedico);
    const resp = await fetch(
      `https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/medico/${idMedico}`
    );
    if (!resp.ok) throw new Error("Error cargando médico");
    const data = await resp.json();
    medicoCache.set(idMedico, data);
    return data;
  }

  async function obtenerCita(idCita) {
    const resp = await fetch(
      `https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/cita_medica/${idCita}`
    );
    if (!resp.ok) throw new Error("Error cargando cita");
    return await resp.json();
  }

  function renderMedicoEnModal(medico, cita, prog) {
    const contenido = `
      <div>
        <p><strong>Nombre:</strong> Dr(a). ${medico.nombre} ${
      medico.apellido
    }</p>
        <p><strong>Documento:</strong> ${medico.num_documento}</p>
        <p><strong>Correo:</strong> ${medico.correo}</p>
        <p><strong>Teléfono:</strong> ${medico.telefono}</p>
        <p><strong>Dirección:</strong> ${medico.direccion}</p>
        <hr>
        <p><strong>Fecha cita:</strong> ${cita.fecha}</p>
        <p><strong>Horario:</strong> ${segundosAHora(
          cita.hora_inicio
        )} - ${segundosAHora(cita.hora_fin)}</p>
        <p><strong>Programación:</strong> ${
          prog
            ? `${prog.id_programacion} (${segundosAHora(
                prog.hora_inicio
              )} - ${segundosAHora(prog.hora_fin)})`
            : "N/A"
        }</p>
      </div>
    `;
    medicoModalBody.innerHTML = contenido;
    // Mostrar modal (Bootstrap)
    $(medicoModal).modal("show");
  }

  async function handleRowClick(e) {
    const fila = e.target.closest("tr");
    if (!fila) return;
    const idCita = fila.getAttribute("data-idcita");
    if (!idCita) return;

    // Feedback mínimo en la fila mientras carga
    fila.classList.add("table-active");

    try {
      const [cita, programaciones] = await Promise.all([
        obtenerCita(idCita),
        obtenerProgramaciones(),
      ]);
      const prog = programaciones.find(
        (p) => p.id_programacion === cita.id_programacion
      );
      if (!prog) throw new Error("Programación no encontrada");
      const medico = await obtenerMedico(prog.id_medico);
      renderMedicoEnModal(medico, cita, prog);
    } catch (err) {
      console.error("Error mostrando datos del médico:", err);
      medicoModalBody.innerHTML = `<p>No se pudo cargar la información del médico. Intenta de nuevo.</p>`;
      $(medicoModal).modal("show");
    } finally {
      fila.classList.remove("table-active");
    }
  }

  // Delegación de eventos: click en cualquier fila de la tabla
  tablaCitas.addEventListener("click", handleRowClick);
});
