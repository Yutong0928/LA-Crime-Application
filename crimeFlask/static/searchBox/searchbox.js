$(document).ready(function () {
    let lat;
    let lng;

    // search bar part
    $("#search").on("keypress", function (e) {
        if (e.keyCode == 13) {
            // define the api key and address
            let address = this.value;
            const myAPIKey = 'keys';

            // return the location
            const geocodingUrl = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${myAPIKey}`;
            fetch(geocodingUrl).then(result => result.json())
                .then(featureCollection => {
                    lat = featureCollection.results[0].geometry.location.lat;
                    lng = featureCollection.results[0].geometry.location.lng;
                    console.log(lat);
                    requestCrime();
                });
        }
    });

    // current location part
    $(".curLocation").on("click", function () {
        // option
        let options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        };

        // success function
        function success(pos) {
            let crd = pos.coords;
            lat = crd.latitude;
            lng = crd.longitude;
            requestCrime();
        }

        // error function
        function error(err) {
            alert('ERROR(' + err.code + '): ' + err.message);
        }

        navigator.geolocation.getCurrentPosition(success, error, options);
    });

    function requestCrime() {
        if (lat != null && lng != null) {
            $.ajax({
                url: "/search",
                method: 'post',
                data: {
                    'isAjax': true,
                    'latitude': lat,
                    'longitude': lng,
                },
                success: function (args) {
                    console.log(args);
                    if (args.code == 1000) {
                        // jump to crime
                        window.location.href = args.url;
                    } else {
                        alert(args.msg);
                    }
                }
            })
        }
    }
})