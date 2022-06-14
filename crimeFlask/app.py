from flask import Flask, render_template, request, jsonify, url_for
import json
from math import radians, cos, sin, asin, sqrt
from SearchData import SearchData
import datetime

# app
app = Flask(__name__)

# calculate the distance between two points in earth
def geodistance(lng1,lat1,lng2,lat2):
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000
    distance = round(distance / 1000, 3)
    return distance

def crmData(sqlQuery, crmNumber, lat, lng, nearbyCrime, articles, typeWeather):
    # connect to database and return useful data
    crimedata = SearchData()
    allData = crimedata.fetchData(sqlQuery)
    for data in allData:
        # get the distance between two locations
        distance = geodistance(data[-2], data[-1], lat, lng)
        # add the filtered data into list
        if distance <= 1:
            date = data[0][:10]
            month, day, year = date.split('/')
            nearbyCrime.append([distance, data[-2], data[-1], int(month), int(day), int(year)])
            typeWeather.append([crmNumber, data[3], data[4]])
            articles.append({
                'crmNumber': str(crmNumber),
                'Date': data[0],
                'CrmDesc': data[1],
                'Location': data[2],
                'Weather': data[-3],
            })
            crmNumber += 1
    return crmNumber


@app.route('/')
def index():
    """
    :return: request the index page (introduction of our project)
    """
    return render_template('index.html')


