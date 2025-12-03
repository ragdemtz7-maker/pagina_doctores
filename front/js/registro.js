document.addEventListener("DOMContentLoaded", () => {
  const registerModal = document.getElementById("registerModal");
  const registerForm = document.getElementById("registerForm");

  // Utilidad para generar un número aleatorio como documento (fallback)
  function randomDocumento() {
    return Math.floor(Math.random() * 1000000000).toString();
  }

  registerForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("registerEmail").value.trim();
    const nombre = document.getElementById("registerNombre").value.trim();
    const apellido = document.getElementById("registerApellido").value.trim();
    const telefono = document.getElementById("registerTelefono").value.trim();
    const direccion = document.getElementById("registerDireccion").value.trim();
    let num_documento = document.getElementById("registerDocumento").value.trim();

    // Si el usuario no escribe nada, generamos uno aleatorio
    if (!num_documento) {
      num_documento = randomDocumento();
    }

    // Payload para paciente
    const pacientePayload = {
      nombre,
      apellido,
      num_documento, // CURP o lo que el usuario haya escrito
      correo: email,
      telefono,
      direccion,
      fecha_nacimiento: "1990-01-01" // puedes agregar un campo en el formulario si quieres capturar fecha real
    };

    // Payload para usuario
    const usuarioPayload = {
      nombre,
      apellido,
      num_documento,
      correo: email,
      telefono,
      direccion,
      id_cognito: crypto.randomUUID(), // genera un UUID válido
      rol: "paciente"
    };

    try {
      // Crear paciente
      const respPaciente = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/paciente", {
        method: "POST",
        headers: { "Content-Type": "application/json", accept: "application/json" },
        body: JSON.stringify(pacientePayload),
      });

      const dataPaciente = await respPaciente.json();
      if (!respPaciente.ok) {
        console.error("Error paciente:", dataPaciente);
        alert("No se pudo registrar el paciente.");
        return;
      }

      // Crear usuario
      const respUsuario = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/usuario", {
        method: "POST",
        headers: { "Content-Type": "application/json", accept: "application/json" },
        body: JSON.stringify(usuarioPayload),
      });

      const dataUsuario = await respUsuario.json();
      if (!respUsuario.ok) {
        console.error("Error usuario:", dataUsuario);
        alert("Paciente creado, pero error al registrar usuario.");
        return;
      }

      alert("Registro exitoso. Ahora puedes iniciar sesión.");
      registerModal.style.display = "none";
    } catch (err) {
      console.error("Error en registro:", err);
      alert("Error al registrar.");
    }
  });
});
