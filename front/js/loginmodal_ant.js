document.addEventListener("DOMContentLoaded", () => {
  const modals = {
    loginModal: document.getElementById("loginModal"),
    registerModal: document.getElementById("registerModal")
  };

  const openLoginBtn = document.getElementById("openLoginModal");
  const openRegisterBtn = document.getElementById("openRegisterModal");

  const closeButtons = document.querySelectorAll(".close-button");

  const openModal = (modalId) => {
    modals[modalId].style.display = "block";
  };

  const closeModal = (modalId) => {
    modals[modalId].style.display = "none";
  };

  openLoginBtn.addEventListener("click", () => openModal("loginModal"));
  openRegisterBtn.addEventListener("click", () => openModal("registerModal"));

  closeButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const modalId = btn.getAttribute("data-modal");
      closeModal(modalId);
    });
  });

  window.addEventListener("click", (event) => {
    Object.keys(modals).forEach(modalId => {
      if (event.target === modals[modalId]) {
        closeModal(modalId);
      }
    });
  });

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      Object.keys(modals).forEach(modalId => {
        if (modals[modalId].style.display === "block") {
          closeModal(modalId);
        }
      });
    }
  });
});