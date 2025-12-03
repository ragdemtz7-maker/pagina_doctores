document.addEventListener("DOMContentLoaded", () => {
  const loginModal = document.getElementById("loginModal");
  const loginForm = document.getElementById("loginForm");
  const openLogin = document.getElementById("openLoginModal");
  const closeButtons = document.querySelectorAll(".close-button");

  // Abrir modal
  openLogin.addEventListener("click", () => {
    loginModal.style.display = "block";
  });

  // Cerrar modal
  closeButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      btn.closest(".modal").style.display = "none";
    });
  });

  window.addEventListener("click", (event) => {
    if (event.target === loginModal) loginModal.style.display = "none";
  });

  // Lógica de "login"
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    // Validar longitud de password
    if (password.length < 8) {
      alert("La contraseña debe tener al menos 8 caracteres");
      return;
    }

    try {
      // Buscar paciente
      const pacientesRes = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/paciente");
      const pacientes = await pacientesRes.json();
      const paciente = pacientes.find(p => p.correo === email);

      if (!paciente) {
        alert("Paciente no encontrado");
        return;
      }

      // Buscar usuario
      const usuariosRes = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/usuario");
      const usuarios = await usuariosRes.json();
      const usuario = usuarios.find(u => u.correo === email);

      if (!usuario) {
        alert("Usuario no encontrado");
        return;
      }

      // Validar id_cognito formato UUID simple
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
      if (!uuidRegex.test(usuario.id_cognito)) {
        alert("id_cognito inválido");
        return;
      }

      // Generar JWT simulado
      const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
      const payload = btoa(JSON.stringify({
        id_paciente: paciente.id_paciente,
        nombre: paciente.nombre,
        apellido: paciente.apellido,
        correo: paciente.correo,
        rol: usuario.rol,
        id_cognito: usuario.id_cognito
      }));
      const signature = btoa("fake_signature"); // aquí no firmamos de verdad

      const jwt = `${header}.${payload}.${signature}`;

      // Guardar en localStorage
      localStorage.setItem("userPatient", jwt);

      // Recargar página
      window.location.reload();

    } catch (err) {
      console.error(err);
      alert("Error en el proceso de login simulado");
    }
  });
});
