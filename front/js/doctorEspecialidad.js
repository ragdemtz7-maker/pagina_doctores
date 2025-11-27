<script>
  const doctorEspecialidadMap = {
    "Patricia Conde": "Pediatría",
    "Martha Zamora": "Ginecología",
    "Manuel Lara": "Cardiología",
    "Eduardo Pérez": "Gastroenterología",
    "Joaquín Oropeza": "Médico General"
  };

  const especialidadDoctorMap = Object.entries(doctorEspecialidadMap).reduce((acc, [doctor, especialidad]) => {
    acc[especialidad] = doctor;
    return acc;
  }, {});
</script>
