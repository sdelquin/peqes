htmx.onLoad((content) => {
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

  document
    .querySelector("span#copyURL>i")
    .addEventListener("click", (event) => {
      const url = document.querySelector("span#shortenURL").textContent;
      navigator.clipboard.writeText(url).then(() => {
        const classes = [
          "has-text-success",
          "fa-clipboard-check",
          "opacity-100",
        ];
        const button = event.target;
        button.classList.add(...classes);
        setTimeout(() => {
          button.classList.remove(...classes);
        }, 2000);
      });
    });
});
