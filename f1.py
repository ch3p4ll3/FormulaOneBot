import requests
import botogram
import datetime
from src import config

bot = botogram.create(config.token_tg)
bot.owner = "@ch3p4ll3"


def convert_time(strr):
    strr = strr.replace("Z", "")
    a = strr.split(":")
    h = str(int(a[0]) + 1)
    return h + ":" + a[1] + ":" + a[2]


def diffdate(data, f):
    datetime_format = '%d/%m/%Y %H:%M:%S'
    now = datetime.datetime.now()
    date1 = data + " " + f
    date2 = now.strftime("%d/%m/%Y %H:%M:%S")
    diff = (datetime.datetime.strptime(date1, datetime_format) -
            datetime.datetime.strptime(date2, datetime_format))

    return diff


def convert_data(strr):
    strr = strr.split("-")
    return strr[2] + "/" + strr[1] + "/" + strr[0]


@bot.callback("racelast")
def racelast(message):
    url = "http://ergast.com/api/f1/current/last/results.json"

    r = requests.get(url)

    data = r.json()['MRData']['RaceTable']['Races'][0]['Results']
    btns = botogram.Buttons()
    btns[0].callback("Qualify", "qualylast")
    btns[1].callback("Go back", "menulast")
    text = "DRIVER | GAP\n\n"
    for driver in data:
        try:
            text += driver['Driver']['code'] + " | " + \
                    driver['Time']['time'] + "\n"
        except KeyError:
            try:
                text += driver['Driver']['code'] + " | " + \
                        driver['status'] + "\n"
            except Exception:
                pass
    message.edit(text, attach=btns)


@bot.callback("menulast")
def menulast(message):
    url = "http://ergast.com/api/f1/current/last.json"

    r = requests.get(url)

    data = r.json()['MRData']['RaceTable']['Races'][0]

    btns = botogram.Buttons()

    btns[0].callback("Results", "resultslast")
    btns[1].url(data['raceName'], data['url'])
    btns[2].url("Streaming", "https://www.premiersport.tv/")

    message.edit((
                     "*{}*\n*Round: *{}\n*Data: *{}\n*Time: *{} (CET)"
                 ).format(data['raceName'], data['round'],
                          convert_data(data['date']),
                          convert_time(data['time'])),
                 syntax="markdown", attach=btns)


@bot.callback("qualylast")
def qualyslast(message):
    url = "http://ergast.com/api/f1/current/last/qualifying.json"

    r = requests.get(url)

    data = r.json()['MRData']['RaceTable']['Races'][0]['QualifyingResults']

    btns = botogram.Buttons()
    btns[0].callback("Race", "racelast")
    btns[1].callback("Go back", "menulast")
    text = "DRIVER | Time\n\n"
    for driver in data:
        try:
            if driver['Q3'] != "":
                text += driver['Driver']['code'] + " | " + \
                        driver['Q3'] + "\n"
            else:
                text += driver['Driver']['code'] + " | DNF\n"
        except KeyError:
            try:
                if driver['Q2'] != "":
                    text += driver['Driver']['code'] + " | " + \
                            driver['Q2'] + "\n"
                else:
                    text += driver['Driver']['code'] + " | DNF\n"
            except KeyError:
                if driver['Q1'] != "":
                    text += driver['Driver']['code'] + " | " + \
                            driver['Q1'] + "\n"
                else:
                    text += driver['Driver']['code'] + " | DNF\n"
    message.edit(text, attach=btns)


@bot.callback("resultslast")
def resultslast(message):
    btns = botogram.Buttons()
    btns[0].callback("Qualify", "qualylast")
    btns[0].callback("Race", "racelast")
    btns[1].callback("Go back", "menulast")
    message.edit("Results", attach=btns)


