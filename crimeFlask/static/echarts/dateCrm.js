$(document).ready(function () {

    let month20 = [];
    let month21 = [];
    let month22 = [];
    let dayDistribution = [];
    let days = new Array(31);
    for (let i = 0; i < days.length; i++) {
        days[i] = i + 1;
    }

    function requestDate() {
        $.ajax({
            url: "/dateCrime",
            method: 'get',
            async: false,
            success: function (args) {
                if (args.code == 1000) {
                    month20 = args.month20;
                    month21 = args.month21;
                    month22 = args.month22;
                    dayDistribution = args.dayDistribution;
                } else {
                    alert(args.msg);
                }
            }
        })
    }

    requestDate();

    // Initialize the echarts instance based on the prepared dom
    let myChart = echarts.init(document.getElementById('month_crime'));
    let myChart1 = echarts.init(document.getElementById('day_crime'));
    window.onresize = function () {
        myChart.resize();
    }
    let month_crime = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {type: 'cross'}
        },
        legend: {},
        xAxis: [
            {
                type: 'category',
                axisTick: {
                    alignWithLabel: true
                },
                data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                ]
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: 'Crime',
                position: 'left',
                axisLabel: {
                    formatter: '{value}'
                }
            },
        ],
        series: [
            {
                data: month20,
                type: 'bar',
                name: '2020',
                stack: 'x'
            },
            {
                data: month21,
                type: 'bar',
                name: '2021',
                stack: 'x'
            },
            {
                data: month22,
                type: 'bar',
                name: '2022',
                stack: 'x'
            },
        ]
    };
    let day_crime = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {type: 'cross'}
        },
        legend: {},
        xAxis: [
            {
                type: 'category',
                axisTick: {
                    alignWithLabel: true
                },
                data: days
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: 'Crime',
                position: 'left',
                axisLabel: {
                    formatter: '{value}'
                }
            },
        ],
        series: [
            {
                data: dayDistribution,
                type: 'line',
                smooth: true,
                lineStyle: {
                    normal: {
                        color: 'lightblue',
                        width: 4,
                    }
                },
            },
        ]
    };

    // draw the chart
    myChart.setOption(month_crime);
    myChart1.setOption(day_crime);
})