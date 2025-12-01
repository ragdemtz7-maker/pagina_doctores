document.addEventListener("DOMContentLoaded", () => {
  const inputs = document.querySelectorAll('.mail_text, .massage-bt');
  const submitBtn = document.getElementById('submitBtn');

  function validarCampos() {
    let todosLlenos = true;
    inputs.forEach(input => {
      if (!input.value.trim()) {
        todosLlenos = false;
      }
    });
    submitBtn.disabled = !todosLlenos;
  }

  inputs.forEach(input => {
    input.addEventListener('input', validarCampos);
  });
});
