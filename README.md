# FormulaOneBot

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b074f2014e034c9894cb3413ac616e14)](https://www.codacy.com/manual/slinucs/FormulaOneBot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ch3p4ll3/FormulaOneBot&amp;utm_campaign=Badge_Grade)

With this bot you can check the race results and qualifications, get information on the circuits, constructors, drivers and the championship

This bot was born using python, [botogram](https://botogram.dev/) library and [ergast](http://ergast.com/mrd) api's.

## Configuration
Enter the token as a system variable called "TOKEN_TG" (editable by changing the name to src/config.py).

## How to use
There are some commands you can use with this bot specifying the season. In case of error the current season will be used:

- circuits -> List the circuits
- constructors -> List F1 constructors
- next -> Show next f1 race.
- raceresults -> List all f1 races and get all results
- standings -> Driver and Constructor standings.

instead these commands cannot have arguments so they only work with the current season:
- drivers -> list F1 drivers
- help -> Show this help message.
- last -> Show the results of the last f1 race and qualifying.

For info contact [me](https://t.me/ch3p4ll3).
