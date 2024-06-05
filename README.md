# Thug's Demo Analyzer

This Demo Analyzer is a tool designed for generating detailed scoreboards from CS2 demos, making it ideal for tracking player statistics in small leagues and tournaments. It simplifies the process of analyzing game data, providing comprehensive and accurate insights into player performance.

Currently supported stats:

 - Rounds won
 - Kills
 - Deaths
 - Assists
 - Headshot kills
 - Damage
 - Enemies flashed
 - 5K, 4K, 3K
 - Opening Kills
 - 1vsXs
 - Zeus kills

## Releases
Check out the first beta [release](https://github.com/muiloya/Demo-Analyzer/releases). Note this is currently only tested on Faceit, behavior on pro, Esportal, and Matchmaking demos may be different.

## Development requirements

In order to contribute you will require:

 - Pandas
 - PandasGUI
 - Demoparser2
- Pyinstaller

## Creating a release

To create a release, open a terminal at the root folder and run:

> `pyinstaller --onefile --collect-all qtstylish --hidden-import polars --icon=resources/icon.ico --name="Thug Demo Analyzer" main.py`

## License

[MIT License](https://opensource.org/license/mit)

