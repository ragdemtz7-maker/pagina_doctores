document.addEventListener("DOMContentLoaded", () => {
  // Modales y elementos
  const loginModal = document.getElementById("loginModal");
  const registerModal = document.getElementById("registerModal");
  const loginForm = document.getElementById("loginForm");
  const openLogin = document.getElementById("openLoginModal");
  const openRegister = document.getElementById("openRegisterModal");
  const closeButtons = document.querySelectorAll(".close-button");
  const logoutBtn = document.getElementById("logoutBtn"); // <li id="logoutBtn">

  // Abrir modales
  openLogin?.addEventListener("click", () => (loginModal.style.display = "block"));
  openRegister?.addEventListener("click", () => (registerModal.style.display = "block"));

  // Cerrar modales con botón
  closeButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const modal = btn.getAttribute("data-modal");
      const el = document.getElementById(modal);
      if (el) el.style.display = "none";
    });
  });

  // Cerrar modales por click fuera
  window.addEventListener("click", (event) => {
    if (event.target === loginModal) loginModal.style.display = "none";
    if (event.target === registerModal) registerModal.style.display = "none";
  });

  // Mostrar/ocultar login, registro y logout según sesión
  const token = localStorage.getItem("userPatient");
  if (token) {
    // Ocultar login y registro
    if (openLogin) openLogin.style.display = "none";
    if (openRegister) openRegister.style.display = "none";
    // Mostrar logout
    if (logoutBtn) logoutBtn.style.display = "block";

    logoutBtn?.addEventListener("click", () => {
      localStorage.clear();
      window.location.href = "index.html"; // redirige al home
    });
  } else {
    // Usuario no logueado
    if (openLogin) openLogin.style.display = "block";
    if (openRegister) openRegister.style.display = "block";
    if (logoutBtn) logoutBtn.style.display = "none";
  }

  // Login (JWT simulado)
  loginForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;

    if (!email || password.length < 8) {
      alert("Error en crdenciales, revisa usuario y contraseña");
      return;
    }

    try {
      // Buscar paciente
      const pacientesRes = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/paciente");
      if (!pacientesRes.ok) throw new Error(`HTTP ${pacientesRes.status}`);
      const pacientes = await pacientesRes.json();
      const paciente = pacientes.find((p) => p.correo === email);
      if (!paciente) {
        alert("Paciente no encontrado");
        return;
      }

      // Buscar usuario
      const usuariosRes = await fetch("https://1w19wlsa1d.execute-api.us-east-2.amazonaws.com/prod/api/usuario");
      if (!usuariosRes.ok) throw new Error(`HTTP ${usuariosRes.status}`);
      const usuarios = await usuariosRes.json();
      const usuario = usuarios.find((u) => u.correo === email);
      if (!usuario) {
        alert("Usuario no encontrado");
        return;
      }

      // Validar id_cognito (UUID)
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
      if (!uuidRegex.test(usuario.id_cognito)) {
        alert("id_cognito inválido");
        return;
      }

      // JWT simulado
      const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
      const payload = btoa(
        JSON.stringify({
          id_usuario: usuario.id_usuario,
          id_cognito: usuario.id_cognito,
          rol: usuario.rol,
          id_persona: usuario.id_persona,
          nombre: usuario.nombre,
          apellido: usuario.apellido,
          num_documento: usuario.num_documento,
          correo: usuario.correo,
          telefono: usuario.telefono,
          direccion: usuario.direccion,
          id_paciente: paciente.id_paciente,
          fecha_nacimiento: paciente.fecha_nacimiento,
          iat: Math.floor(Date.now() / 1000),
          exp: Math.floor(Date.now() / 1000) + 60 * 60,
        })
      );
      const signature = btoa("fake_signature");
      const jwt = `${header}.${payload}.${signature}`;

      localStorage.setItem("userPatient", jwt);
      window.location.reload();
    } catch (err) {
      console.error(err);
      alert("Error en el proceso de login simulado");
    }
  });
});
