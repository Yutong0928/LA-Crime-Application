$(document).ready(function () {
    let typeCrime = [];
    function requestType() {
        $.ajax({
            url: "/typeCrime",
            method: 'get',
            async: false,
            success: function (args) {
                if (args.code == 1000) {
                    typeCrime = args.typeCrime;
                } else {
                    alert(args.msg);
                }
            }
        })
    }
    requestType();
    // Initialize the echarts instance based on the prepared dom
    let myChart = echarts.init(document.getElementById('typeCrm'));
    window.onresize = function () {
        myChart.resize();
    }
    let type_crime = {
        series: [
            {
                type: 'pie',
                data: [
                    {
                        value: typeCrime[0],
                        name: 'theft'
                    },
                    {
                        value: typeCrime[1],
                        name: 'sexual'
                    },
                    {
                        value: typeCrime[2],
                        name: 'assault'
                    },
                    {
                        value: typeCrime[3],
                        name: 'burglary'
                    },
                    {
                        value: typeCrime[4],
                        name: 'robbery'
                    },
                    {
                        value: typeCrime[5],
                        name: 'vandalism'
                    },
                    {
                        value: typeCrime[6],
                        name: 'vehicle'
                    },
                    {
                        value: typeCrime[7],
                        name: 'others'
                    },
                ],
                roseType: 'area'
            }
        ]
    };
    myChart.setOption(type_crime);
})