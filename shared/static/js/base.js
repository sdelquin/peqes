document.addEventListener("DOMContentLoaded", function () {
  const disclaimer = document.querySelector("#disclaimer");
  const deleteButton = document.querySelector("#disclaimer .delete");

  // Verificar si el mensaje ya fue cerrado en esta sesión
  if (sessionStorage.getItem("disclaimerClosed") !== "true") {
    disclaimer.style.display = "block";
  }

  // Evento para cerrar el mensaje
  if (deleteButton) {
    deleteButton.addEventListener("click", function () {
      disclaimer.style.display = "none"; // Ocultar el mensaje
      sessionStorage.setItem("disclaimerClosed", "true"); // Guardar en la sesión
    });
  }
});
