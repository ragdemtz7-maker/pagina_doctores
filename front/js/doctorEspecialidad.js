  const doctorEspecialidadMap = {
    "Pediatría": "Patricia Conde",
    "Ginecología": "Martha Zamora",
    "Cardiología": "Manuel Lara",
    "Gastroenterología": "Eduardo Pérez",
    "Médico General": "Joaquín Oropeza"
  };

  const especialidadDoctorMap = Object.entries(doctorEspecialidadMap).reduce((acc, [especialidad, doctor]) => {
    acc[doctor] = especialidad;
    return acc;
  }, {});