@app.route('/home')
def home():
    """
    :return: request the home page (members)
    """
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    :return:
    """
    if request.method == 'POST':
        if request.form['isAjax']:
            data = {'code': 1000, 'msg': ''}
            lat, lng = request.form['latitude'], request.form['longitude']
            if lat and lng:
                data['url'] = url_for('crime', lat=lat, lng=lng)
            else:
                data['code'] = 4000
                data['msg'] = 'Can not find that location'
            return jsonify(data)
    return render_template('search.html')



@app.route('/crime/<lat>/<lng>', methods=['GET', 'POST'])
def crime(lat, lng):
    """
    :return: request the crime web page (visualization)
    """
    # start date -> end date -> min date -> max date
    timeSpan = ['2020-01-01', str(datetime.date.today()), '2020-01-01', str(datetime.date.today())]
    # lat, lng = float(lat), float(lng)
    center = [lat, lng]
    # define returned value
    nearbyCrime, articles, typeWeather = [], [], []
    try:
        # timespan
        timeSpan[0], timeSpan[1] = request.form['crime-start'], request.form['crime-end']
        limit = int(request.form['flexRadioDefault'])
        timeQuery = f"where `date` between '{timeSpan[0]}' and '{timeSpan[1]}'"
        # row number
        crimedata = SearchData()
        rowNumber = crimedata.fetchData("select count(1) from LaCrime " + timeQuery)[0][0]
        # define a offset
        offset = 0
        # record a number to mark the element in the front end
        crmNumber = 0
        # execute the loop until we collect enough data
        while(crmNumber < limit and offset < rowNumber):
            sqlQuery = """
            select `DATE OCC`, `Crm Cd Desc`,`LOCATION`, crimeType, wx_phrase_label, wx_phrase, LAT, LON from 
            (select `DATE OCC`, `Crm Cd Desc`,`LOCATION`, crimeType, LAT, LON, `date` from LaCrime {timeQuery}) as a 
            left join (select `date`, wx_phrase_label, wx_phrase from LaWeather) as b 
            on a.date = b.date order by a.date desc limit 10000 offset {offset};
            """.format(timeQuery=timeQuery, offset=offset)
            offset += 10000
            crmNumber = crmData(sqlQuery, crmNumber, lat, lng, nearbyCrime, articles, typeWeather)
            print(crmNumber)
            if crmNumber >= limit:
                nearbyCrime = nearbyCrime[:limit]
                articles = articles[:limit]
                typeWeather = typeWeather[:limit]
    except:
        sqlQuery = """
        select `DATE OCC`, `Crm Cd Desc`,`LOCATION`, crimeType, wx_phrase_label, wx_phrase, LAT, LON from 
        (select `DATE OCC`, `Crm Cd Desc`,`LOCATION`, crimeType, LAT, LON, `date` from LaCrime) as a 
        left join (select `date`, wx_phrase_label, wx_phrase  from LaWeather) as b 
        on a.date = b.date order by a.date desc limit 10000;
        """
        crmNumber = 0
        crmNumber = crmData(sqlQuery, crmNumber, lat, lng, nearbyCrime, articles, typeWeather)
    return render_template('crime.html', context={
        'timeSpan': timeSpan,
        'center': center,
        'locations': nearbyCrime,
        'articles': articles,
        'typeWeather': typeWeather,
    })


@app.route('/analysis')
def analysis():
    """
    :return: request the analysis web page (machine learning -> prediction)
    """
    return render_template('analysis.html')


@app.route('/rawCrime/<int:page>/', methods=['GET'])
def rawCrime(page):
    """
    :return: request the crime web page (visualization)
    """
    # define the offset
    offset = page * 20
    # connect to database and return useful data
    crimedata = SearchData()
    # show it
    headers = []
    crimeCase = []
    try:
        columns = crimedata.fetchData("select COLUMN_NAME from information_schema.COLUMNS where TABLE_SCHEMA = 'dsci551' and TABLE_NAME = 'LaCrime'")
        headers = [column[0] for column in columns][:-5]
        headers1 = ['`' + column[0] + '`' for column in columns][:-5]
    except:
        headers = []
    try:
        rowNumber = crimedata.fetchData("select count(1) from LaCrime")[0]
        # get the data
        sqlQuery = f"select {','.join(headers1)} from LaCrime limit 20 offset {offset}"
        crimeCase = crimedata.fetchData(sqlQuery)
    except:
        rowNumber = 0
    # page
    maxPage = rowNumber[0] // 20
    prePage = page - 1 if page != 0 else 0
    curPage = page
    nxtPage = page + 1 if page != maxPage else maxPage
    return render_template('rawCrime.html', context={
        'headers': headers,
        'crimeCase': crimeCase,
        'prePage': prePage,
        'curPage': curPage,
        'nxtPage': nxtPage,
        'maxPage': maxPage,
    })


@app.route('/rawWeather/<int:page>/', methods=['GET'])
def rawWeather(page):
    """
    :return: request the crime web page (visualization)
    """
    # define the offset
    offset = page * 20
    # connect to database and return useful data
    weatherData = SearchData()
    # show it
    headers = []
    weather = []
    try:
        columns = weatherData.fetchData("select COLUMN_NAME from information_schema.COLUMNS where TABLE_SCHEMA = 'dsci551' and TABLE_NAME = 'LaWeather'")
        headers = [column[0] for column in columns][:-1]
        headers1 = ['`' + column[0] + '`' for column in columns][:-1]
    except:
        headers = []
    try:
        rowNumber = weatherData.fetchData("select count(1) from LaWeather")[0]
        # get the data
        sqlQuery = f"select {','.join(headers1)} from LaWeather limit 20 offset {offset}"
        weather = weatherData.fetchData(sqlQuery)
    except:
        rowNumber = 0
    # page
    maxPage = rowNumber[0] // 20
    prePage = page - 1 if page != 0 else 0
    curPage = page
    nxtPage = page + 1 if page != maxPage else maxPage
    return render_template('rawWeather.html', context={
        'headers': headers,
        'weather': weather,
        'prePage': prePage,
        'curPage': curPage,
        'nxtPage': nxtPage,
        'maxPage': maxPage,
    })


@app.route('/rawCity/<int:page>/', methods=['GET'])
def rawCity(page):
    """
    :return: request the crime web page (visualization)
    """
    # define the offset
    offset = page * 20
    # connect to database and return useful data
    cityData = SearchData()
    # show it
    headers = []
    weather = []
    try:
        columns = cityData.fetchData("select COLUMN_NAME from information_schema.COLUMNS where TABLE_SCHEMA = 'dsci551' and TABLE_NAME = 'LaCities'")
        headers = [column[0] for column in columns]
        headers1 = ['`' + column[0] + '`' for column in columns]
    except:
        headers = []
    try:
        rowNumber = cityData.fetchData("select count(1) from LaCities")[0]
        print(rowNumber)
        # get the data
        sqlQuery = f"select {','.join(headers1)} from LaCities limit 20 offset {offset}"
        city = cityData.fetchData(sqlQuery)
    except:
        rowNumber = 0
    # page
    maxPage = rowNumber[0] // 20
    prePage = page - 1 if page != 0 else 0
    curPage = page
    nxtPage = page + 1 if page != maxPage else maxPage
    return render_template('rawCities.html', context={
        'headers': headers,
        'city': city,
        'prePage': prePage,
        'curPage': curPage,
        'nxtPage': nxtPage,
        'maxPage': maxPage,
    })


# analysis part
@app.route('/laCities', methods=['GET'])
def laCities():
    data = {'code': 1000, 'msg': ''}
    try:
        cityData = SearchData()
        sqlQuery = """
        select Cities, LAT, LNG, IFNULL(crimeNumber, 0) as crimeNumber from
        (select Cities, LAT, LNG from LaCities) as a
        left join
        (select district, count(1) as crimeNumber from LaCrime group by district) as b
        on a.Cities = b.district
        """
        data['cities'] = cityData.fetchData(sqlQuery)
    except:
        data['code'] = 2000
    return jsonify(data)


# date and crime
@app.route('/dateCrime', methods=['GET'])
def dateCrime():
    data = {'code': 1000, 'msg': ''}
    try:
        dateData = SearchData()
        firstPart = " select count(1) as crmNumber from  (select left(date, 4) as year, month from LaCrime) as a "
        secondPart = "group by month order by month"
        month20 = dateData.fetchData(firstPart + "where year = '2020' " + secondPart)
        month21 = dateData.fetchData(firstPart + "where year = '2021' " + secondPart)
        month22 = dateData.fetchData(firstPart + "where year = '2022' " + secondPart)
        day = dateData.fetchData("""
        select count(1) as crmNumber from  
        (select left(date, 4) as year, day from LaCrime) as a where year in ('2020', '2021') 
        group by day order by day""")
        data['month20'] = [value[0] for value in month20]
        data['month21'] = [value[0] for value in month21]
        data['month22'] = [value[0] for value in month22]
        data['dayDistribution'] = [value[0] for value in day]
    except:
        data['code'] = 2000
    return jsonify(data)


# type and crime
@app.route('/typeCrime', methods=['GET'])
def typeCrime():
    data = {'code': 1000, 'msg': ''}
    try:
        typeData = SearchData()
        sqlQuery = "select count(1) as number from LaCrime group by crimeType order by crimeType"
        data['typeCrime'] = [value[0] for value in typeData.fetchData(sqlQuery)]
    except:
        data['code'] = 2000
    return jsonify(data)


# weather and Crime
@app.route('/weatherCrime', methods=['GET'])
def weatherCrime():
    data = {'code': 1000, 'msg': ''}
    try:
        weatherData = SearchData()
        weatherDistribution = "select count(1) from LaWeather group by wx_phrase_label order by wx_phrase_label"
        weatherCrime = """
        select wx_phrase_label, count(1) from 
        (select date from LaCrime) as a 
        left join 
        (select date, wx_phrase_label from LaWeather) as b 
        on a.date = b.date 
        group by wx_phrase_label order by wx_phrase_label;
        """
        data['weatherDistribution'] = [value[0] for value in weatherData.fetchData(weatherDistribution)]
        data['weatherCrime'] = [value[1] for value in weatherData.fetchData(weatherCrime) if value[0]]
    except:
        data['code'] = 2000
    return jsonify(data)


#
# weather and Crime
@app.route('/tempCrime', methods=['GET'])
def tempCrime():
    data = {'code': 1000, 'msg': ''}
    try:
        tempData = SearchData()
        temp_type = """
        select temp, crimeType, count(1) as number from
        (select date, crimeType from LaCrime) as a
        left join
        (select date, floor(temp_avg / 10)*10 as temp from LaWeather) as b
        on a.date = b.date 
        where b.date is not null 
        group by temp, crimeType 
        order by temp, crimeType
        """
        groupData = tempData.fetchData(temp_type)
        tempType = [[0 for i in range(8)] for j in range(40, 100, 10)]
        for i in range(len(groupData)):
            temp, type = int(groupData[i][0]), int(groupData[i][1])
            tempType[int(temp/10 - 4)][type-1] = groupData[i][2]
        data['tempType'] = tempType
    except:
        data['code'] = 2000
    return jsonify(data)


if __name__ == '__main__':
    # app.run()
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
