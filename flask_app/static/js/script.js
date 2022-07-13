let images = ["static/images/augusta.jpeg", "static/images/sawgrass.jpeg",
    "static/images/standrews.jpeg"];
let currentImage = 0;

function goForward(){
    currentImage += 1;

    if(currentImage >= images.length){
        currentImage = 0
    }
    document.getElementById("imageclick").src = images[currentImage];
}

function goBack(){
    currentImage -= 1;
    if(currentImage < 0){
        currentImage = 2
    }
    document.getElementById("imageclick").src = images[currentImage];
}


function add1() {
    var count = 0
    var countElement = document.querySelector("#count");
    count ++;
    countElement.innerText = count + " like(s)"
}

const x = document.getElementById("demo");

function getLocation() {
    try {
        navigator.geolocation.getCurrentPosition(showPosition);
    } catch {
        x.innerHTML = err;
    }
}

function showPosition(position) {
    x.innerHTML = "Latitude: " + position.coords.latitude +
        "<br>Longitude: " + position.coords.longitude;
}

function getData(){
    const axios = require("axios");

    const options = {
        method: 'GET',
        url: 'https://golf-course-finder.p.rapidapi.com/courses',
        params: {radius: '20', lat: '35.2271', lng: '-80.8431'},
        headers: {
            'X-RapidAPI-Key': 'ab1d09bf4amsh840dd08b280b8bep193c9fjsn83507321505a',
            'X-RapidAPI-Host': 'golf-course-finder.p.rapidapi.com'
        }
    };
    axios.request(options).then(function (response) {
        console.log(response.data);
    }).catch(function (error) {
        console.error(error);
    });
}