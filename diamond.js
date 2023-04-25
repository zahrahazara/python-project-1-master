// Get references to the HTML elements
const lentomaara = document.getElementById("lentomäärä");
const kilometrimaara = document.getElementById("kilometrimäärä");
const playerName = document.querySelector(".box table tr:nth-child(1) td");



// Define the player object with initial values
const player = {
  name: "",
  lentomaara: 15,
  kilometrimaara: 10000,
};
const aboutLink = document.getElementById("about-link");
const about = document.getElementById("about");

aboutLink.addEventListener("click", function(event) {
    event.preventDefault();
    about.classList.toggle("hidden");
});

// Add event listener to prompt the user to enter their name when the "Game" link is clicked
const gameLink = document.getElementById("game-link");
gameLink.addEventListener("click", function(event) {
  event.preventDefault(); // prevent the link from navigating to a new page

  player.name = prompt("Enter your name:");
  if (player.name) {
    // if the player entered a name, update the HTML and add event listener to the map
    playerName.textContent = player.name;
    map.addEventListener("click", function() {
      if (player.lentomaara > 0 && player.kilometrimaara > 0) {
        player.lentomaara--;
        player.kilometrimaara -= 500;
        lentomaara.textContent = player.lentomaara;
        kilometrimaara.textContent = player.kilometrimaara;
      } else {
        alert("Game over!");
      }
    });
  }


});
