'use strict';
// show map using Leaflet library. (L comes from the Leaflet library)
const map = L.map('map', {tap: false});

L.tileLayer('https:{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);

const apiurl = 'http://127.0.0.1:5000';
let playerRange;
const moves = [];

// Create a marker bubble icon
const orangeIcon = L.icon({
        iconUrl: "img/oranssi.png",
        iconSize: [25, 40],
        iconAnchor: [12, 41],
        popupAnchor: [0, -35]
    });

const blueIcon = L.icon({
    iconUrl: "img/sininen.png",
    iconSize: [25, 40],
    iconAnchor: [12, 41],
    popupAnchor: [0, -35]
});

const greenIcon = L.icon({
    iconUrl: "img/vihre.png",
    iconSize: [25, 40],
    iconAnchor: [12, 41],
    popupAnchor: [0, -35]
});


// function to fetch data from API
async function getData(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('Inlavid server input');
  }
  const data = await response.json();
  return data
}
const playerForm = document.getElementById('player-form');
const playerNameInput = document.getElementById('player-input');
const playerTypeSelect = document.getElementById('player-type');
const welcomeMessage = document.querySelector('.welcome-message');
const welcomeBackMessage = document.querySelector('.welcome-back');
const playerNameSpan = document.getElementById('player-name');
const gameEndpoint = 'https://example.com/game';

playerForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const playerType = playerTypeSelect.value;
  const playerName = playerNameInput.value.trim();

  // Perform any necessary processing on the player name and type
  // ...

  // Send a request to the server to create a new player, if necessary
  if (playerType === 'new') {
    fetch(`${gameEndpoint}/players`, {
      method: 'POST',
      body: JSON.stringify({ name: playerName }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      // Handle successful player creation
      // ...
    })
    .catch(error => {
      // Handle player creation error
      // ...
    });
  }

  // Hide the player form and display the welcome message
  playerForm.style.display = 'none';
  welcomeMessage.style.display = 'block';

  // Hide or show the welcome back message based on whether the player is new or returning
  if (playerType === 'returning') {
    welcomeBackMessage.style.display = 'block';
    playerNameSpan.textContent = playerName;
  } else {
    welcomeBackMessage.style.display = 'none';
  }

  // Set up the game with the player name and API endpoint
  const apiurl = 'http://127.0.0.1:5000';
  const gameSetup = async (url) => {
    try {
      const response = await fetch(url);
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };
  document.querySelector('#welcome-button').addEventListener('click', () => {
    document.querySelector('.welcome-message').classList.add('hidden');
    gameSetup(`${apiurl}/newgame?player=${playerName}`);
  });
});

// function to update game info
function updateGame(game) {
  document.querySelector('#player-name').innerHTML = game.name;
  document.querySelector('#p-flight').innerHTML = game.flight;
  document.querySelector('#p-range').innerHTML = game.range;
  let currentToDiamond = document.querySelector('#goal-distance');
  if (game.distance_to_goal <= 300) {
    currentToDiamond.innerHTML = " 0 - 300 km.";
  } else if (game.distance_to_goal > 300 && game.distance_to_goal <= 500) {
    currentToDiamond.innerHTML = " 300 - 500 km.";
  } else if (game.distance_to_goal > 500 && game.distance_to_goal <= 800) {
    currentToDiamond.innerHTML = " 500 - 800 km.";
  } else if (game.distance_to_goal > 800 && game.distance_to_goal <= 1000) {
    currentToDiamond.innerHTML = " 800 - 1000 km.";
  } else if (game.distance_to_goal > 1000 && game.distance_to_goal <= 1500) {
    currentToDiamond.innerHTML = " 1000 - 1500 km.";
  } else if (game.distance_to_goal > 1500 && game.distance_to_goal <= 2000) {
    currentToDiamond.innerHTML = " 1500 - 2000 km.";
  } else if (game.distance_to_goal > 2000 && game.distance_to_goal <= 2500) {
    currentToDiamond.innerHTML = " 2000 - 2500 km.";
  } else if (game.distance_to_goal > 2500) {
    currentToDiamond.innerHTML = " yli 2500 km.";
  } else {
    currentToDiamond.innerHTML = "abc";
  }
}

const submitBut = document.querySelector('#task-submit');


// function to show game task
function updateTask(task) {
  const taskE = document.querySelector('#task');
  taskE.value = task.name;
}
const p = document.createElement('p');
function checkTask(task, range) {
  const answer = document.querySelector('#answer').value;
  const parentTr = document.querySelector('#task-submit').parentNode;
  const button = document.querySelector('#task-submit');
  if (parseInt(answer) === task.answer) {
    p.innerHTML = "Oikein! Saat 500 km:ä!";
    range += 500;
    parentTr.insertBefore(p, button);
  } else if (parseInt(answer) !== task.answer) {
    p.innerHTML = "Väärin! Menetät 50 km:ä";
    parentTr.insertBefore(p, button);
    range -= 50;
  } else {
    p.innerHTML = "ABS!";
    parentTr.insertBefore(p, button);
  }
  //console.log(range);
  return range
}

