//Get the modal
const loginModal = document.getElementById("loginModal");

//Get the button that opens the modal
const openLoginBtn = document.getElementById("openLoginModal");

//Get the <span>
const closeBtn = document.querySelector(".close-button");

//When the user clicks the button, open the modal
openLoginBtn.onclick =function() {
    loginModal.style.display = "block";
}

//when the user clicks on span, close the modal
closeBtn.onclick = function() {
    loginModal.style.display = "none";
}

//when the user clicks anywhere outside the modal, close it
window.onclick = function(event) {
    if (event.target === loginModal) {
        loginModal.style.display = "none";
    }
};
