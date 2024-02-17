let colorscheme_button = document.querySelector(".main__colorscheme-button");

button.addEventListener('click', (event) => {
	event.preventDefault();
	alert("Es por decoración, no he implementado un cambio de color todavía 😛.");
});

function copyMailAddress() {
	navigator.clipboard.writeText("eriklazaroucenik@gmail.com");
	alert("Mail address copied to clipboard.");
}
