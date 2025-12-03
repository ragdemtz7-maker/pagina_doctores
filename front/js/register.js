document.addEventListener("DOMContentLoaded", () => {
  const registerModal = document.getElementById("registerModal");
  const openBtn = document.getElementById("openRegisterModal");
  const closeBtn = document.querySelector(".close-button");

  const openModal = () => {
    registerModal.style.display = "block";
  };

  const closeModal = () => {
    registerModal.style.display = "none";
  };

  openBtn.addEventListener("click", openModal);
  closeBtn.addEventListener("click", closeModal);

  window.addEventListener("click", (event) => {
    if (event.target === registerModal) {
      closeModal();
    }
  });
});