@bot.command("last")
def last_command(chat):
    """show the results of the last f1 race and qualifying"""
    url = "http://ergast.com/api/f1/current/last.json"

    r = requests.get(url)

    data = r.json()['MRData']['RaceTable']['Races'][0]

    btns = botogram.Buttons()

    btns[0].callback("Results", "resultslast")
    btns[1].url(data['raceName'], data['url'])
    # btns[2].url("Streaming", "https://www.premiersport.tv/")

    chat.send((
                  "*{}*\n*Round: *{}\n*Data: *{}\n*Time: *{} (CET)"
              ).format(data['raceName'], data['round'],
                       convert_data(data['date']),
                       convert_time(data['time'])),
              syntax="markdown", attach=btns)


@bot.command("next")
def next_command(chat):
    """show next f1 race"""
    url = "http://ergast.com/api/f1/current/next.json"

    r = requests.get(url)

    data = r.json()['MRData']['RaceTable']['Races'][0]

    btns = botogram.Buttons()

    btns[0].url(data['raceName'], data['url'])
    btns[1].url("Streaming", "https://www.premiersport.tv/")

    chat.send((
                  "*{}*\n*Round: *{}\n*Data: *{}\n*Time: *{} (CET)"
                  "\n*Missing*: {}"
              ).format(data['raceName'],
                       data['round'],
                       convert_data(data['date']),
                       convert_time(data['time']),
                       diffdate(convert_data(data['date']),
                                convert_time(data['time']))),
              syntax="markdown", attach=btns)


@bot.callback("menustand")
def menustand(message):
    btns = botogram.Buttons()
    btns[0].callback("Driver Standings", "driverstand")
    btns[1].callback("Constructor Standings", "constructorstand")

    message.edit("Standings", syntax="markdown", attach=btns)


@bot.callback("constructorstand")
def constructorstand(message):
    btns = botogram.Buttons()
    btns[0].callback("Driver Standings", "driverstand")
    btns[1].callback("Go back", "menustand")

    url = "http://ergast.com/api/f1/current/constructorStandings.json"

    r = requests.get(url)

    data = r.json()['MRData']['StandingsTable']
    data = data['StandingsLists'][0]['ConstructorStandings']

    text = "Car | points\n\n"

    for car in data:
        text += car['Constructor']['name'] + " | " + car['points'] + "\n"

    message.edit(text, attach=btns)


@bot.callback("driverstand")
def driverstand(message):
    url = "http://ergast.com/api/f1/current/driverStandings.json"

    r = requests.get(url)

    data = r.json()['MRData']['StandingsTable']
    data = data['StandingsLists'][0]['DriverStandings']

    btns = botogram.Buttons()
    btns[0].callback("Constructor Standings", "constructorstand")
    btns[1].callback("Go back", "menustand")

    text = "Driver | Car | points\n\n"

    for driver in data:
        text += driver['Driver']['code'] + " | " + \
                driver['Constructors'][0]['name'] + " | " + \
                driver['points'] + "\n"

    message.edit(text, attach=btns)


@bot.command("standings")
def standings_command(chat):
    """Driver and Constructor standings"""
    btns = botogram.Buttons()
    btns[0].callback("Driver Standings", "driverstand")
    btns[1].callback("Constructor Standings", "constructorstand")

    chat.send("Standings", syntax="markdown", attach=btns)


@bot.callback("menudrivers")
def menudriver(message):
    url = "http://ergast.com/api/f1/current/drivers.json"

    btns = botogram.Buttons()

    r = requests.get(url)

    data = r.json()['MRData']['DriverTable']['Drivers']

    i = 1
    y = 0

    for driver in data:
        btns[y].callback(driver['familyName'], "drivers", driver['driverId'])
        if i % 3 == 0:
            y += 1
        i += 1

    message.edit("Drivers", attach=btns)


@bot.callback("drivers")
def driverlist(message, data):
    url = "http://ergast.com/api/f1/current/drivers.json"

    btns = botogram.Buttons()

    r = requests.get(url)

    dat = r.json()['MRData']['DriverTable']['Drivers']

    text = ""

    for driver in dat:
        if driver['driverId'] == data:
            btns[0].url(driver['givenName'] + " " + driver['familyName'],
                        driver['url'])

            text += ("*" + driver['givenName'] + " " + driver['familyName']
                     + "*\n\n*Number: *" + driver['permanentNumber'] + "\n" +
                     "*Date of birth: *" + convert_data(driver['dateOfBirth'])
                     + "\n*Nationality: *" + driver['nationality'])

    btns[1].callback("Go back", "menudrivers")
    message.edit(text, attach=btns)


