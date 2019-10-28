import requests
import botogram
import datetime

bot = botogram.create("xxx")


def convertTime(strr):
    strr = strr.replace("Z", "")
    a = strr.split(":")
    h = str(int(a[0]) + 1)
    return h + ":" + a[1] + ":" + a[2]


def diffdate(data, f):
    datetimeFormat = '%d/%m/%Y %H:%M:%S'
    now = datetime.datetime.now()
    date1 = data + " " + f
    date2 = now.strftime("%d/%m/%Y %H:%M:%S")
    diff = datetime.datetime.strptime(date1, datetimeFormat) \
           - datetime.datetime.strptime(date2, datetimeFormat)

    return diff


def convertData(strr):
    strr = strr.split("-")
    return strr[2] + "/" + strr[1] + "/" + strr[0]


@bot.callback("racelast")
def racelast(query, chat, message):
    URL = "http://ergast.com/api/f1/current/last/results.json"

    r = requests.get(URL)

    data = r.json()['MRData']['RaceTable']['Races'][0]['Results']
    btns = botogram.Buttons()
    btns[0].callback("Qualify", "qualylast")
    btns[1].callback("Go back", "menulast")
    l = "DRIVER | GAP\n\n"
    for driver in data:
        try:
            l += driver['Driver']['code'] + " | " + driver['Time']['time'] + "\n"
        except KeyError:
            try:
                l += driver['Driver']['code'] + " | " + driver['status'] + "\n"
            except:
                pass
    message.edit(l, attach=btns)


@bot.callback("menulast")
def menulast(query, chat, message):
    URL = "http://ergast.com/api/f1/current/last.json"

    r = requests.get(URL)

    data = r.json()['MRData']['RaceTable']['Races'][0]

    btns = botogram.Buttons()

    btns[0].callback("Results", "resultslast")
    btns[1].url(data['raceName'], data['url'])
    btns[2].url("Streaming", "https://www.premiersport.tv/")

    message.edit((
                     "*{}*\n*Round: *{}\n*Data: *{}\n*Time: *{} (IT)"
                 ).format(data['raceName'], data['round'],
                          convertData(data['date']),
                          convertTime(data['time'])),
                 syntax="markdown", attach=btns)


@bot.callback("qualylast")
def qualyslast(query, chat, message):
    URL = "http://ergast.com/api/f1/current/last/qualifying.json"

    r = requests.get(URL)

    data = r.json()['MRData']['RaceTable']['Races'][0]['QualifyingResults']
    # print(data)
    btns = botogram.Buttons()
    btns[0].callback("Race", "racelast")
    btns[1].callback("Go back", "menulast")
    l = "DRIVER | Time\n\n"
    for driver in data:
        try:
            if driver['Q3'] != "":
                l += driver['Driver']['code'] + " | " + driver['Q3'] + "\n"
            else:
                l += driver['Driver']['code'] + " | DNF\n"
        except KeyError:
            try:
                if driver['Q2'] != "":
                    l += driver['Driver']['code'] + " | " + driver['Q2'] + "\n"
                else:
                    l += driver['Driver']['code'] + " | DNF\n"
            except KeyError:
                if driver['Q1'] != "":
                    l += driver['Driver']['code'] + " | " + driver['Q1'] + "\n"
                else:
                    l += driver['Driver']['code'] + " | DNF\n"
    message.edit(l, attach=btns)


@bot.callback("resultslast")
def resultslast(query, chat, message):
    btns = botogram.Buttons()
    btns[0].callback("Qualify", "qualylast")
    btns[0].callback("Race", "racelast")
    btns[1].callback("Go back", "menulast")
    message.edit("Results", attach=btns)


@bot.command("last")
def last_command(chat, message, args):
    """show the results of the last f1 race and qualifying"""
    URL = "http://ergast.com/api/f1/current/last.json"

    r = requests.get(URL)

    data = r.json()['MRData']['RaceTable']['Races'][0]

    btns = botogram.Buttons()

    btns[0].callback("Results", "resultslast")
    btns[1].url(data['raceName'], data['url'])
    btns[2].url("Streaming", "https://www.premiersport.tv/")

    chat.send((
                  "*{}*\n*Round: *{}\n*Data: *{}\n*Time: *{} (IT)"
              ).format(data['raceName'], data['round'],
                       convertData(data['date']),
                       convertTime(data['time'])),
              syntax="markdown", attach=btns)


