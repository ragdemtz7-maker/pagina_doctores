<script>
  const doctorSelect = document.getElementById("doctorSelect");
  const especialidadSelect = document.getElementById("especialidadSelect");

  doctorSelect.addEventListener("change", function () {
    const selectedDoctor = doctorSelect.value;
    const especialidad = doctorEspecialidadMap[selectedDoctor] || "";
    especialidadSelect.value = especialidad;
  });

  especialidadSelect.addEventListener("change", function () {
    const selectedEspecialidad = especialidadSelect.value;
    const doctor = especialidadDoctorMap[selectedEspecialidad] || "";
    doctorSelect.value = doctor;
  });
</script>
