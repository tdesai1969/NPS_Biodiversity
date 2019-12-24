'use strict';

$(function () {
    //Pass park_code into this function from leaflet, when ready.
    loadSpecies('BIBE');
});

function loadSpecies(park_code) {
    var speciesUrl = `${BaseApiUrl}/park/${park_code}/species`;
    $.ajax({
        url: speciesUrl,
        success: function (data) {
            // Table select
            var table_body = $('#species-rows');
            table_body.html('');

            // Append rows in the table
            data.forEach(element => {
                var row =
                 `
                <tr>
                    <th scope="row">${element.speciesID}</th>
                    <td>${element.scientificName}</td>
                    <td>${element.family}</td>
                    <td>${element.category}</td>
                    <td>${element.speciesOrder}</td>
                </tr>
                `

                table_body.append(row);
            });
        }
    });
}