@bot.command("next")
def next_command(chat, message, args):
    """show next f1 race"""
    URL = "http://ergast.com/api/f1/current/next.json"

    r = requests.get(URL)

    data = r.json()['MRData']['RaceTable']['Races'][0]

    btns = botogram.Buttons()

    btns[0].url(data['raceName'], data['url'])
    btns[1].url("Streaming", "https://www.premiersport.tv/")

    chat.send((
                  "*{}*\n*Round: *{}\n*Data: *{}\n*Time: *{} (IT)\n*Missing*: {}"
              ).format(data['raceName'],
                       data['round'],
                       convertData(data['date']),
                       convertTime(data['time']),
                       diffdate(convertData(data['date']), convertTime(data['time']))),
              syntax="markdown", attach=btns)


@bot.callback("menustand")
def menustand(query, message, chat):
    btns = botogram.Buttons()
    btns[0].callback("Driver Standings", "driverstand")
    btns[1].callback("Constructor Standings", "constructorstand")

    message.edit("Standings", syntax="markdown", attach=btns)


@bot.callback("constructorstand")
def constructorstand(query, chat, message):
    btns = botogram.Buttons()
    btns[0].callback("Driver Standings", "driverstand")
    btns[1].callback("Go back", "menustand")

    URL = "http://ergast.com/api/f1/current/constructorStandings.json"

    r = requests.get(URL)

    data = r.json()['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

    l = "Car | points\n\n"

    for car in data:
        l += car['Constructor']['name'] + " | " + car['points'] + "\n"

    message.edit(l, attach=btns)


@bot.callback("driverstand")
def driverstand(query, chat, message):
    URL = "http://ergast.com/api/f1/current/driverStandings.json"

    r = requests.get(URL)

    data = r.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    btns = botogram.Buttons()
    btns[0].callback("Constructor Standings", "constructorstand")
    btns[1].callback("Go back", "menustand")

    l = "Driver | Car | points\n\n"

    for driver in data:
        l += driver['Driver']['code'] + " | " + driver['Constructors'][0]['name'] + " | " + driver['points'] + "\n"

    message.edit(l, attach=btns)


@bot.command("standings")
def standings(chat, message):
    """Driver and Constructor standings"""
    btns = botogram.Buttons()
    btns[0].callback("Driver Standings", "driverstand")
    btns[1].callback("Constructor Standings", "constructorstand")

    chat.send("Standings", syntax="markdown", attach=btns)


@bot.callback("menudrivers")
def menudriver(query, chat, message):
    URL = "http://ergast.com/api/f1/current/drivers.json"

    btns = botogram.Buttons()

    r = requests.get(URL)

    data = r.json()['MRData']['DriverTable']['Drivers']

    i = 1
    y = 0

    for driver in data:
        btns[y].callback(driver['familyName'], "drivers", driver['driverId'])
        if (i % 3 == 0):
            y += 1
        i += 1

    chat.send("Drivers", attach=btns)


@bot.callback("drivers")
def driverlist(query, chat, message, data):
    URL = "http://ergast.com/api/f1/current/drivers.json"

    btns = botogram.Buttons()

    r = requests.get(URL)

    dat = r.json()['MRData']['DriverTable']['Drivers']

    l = ""

    for driver in dat:
        if driver['driverId'] == data:
            btns[0].url(driver['givenName'] + " " + driver['familyName'], driver['url'])

            l += ("*" + driver['givenName'] + " " + driver['familyName'] + "*\n\n"
                                                                           "*Number: *" + driver[
                      'permanentNumber'] + "\n*Date of birth: *" +
                  convertData(driver['dateOfBirth']) + "\n*Nationality: *" +
                  driver['nationality'])

    btns[1].callback("Go back", "menudrivers")
    message.edit(l, attach=btns)


@bot.command("drivers")
def drivers(chat, message, args):
    """list F1 drivers"""
    URL = "http://ergast.com/api/f1/current/drivers.json"

    btns = botogram.Buttons()

    r = requests.get(URL)

    data = r.json()['MRData']['DriverTable']['Drivers']

    i = 1
    y = 0

    for driver in data:
        btns[y].callback(driver['familyName'], "drivers", driver['driverId'])
        if (i % 3 == 0):
            y += 1
        i += 1

    chat.send("Drivers", attach=btns)


@bot.callback("menudconstructors")
def menudconstructors(query, chat, message):
    URL = "http://ergast.com/api/f1/current/constructors.json"

    btns = botogram.Buttons()

    r = requests.get(URL)

    data = r.json()['MRData']['ConstructorTable']['Constructors']

    i = 1
    y = 0

    for driver in data:
        btns[y].callback(driver['name'], "constructorlst", driver['constructorId'])
        if (i % 2 == 0):
            y += 1
        i += 1

    message.edit("Constructors", attach=btns)


@bot.callback("constructorlst")
def constructorlist(query, chat, message, data):
    URL = "http://ergast.com/api/f1/current/constructors.json"

    btns = botogram.Buttons()

    r = requests.get(URL)

    dat = r.json()['MRData']['ConstructorTable']['Constructors']

    l = ""

    for driver in dat:
        if driver['constructorId'] == data:
            btns[0].url(driver['name'], driver['url'])

            vincite = requests.get(
                "https://ergast.com/api/f1/constructors/" + data + "/constructorStandings/1/seasons.json")

            vittorie = vincite.json()['MRData']

            l2 = ""
            for c in vittorie['SeasonTable']['Seasons']:
                l2 += c['season'] + " , "

            l += ("*" + driver['name'] + "*\n\n*Championships: *"
                  + vittorie['total'] + "\n*Years: *" + l2[0:len(l2) - 3] +
                  "\n*Nationality: *" + driver['nationality'])

    btns[1].callback("Go back", "menudconstructors")
    message.edit(l, attach=btns)


@bot.command("constructors")
def constructors(chat, message, args):
    """list F1 constructors"""
    URL = "http://ergast.com/api/f1/current/constructors.json"

    btns = botogram.Buttons()

    r = requests.get(URL)

    data = r.json()['MRData']['ConstructorTable']['Constructors']

    i = 1
    y = 0

    for driver in data:
        btns[y].callback(driver['name'], "constructorlst", driver['constructorId'])
        if (i % 2 == 0):
            y += 1
        i += 1

    chat.send("Constructors list", attach=btns)


@bot.command("raceresults")
def raceresults(chat, message):
    """List all f1 races and get all results"""
    URL = "https://ergast.com/api/f1/current/results.json?limit=99999"

    r = requests.get(URL)

    data = r.json()['MRData']['RaceTable']['Races']

    btns = botogram.Buttons()

    i = -1
    y = 0

    for dat in data:
        btns[y].callback(dat['raceName'], "raceresult", dat['round'])
        if i % 2 == 0:
            y += 1
        i += 1

    chat.send("Race results", attach=btns, syntax="markdown")


@bot.callback("raceresult")
def raceresultquery(query, chat, message, data):
    URL = "https://ergast.com/api/f1/current/{}/results.json".format(str(data))

    r = requests.get(URL)

    dat = r.json()['MRData']['RaceTable']['Races'][0]['Results']

    btns = botogram.Buttons()
    btns[0].callback("Qualify", "qualyresult", str(data))
    btns[1].callback("Go back", "menuresults")
    l = "*{}*\n\nDRIVER | GAP\n".format(r.json()['MRData']['RaceTable']['Races'][0]['raceName'])
    for driver in dat:
        try:
            l += driver['Driver']['code'] + " | " + driver['Time']['time'] + "\n"
        except KeyError:
            try:
                l += driver['Driver']['code'] + " | " + driver['status'] + "\n"
            except:
                pass
    message.edit(l, attach=btns)


@bot.callback("qualyresult")
def qualyresults(message, data):
    URL = "https://ergast.com/api/f1/current/{}/qualifying.json".format(str(data))

    r = requests.get(URL)

    dat = r.json()['MRData']['RaceTable']['Races'][0]['QualifyingResults']
    btns = botogram.Buttons()
    btns[0].callback("Race", "raceresult", str(data))
    btns[1].callback("Go back", "menuresults")
    l = "*{}*\n\nDRIVER | Time\n".format(r.json()['MRData']['RaceTable']['Races'][0]['raceName'])
    for driver in dat:
        try:
            if driver['Q3'] != "":
                l += driver['Driver']['code'] + " | " + driver['Q3'] + "\n"
            else:
                l += driver['Driver']['code'] + " | DNF\n"
        except KeyError:
            try:
                if driver['Q2'] != "":
                    l += driver['Driver']['code'] + " | " + driver['Q2'] + "\n"
                else:
                    l += driver['Driver']['code'] + " | DNF\n"
            except KeyError:
                if driver['Q1'] != "":
                    l += driver['Driver']['code'] + " | " + driver['Q1'] + "\n"
                else:
                    l += driver['Driver']['code'] + " | DNF\n"

    message.edit(l, attach=btns)


@bot.callback("menuresults")
def menuresults(message):
    URL = "https://ergast.com/api/f1/current/results.json?limit=99999"

    btns = botogram.Buttons()

    r = requests.get(URL)

    data = r.json()['MRData']['RaceTable']['Races']

    i = -1
    y = 0

    for dat in data:
        btns[y].callback(dat['raceName'], "raceresult", dat['round'])
        if i % 2 == 0:
            y += 1
        i += 1

    message.edit("Race results", attach=btns, syntax="markdown")


if __name__ == "__main__":
    bot.run()