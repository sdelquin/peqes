htmx.onLoad((content) => {
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
