'use strict';

$(async function () {
    var parks = await loadParkGeoJson();
    generateParkMap(parks);

    $(document).on('click', '.species-href', async (e) => {
        var parkCode = $(e.target).data('parkcode');
        await loadSpecies(parkCode);
    });

});

async function loadParkGeoJson() {
    var parkUrl = `api/park`;
    var parks = await $.ajax({
        url: parkUrl
    });
    return GeoJSON.parse(parks, {
        Point: ['latitude', 'longitude']
    });
}

function generateParkMap(parks) {
    var parkMap = L.map("map-id", {
        center: [37.0902, -95.7129],
        zoom: 3,
    });

    L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox.outdoors',
        accessToken: API_KEY
    }).addTo(parkMap);

    L.geoJson(parks, {
            pointToLayer: function (feature, latLong) {
                return L.marker(latLong);
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup(createPopup(feature.properties));
            }
        })
        .addTo(parkMap);
}

function createPopup(details) {
    return `
    <h4>${details.park_name}, ${details.state}</h4>
    <b>Code: </b>${details.park_code}<br>  
    <b>acres: </b>${details.acres}<br>
    <b>visitors: </b>${details.visitors.toFixed(0)}<br>
    <a class="species-href" href="#" data-parkcode="${details.park_code}">Species information</a>
    `;
}

async function loadSpecies(park_code) {
    var speciesUrl = `api/park/${park_code}/species`;
    var data = await $.ajax({
        url: speciesUrl
    });

    // Table select
    var table_body = $('#species-rows');
    table_body.html('');

    // Append rows in the table
    data.forEach(element => {
        var row =
            `
            <tr>
                <th scope="row">${element.common_names}</th>
                <td>${element.scientificName}</td>
                <td>${element.family}</td>
                <td>${element.category}</td>
                <td>${element.speciesOrder}</td>
            </tr>
            `

        table_body.append(row);
    });
}