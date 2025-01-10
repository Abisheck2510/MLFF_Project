$(document).ready(function() {
    $("#compare-plates-btn").click(function() {
        $(this).toggleClass('on');
        
        const isToggleOn = $(this).hasClass('on');
        const statusHeaderExists = $('#data-table thead tr th:contains("Status")').length > 0;

        if (isToggleOn) {
            // Logic when toggle is ON: Make API call and display Status column
            $.ajax({
                url: "/compare-plates",
                type: "GET",
                success: function (result) {
                    console.log("Comparison successful:", result);

                    // Add Status Header if it doesn't exist
                   if (!statusHeaderExists){
                      $('#data-table thead tr').append('<th>Status</th>');
                    }
                    
                    // Process each row and update status
                     $('#data-table tbody tr').each(function (index) {
                        let row = result[index]
                         if (row)
                          {
                                $(this).append(`<td>${row.status}</td>`);
                          }
                      });


                    alert("Plates compared successfully!");
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.error("Error during comparison:", textStatus, errorThrown);
                    alert("Error during plate comparison. Please check console for details.");
                }
            });
        } else {
            // Logic when toggle is OFF: Hide Status column
              if (statusHeaderExists){
                  $('#data-table thead th:contains("Status")').remove();
                  $('#data-table tbody tr').each(function () {
                       $(this).find('td:last').remove();
                  });
              }
            console.log("off");
        }
    });
});



$(document).ready(function () {
    // Fetch data from FastAPI backend

    $.ajax({
        url: "http://localhost:8000/get-mlff-data",  // Adjust URL based on your FastAPI setup
        type: "GET",
        dataType: "json",
        success: function (combined_data) {
            console.log(combined_data);
            // Populate the table with the data
            combined_data.forEach(function (row) {
                const formattedDateTime = formatDateTime(row.date_time);
                const vehicleImagePath = `/static/vehicle image/${row.vehicle_image}`;
                const numberPlateImagePath = `/static/number plate image/${row.number_plate_image}`;


                $('#data-table #entries').append(`
                    <tr>
                        <td>${row.id}</td>
                        <td>${row.fastag_id}</td>
                        <td>${formattedDateTime}</td>
                        <td>${row.lane_camera_id}</td>
                        <td>${row.colour}</td>
                        <td>${row.vehicle_name}</td>
                        <td><img src="${vehicleImagePath}" alt="Vehicle Image" style="width: 100px; height: auto;"></td>
                        <td><img src="${numberPlateImagePath}" alt="Number Plate Image" style="width: 100px; height: auto;"></td>
                        <td>${row.vehicle_plate_number}</td>
                        <td>${row.vehicle_registration_number}</td>
                    </tr>
                `);
            });
        },
        error: function (error) {
            console.log("Error fetching data:", error);
        }
    });

    // Filtering functionality
    $("#search-id, #search-fastag-id, #search-datetime, #search-vehicle, #search-lane, #search-status").on("input", function () {
        filterTable();
    });

    function filterTable() {
        const minCharacters = 1; // Minimum characters before filtering
        const searchId = $("#search-id").val().toLowerCase();
        const searchFastagId = $("#search-fastag-id").val().toLowerCase();
        const searchDateTime = $("#search-datetime").val();
        const searchLane = $("#search-lane").val().toLowerCase();
        const searchVehicle = $("#search-vehicle").val().toLowerCase();
        const searchStatus = $("#search-status").val().toLowerCase();

        $("#data-table tbody tr").each(function () {
            const row = $(this);
            const id = row.find("td").eq(0).text().toLowerCase(); // ID column
            const fastagId = row.find("td").eq(1).text().toLowerCase();
            const dateTime = row.find("td").eq(2).text();
            const lane = row.find("td").eq(3).text().toLowerCase(); // Lane column
            const vehicle = row.find("td").eq(5).text().toLowerCase(); // Vehicle column
            const status = row.find("td").eq(10).text().toLowerCase(); // Status column

            const formattedSearchDateTime = searchDateTime
                ? formatDateTime(searchDateTime.replace("T", " "))
                : "";

            // Check if input has at least the minimum characters
            const isIdMatch = searchId.length < minCharacters || id.includes(searchId);
            const isFastagIdMatch = searchFastagId.length < minCharacters || fastagId.includes(searchFastagId);
            const isDateTimeMatch = searchDateTime.length < minCharacters || dateTime.includes(formattedSearchDateTime);
            const isVehicleMatch = searchVehicle.length < minCharacters || vehicle.includes(searchVehicle);
            const isLaneMatch = searchLane.length < minCharacters || lane.includes(searchLane);
            const isStatusMatch = searchStatus.length < minCharacters || status.includes(searchStatus);

            // Show or hide row based on conditions
            if (isIdMatch && isFastagIdMatch && isDateTimeMatch && isVehicleMatch && isLaneMatch && isStatusMatch) {
                row.show();
            } else {
                row.hide();
            }
        });
    }

    function formatDateTime(dateTime) {
        if (!dateTime) return "";
        const dateObj = new Date(dateTime);
        const day = String(dateObj.getDate()).padStart(2, "0");
        const month = String(dateObj.getMonth() + 1).padStart(2, "0");
        const year = dateObj.getFullYear();
        const hours = String(dateObj.getHours()).padStart(2, "0");
        const minutes = String(dateObj.getMinutes()).padStart(2, "0");
        const seconds = String(dateObj.getSeconds()).padStart(2, "0");
        return `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`;
    }
});

//     // Filtering functionality
//     $('#search-id, #search-vehicle, #search-lane, #search-status').on('input', function() {
//         filterTable();
//     });

//     function filterTable() {
//         let searchId = $('#search-id').val().toLowerCase();
//         let searchVehicle = $('#search-vehicle').val().toLowerCase();
//         let searchLane = $('#search-lane').val().toLowerCase();
//         let searchVrn = $('#search-status').val().toLowerCase();

//         $('#data-table tbody tr').each(function() {
//             let row = $(this);
//             let id = row.find('td').eq(0).text().toLowerCase();
//             let vehicle = row.find('td').eq(2).text().toLowerCase();
//             let lane = row.find('td').eq(4).text().toLowerCase();
//             let vrn = row.find('td').eq(6).text().toLowerCase();

//             if (
//                 id.includes(searchId) &&
//                 vehicle.includes(searchVehicle) &&
//                 lane.includes(searchLane) &&
//                 vrn.includes(searchVrn)
//             ) {
//                 row.show();
//             } else {
//                 row.hide();
//             }
//         });
//     }
// });

// <td><img src="/static/vehicle_images/2_1001-.jpg" alt="Vehicle Image" style="width: 100px; height: auto;"></td>
// <td><img src="/static/number_plate_images/2_1001.jpg" alt="Number Plate Image" style="width: 100px; height: auto;"></td>