@bot.command("drivers")
def drivers_command(chat):
    """list F1 drivers"""
    url = "http://ergast.com/api/f1/current/drivers.json"

    btns = botogram.Buttons()

    r = requests.get(url)

    data = r.json()['MRData']['DriverTable']['Drivers']

    i = 1
    y = 0

    for driver in data:
        btns[y].callback(driver['familyName'], "drivers",
                         driver['driverId'])
        if i % 3 == 0:
            y += 1
        i += 1

    chat.send("Drivers", attach=btns)


@bot.callback("menudconstructors")
def menudconstructors(message):
    url = "http://ergast.com/api/f1/current/constructors.json"

    btns = botogram.Buttons()

    r = requests.get(url)

    data = r.json()['MRData']['ConstructorTable']['Constructors']

    i = 1
    y = 0

    for driver in data:
        btns[y].callback(driver['name'], "constructorlst",
                         driver['constructorId'])
        if i % 2 == 0:
            y += 1
        i += 1

    message.edit("Constructors", attach=btns)


@bot.callback("constructorlst")
def constructorlist(message, data):
    url = "http://ergast.com/api/f1/current/constructors.json"

    btns = botogram.Buttons()

    r = requests.get(url)

    dat = r.json()['MRData']['ConstructorTable']['Constructors']

    text = ""

    for driver in dat:
        if driver['constructorId'] == data:
            btns[0].url(driver['name'], driver['url'])

            vincite = requests.get(
                "https://ergast.com/api/f1/constructors/" + data +
                "/constructorStandings/1/seasons.json")

            vittorie = vincite.json()['MRData']

            l2 = ""
            for c in vittorie['SeasonTable']['Seasons']:
                l2 += c['season'] + " , "

            text += ("*" + driver['name'] + "*\n\n*Championships: *" +
                     vittorie['total'] + "\n*Years: *" + l2[0:len(l2) - 3] +
                     "\n*Nationality: *" + driver['nationality'])

    btns[1].callback("Go back", "menudconstructors")
    message.edit(text, attach=btns)


@bot.command("constructors")
def constructors_command(chat):
    """list F1 constructors"""
    url = "http://ergast.com/api/f1/current/constructors.json"

    btns = botogram.Buttons()

    r = requests.get(url)

    data = r.json()['MRData']['ConstructorTable']['Constructors']

    i = 1
    y = 0

    for driver in data:
        btns[y].callback(driver['name'], "constructorlst",
                         driver['constructorId'])
        if i % 2 == 0:
            y += 1
        i += 1

    chat.send("Constructors list", attach=btns)


@bot.command("raceresults")
def raceresults_command(chat):
    """List all f1 races and get all results"""
    url = "https://ergast.com/api/f1/current/results.json?limit=99999"

    r = requests.get(url)

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
def raceresultquery(message, data):
    url = "https://ergast.com/api/f1/current/{}/results.json".format(
        str(data))

    r = requests.get(url)

    dat = r.json()['MRData']['RaceTable']['Races'][0]['Results']

    btns = botogram.Buttons()
    btns[0].callback("Qualify", "qualyresult", str(data))
    btns[1].callback("Go back", "menuresults")
    text = "*{}*\n\nDRIVER | GAP\n".format(
        r.json()['MRData']['RaceTable']['Races'][0]['raceName'])

    for driver in dat:
        try:
            text += driver['Driver']['code'] + " | " + \
                    driver['Time']['time'] + "\n"
        except KeyError:
            try:
                text += driver['Driver']['code'] + " | " + \
                        driver['status'] + "\n"
            except Exception:
                pass
    message.edit(text, attach=btns)