// function to check if game over
function checkGameOver(flight, rangeToFly) {
  if (flight === 0) {
    console.log('Lennot on loppunut!');
    modalTitle.innerHTML = 'Game over!';
    dialogImg.src = 'img/game_over.gif';
    modalText.innerHTML = `Lennot ovat loppuneet. <br>
        Ikävä, et löysi timantin tällä kerralla. Kokeilla uudestaan!`
    return true
  } else if (rangeToFly === false) {
    console.log('Ei riittäviä kilometrejä lentämiseen');
    modalTitle.innerHTML = 'Game over!';
    dialogImg.src = 'img/game_over.gif';
    modalText.innerHTML = `Sinulla ei ole riittävää kilometriä lentämiseen. <br>
        Ikävä, et löysi timantin tällä kerralla. Kokeilla uudestaan!`;
    return true
  }
  return false
}

// check if player went to the airport that has diamond, current & diamond on airport code
function checkGameWin(current, diamond) {
  if (current === diamond) {
    console.log(current, diamond);
    console.log('You won.');
    modalTitle.innerHTML = 'Onnea! Voitit pelin!';
    modalText.innerHTML = '';
    dialogImg.src = 'img/win.jpg';
    return true;
  }
  return false;
}


// function for game start
async function gameSetup(url) {
  try {
    const gameData = await getData(url);
    console.log(gameData);
    updateGame(gameData.game);
    updateTask(gameData.task);
    let gameWin = checkGameWin(gameData.game.player_loc.ident,gameData.game.diamond.location);
    console.log(checkGameWin(gameData.game.player_loc.ident,gameData.game.diamond.location));

    let playerRange = gameData.game.range;
    submitBut.addEventListener('click', function(evt) {
      playerRange = checkTask(gameData.task, gameData.game.range);
      document.querySelector('#p-range').innerHTML = playerRange;
    })
    for (let airport of gameData.airports) {
      const marker = L.marker([airport.latitude_deg, airport.longitude_deg]).addTo(map);
        if (airport.active) {
          map.flyTo([airport.latitude_deg, airport.longitude_deg], 7);
          marker.bindPopup(`Olet tässä ${airport.name}, ${airport.country_name} `)
          marker.openPopup()
          marker.setIcon(greenIcon);
          moves.push(airport);
        } else {
          marker.setIcon(blueIcon);
          //marker.bindPopup(`${airport.name}. <br>Etäisyys sijainista noin ${airport.distance} km`);
          const popupContent = document.createElement('div');
          const h4 = document.createElement('h4');
          h4.innerHTML = `${airport.name} - lentolenttä`;
          popupContent.append(h4);
          const goButton = document.createElement('button');
          goButton.classList.add('button');
          goButton.innerHTML = 'Lennä tänne';
          popupContent.append(goButton);
          const p = document.createElement('p');
          p.innerHTML = `Etäisyys ${airport.distance} km`;
          popupContent.append(p);
          marker.bindPopup(popupContent);
          goButton.addEventListener('click', function (evt) {
            evt.stopPropagation();
            evt.preventDefault();
            if (playerRange < airport.distance) {
              marker.bindPopup(`Sinulla ei ole riittävästi kilometrejä lentääksesi tänne!`);
            } else if (gameData.game.flight === 0) {
              marker.bindPopup(`Sinulla ei ole riittävää lentoa.`);
            } else if (gameWin) {
              marker.bindPopup(`Voitit jo tällä kertaa.`);
            } else {
              // player's new range and flight
              playerRange = playerRange - airport.distance;
              let playerFlight = gameData.game.flight - 1;

              // call flyto api http://127.0.0.1:5000/flyto?game=30&dest=EFPO&range=700&flight=14
              gameSetup(`${apiurl}/flyto?game=${gameData.game.id}
              &dest=${airport.ident}&range=${playerRange}&flight=${playerFlight}`);
            }
          });
        }
    }
    if (gameWin) {
      dialog.showModal();
      return
    }
    if (checkGameOver(gameData.game.flight, gameData.game.range_to_flight)) {
      console.log('Game over');
      modalText.innerHTML += `<br>Timantti sijaitsi ${gameData.game.diamond.airport_name}. `;
      dialog.showModal();
      return
    }

  } catch (error) {
    console.log(error);
  }
}


// gameSetup('http://127.0.0.1:5000/newgame?player=Martti');





