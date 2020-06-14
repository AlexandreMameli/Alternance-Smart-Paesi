// declaration des bibliotheques utilisees
// d3 pour la lecture des fichiers rainbow pour creer un gradient de couleurs
const d3 = require('d3-fetch')
const Rainbow = require('rainbowvis.js')

// creation du gradient de couleur et stockage dans un tableau
var numberOfItems = 1000
var rainbow = new Rainbow();
rainbow.setNumberRange(1, numberOfItems);
rainbow.setSpectrum('green', "yellow", "red");
var s = [];
for (var i = 1; i <= numberOfItems; i++) {
    var hexColour = rainbow.colourAt(i);
    s.push('#' + hexColour)
}

// parametrage et creation de la carte
var map = L.map("mapid").setView([41.935311, 9.153702], 18);
L.tileLayer(
    'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 35,
    })
.addTo(map);
// placement du marqueur representant l'antenne LoRaWAN
L.marker([41.935374, 9.153700]).addTo(map)


function pourcents(val, min, max){// nous permettra de determiner l'indice d'un rssi dans le tableau de couleurs
    return (val-min)/(max-min)
}

function tabGeoliers(matriceRssi, posI, posJ){// permet de determiner quelles zones entourent une zone donnee
    rssiNonNuls = []
    for(var i = Math.max(0,posI-1); i<=Math.min(posI+1, matriceRssi.length-1); i++)
    {
        for(var j = Math.max(0,posJ-1); j<=Math.min(posJ+1, matriceRssi[0].length-1); j++)
        {
            if(matriceRssi[i][j]!=0)
                rssiNonNuls.push(matriceRssi[i][j])
        }
    }
    return rssiNonNuls
}
function meanEmpty(geoliers)
{// si une zone ne possede pas de mesures nous permet de faire une estimation
// grace aux zone voisines possedants des mesures
    var somme = 0
    if(geoliers.length>4)
    {
        geoliers.forEach((elt) =>{
            somme+= -elt
        })
        var moyenne = somme/geoliers.length
        return moyenne
    }
    return 0

}
// bornes a partir desquelles nous allons determiner si des mesures sont exploitables
const minLat = 40
const maxLat = 42
const minLon = 9.1
const maxLon = 9.2
// valeur d'un metre en latitude et longitude a nos coordonnees
const pasLat = 0.00027
const pasLon = 0.00035
// nombre d'element sur lesquels travailler
tailleLat = Math.floor((maxLat-minLat)/pasLat)+1
tailleLon = Math.floor((maxLon-minLon)/pasLon)+1
// declaration des matrices qui permettront de determiner la moyenne du rssi sur une zone
let tabRssi = []
let tabCpt = []
// lecture du fichier contenant les donnees
d3.json('tout.json').then((eqs) => {
    // variables qui contiendrons les valeurs min et max du rssi
    // le rssi est une valeur negative nous les passon en positif pour rendre le traitement plus simple
    var minRssi = -eqs.hits.hits[0]._source.rssi
    var maxRssi = -eqs.hits.hits[0]._source.rssi
    // creation des matrices et remplissage par des 0
    for(var i = 0; i<tailleLat; i++)
    {
        tabRssi[i] = []
        tabCpt[i] = []
        for(var j = 0; j<tailleLon; j++){
            tabRssi[i][j]=0
            tabCpt[i][j]=0
        }
    }
    // recherche des min et max du rssi
    eqs.hits.hits.forEach((d) => {
        if(maxRssi<-d._source.rssi){
            maxRssi = -d._source.rssi
        }
        if(minRssi>-d._source.rssi){
            minRssi = -d._source.rssi
        }
    })
    // peut sembler redondant car s contient deja le gradient mais etrangement
    // le script ne fonctionnait pas sinon
    var testGradient = new Map()
    for(var i=0; i<1000; i++){
        testGradient.set(i,s[i])
    }
    // creation des cercles representants une mesure du rssi et remplissage des matrices
    eqs.hits.hits.forEach((d) => {
        val = pourcents(-d._source.rssi,minRssi, maxRssi)*1000
        var circle = L.circle([d._source.location[1], d._source.location[0]], {
            color: testGradient.get(Math.round(val)),
            fillColor : testGradient.get(Math.round(val)),
            fillOpacity: 0.5,
            radius: 5
        }).addTo(map);
        tabRssi[Math.floor((d._source.location[1]-minLat)/pasLat)][Math.floor((d._source.location[0]-minLon)/pasLon)] += d._source.rssi
        tabCpt[Math.floor((d._source.location[1]-minLat)/pasLat)][Math.floor((d._source.location[0]-minLon)/pasLon)] += 1
    })
    // affiche si possible les carres representant la moyenne des valeurs mesurees sur une zone
    for(var i = 0; i<tailleLat; i++)
    {
        for(var j = 0; j<tailleLon; j++){
            if(tabCpt[i][j]!=0)
            {

                tabRssi[i][j]/=tabCpt[i][j]
                if(tabRssi[i][j]!=0)
                {
                    val = pourcents(-tabRssi[i][j],minRssi, maxRssi)*1000
                    L.rectangle([[minLat+i*pasLat, minLon+j*pasLon],[minLat+(i+1)*pasLat,minLon+(j+1)*pasLon]], {color: testGradient.get(Math.round(val))}).addTo(map);
                }
            }
        }
    }
    // determine si une zone ne possedant pas de valeurs possede suffisament de voisins pour etre estimee
    // et affiche un carre barre d'une diagonale si la zone correspond aux criteres
    for(var i = 0; i<tailleLat; i++)
    {
        for(var j = 0; j<tailleLon; j++){
            var moyenneCaptif = 0
            if (tabRssi[i][j]==0){
                var geoliers = tabGeoliers(tabRssi, i, j)
                moyenneCaptif = meanEmpty(geoliers)
                val = pourcents(moyenneCaptif,minRssi, maxRssi)*1000
                if(moyenneCaptif!=0)
                {
                    L.rectangle([[minLat+i*pasLat, minLon+j*pasLon],[minLat+(i+1)*pasLat,minLon+(j+1)*pasLon]], {color: testGradient.get(Math.round(val))}).addTo(map);
                    L.polyline([[minLat+i*pasLat, minLon+j*pasLon],[minLat+(i+1)*pasLat,minLon+(j+1)*pasLon]], {color : testGradient.get(Math.round(val))}).addTo(map)
                }
            }
        }
    }
});