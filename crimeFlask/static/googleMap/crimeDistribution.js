$(document).ready(function (){
    let data = [];
    const geoCoordMap = {};
    // request district names and their locations
    function requestDistrict() {
        $.ajax({
            url: "/laCities",
            method: 'get',
            async: false,
            success: function (args) {
                if (args.code == 1000) {
                    let cities = args.cities;
                    for (let i = 0; i < cities.length; i++) {
                        data.push({
                            name: cities[i][0],
                            value: 10 + cities[i][3] / 100
                        });
                        geoCoordMap[cities[i][0]] = [cities[i][2], cities[i][1]];
                    }
                } else {
                    alert(args.msg);
                }
            }
        })
    }
    requestDistrict();

    // define a function to process location data
    function convertData(data) {
        let res = [];
        for(let i = 0; i < data.length; i++) {
            let geoCoord = geoCoordMap[data[i].name];
            if (geoCoord) {
                res.push({
                    name: data[i].name,
                    value: geoCoord.concat(data[i].value)
                });
            }
        }
        return res;
    }

    // map config
    let mapOption = {
        // google map component
        gmap: {
            center: [-118.243683, 34.052235],
            zoom: 11,
            roam: true,
        },
        tooltip: {
            trigger: 'item'
        },

        animation: true,
        series: [
            {
                name: 'CRIME',
                type: 'scatter',
                // use `gmap` as the coordinate system
                coordinateSystem: 'gmap',
                // data items [[lng, lat, value], [lng, lat, value], ...]
                data: convertData(data),
                symbolSize: function (val) {
                    return val[2] / 10;
                },
                encode: {
                    value: 2,
                    lng: 0,
                    lat: 1
                },
                label: {
                    formatter: '{b}',
                    position: 'right',
                    show: false
                },
                itemStyle: {
                    color: 'orange'
                },
                emphasis: {
                    label: {
                        show: true
                    }
                }
            },
            {
                name: 'TOP 5 CRIME LOCATIONS',
                type: 'effectScatter',
                coordinateSystem: 'gmap',
                data: convertData(data.sort(function (a, b) {
                    return b.value - a.value;
                }, geoCoordMap).slice(0, 6)),
                symbolSize: function (val) {
                    return val[2] / 10;
                },
                encode: {
                    value: 2,
                    lng: 0,
                    lat: 1
                },
                showEffectOn: 'render',
                rippleEffect: {
                    brushType: 'stroke'
                },
                label: {
                    formatter: '{b}',
                    position: 'right',
                    show: true
                },
                itemStyle: {
                    color: 'red',
                    shadowBlur: 10,
                    shadowColor: '#333'
                },
                zlevel: 1
            }
        ]
    };
    // initialize chart
    let chart = echarts.init(document.getElementById("echarts-google-map"));
    chart.setOption(mapOption);
})