@bot.callback("qualyresult")
def qualyresults(message, data):
    url = "https://ergast.com/api/f1/current/{}/qualifying.json".format(
        str(data))

    r = requests.get(url)

    dat = r.json()['MRData']['RaceTable']['Races'][0]['QualifyingResults']
    btns = botogram.Buttons()
    btns[0].callback("Race", "raceresult", str(data))
    btns[1].callback("Go back", "menuresults")
    text = "*{}*\n\nDRIVER | Time\n".format(
        r.json()['MRData']['RaceTable']['Races'][0]['raceName'])
    for driver in dat:
        try:
            if driver['Q3'] != "":
                text += driver['Driver']['code'] + " | " + \
                        driver['Q3'] + "\n"
            else:
                text += driver['Driver']['code'] + " | DNF\n"
        except KeyError:
            try:
                if driver['Q2'] != "":
                    text += driver['Driver']['code'] + " | " + \
                            driver['Q2'] + "\n"
                else:
                    text += driver['Driver']['code'] + " | DNF\n"
            except KeyError:
                if driver['Q1'] != "":
                    text += driver['Driver']['code'] + " | " + \
                            driver['Q1'] + "\n"
                else:
                    text += driver['Driver']['code'] + " | DNF\n"

    message.edit(text, attach=btns)


@bot.callback("menuresults")
def menuresults(message):
    url = "https://ergast.com/api/f1/current/results.json?limit=99999"

    btns = botogram.Buttons()

    r = requests.get(url)

    data = r.json()['MRData']['RaceTable']['Races']

    i = -1
    y = 0

    for dat in data:
        btns[y].callback(dat['raceName'], "raceresult", dat['round'])
        if i % 2 == 0:
            y += 1
        i += 1

    message.edit("Race results", attach=btns, syntax="markdown")


@bot.command("circuits")
def circuitslist_command(chat):
    """list the circuits"""
    url = "https://ergast.com/api/f1/current/circuits.json"

    r = requests.get(url)

    data = r.json()['MRData']['CircuitTable']['Circuits']

    btns = botogram.Buttons()

    i = -1
    y = 0

    for dat in data:
        btns[y].callback(dat['circuitName'], "circuitslst", dat['circuitId'])
        if i % 2 == 0:
            y += 1
        i += 1

    chat.send("Circuit list", attach=btns)


@bot.callback("circuitslst")
def circuitsinfo(message, data):
    """List all circuits"""
    url = "https://ergast.com/api/f1/current/circuits/{}.json".format(
        str(data))

    url2 = "https://ergast.com/api/f1/current/circuits/{}/races.json".format(
        str(data))

    r = requests.get(url)
    r2 = requests.get(url2)

    dat = r.json()['MRData']['CircuitTable']['Circuits'][0]
    dat2 = r2.json()['MRData']['RaceTable']['Races'][0]

    btns = botogram.Buttons()

    btns[0].url(dat['circuitName'], dat['url'])
    btns[1].callback("Send Position", "sendCircuitPosition", data)
    btns[2].callback("Go back", "menuCircuits")

    text = ("*{}*\n*Round:* {}\n*Date:* {}"
            "\n*Time:* {}\n*Locality:* {}, {}").format(
                dat['circuitName'],
                dat2['round'],
                convert_data(dat2['date']),
                convert_time(dat2['time']),
                dat['Location']['locality'],
                dat['Location']['country'])

    message.edit(text, attach=btns, syntax="markdown")


@bot.callback("menuCircuits")
def menucircuits(message):
    url = "https://ergast.com/api/f1/current/circuits.json"

    r = requests.get(url)

    data = r.json()['MRData']['CircuitTable']['Circuits']

    btns = botogram.Buttons()

    i = -1
    y = 0

    for dat in data:
        btns[y].callback(dat['circuitName'], "circuitslst", dat['circuitId'])
        if i % 2 == 0:
            y += 1
        i += 1

    message.edit("Circuit list", attach=btns)


@bot.callback("sendCircuitPosition")
def circuitposition(chat, data):
    url = "https://ergast.com/api/f1/current/circuits/{}.json".format(
        str(data))

    r = requests.get(url)

    dat = r.json()['MRData']['CircuitTable']['Circuits'][0]
    chat.send_location(latitude=dat['Location']['lat'],
                       longitude=dat['Location']['long'])


if __name__ == "__main__":
    bot.run()
