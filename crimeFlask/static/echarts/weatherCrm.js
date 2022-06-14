$(document).ready(function () {
    let weatherDistribution = [];
    let weatherCrime = [];

    function requestWeather() {
        $.ajax({
            url: "/weatherCrime",
            method: 'get',
            async: false,
            success: function (args) {
                if (args.code == 1000) {
                    weatherDistribution = args.weatherDistribution;
                    weatherCrime = args.weatherCrime;
                } else {
                    alert(args.msg);
                }
            }
        })
    }
    requestWeather();

    // process the data
    let sum1 = weatherDistribution.reduce((a, b) => a + b, 0);
    weatherDistribution = weatherDistribution.map(x => (x/sum1) * 100);
    let sum2 = weatherCrime.reduce((a, b) => a + b, 0);
    weatherCrime = weatherCrime.map(x => (x/sum2) * 100);
    console.log(weatherDistribution);
    console.log(weatherCrime);

    // Initialize the echarts instance based on the prepared dom
    let myChart = echarts.init(document.getElementById('weatherDistribution'));
    let myChart1 = echarts.init(document.getElementById('weatherCrm'));
    let myChart2 = echarts.init(document.getElementById('compareDistribution'));
    window.onresize = function () {
        myChart.resize();
    }
    // define three panels and draw it
    let weather_distribution = {
        title: {
            text: 'weather distribution',
            left: 'center',
            top: 'center'
        },
        series: [
            {
                type: 'pie',
                radius: ['40%', '70%'],
                data: [
                    {
                        value: weatherDistribution[0],
                        name: 'fair'
                    },
                    {
                        value: weatherDistribution[1],
                        name: 'cloudy'
                    },
                    {
                        value: weatherDistribution[2],
                        name: 'rain'
                    },
                    {
                        value: weatherDistribution[3],
                        name: 'haze'
                    },
                    {
                        value: weatherDistribution[4],
                        name: 'fog'
                    },
                ],
            }
        ]
    };
    let weather_crime = {
        title: {
            text: 'crime distribution',
            left: 'center',
            top: 'center'
        },
        series: [
            {
                name: 'weather and crime',
                type: 'pie',
                radius: ['40%', '70%'],
                data: [
                    {
                        value: weatherCrime[0],
                        name: 'fair'
                    },
                    {
                        value: weatherCrime[1],
                        name: 'cloudy'
                    },
                    {
                        value: weatherCrime[2],
                        name: 'rain'
                    },
                    {
                        value: weatherCrime[3],
                        name: 'haze'
                    },
                    {
                        value: weatherCrime[4],
                        name: 'fog'
                    },
                ],
            }
        ]
    };
    let compare_distribution = {
        legend: {},
        xAxis: {
            type: 'category',
            data: ['fair', 'cloudy', 'rain', 'haze', 'fog']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: 'weather distribution',
                data: weatherDistribution,
                type: 'line'
            },
            {
                name: 'crime distribution',
                data: weatherCrime,
                type: 'line'
            }
        ]
    };
    myChart.setOption(weather_distribution);
    myChart1.setOption(weather_crime);
    myChart2.setOption(compare_distribution);
})