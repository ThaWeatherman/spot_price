Spot price checker

Provides a simple API for getting the current spot price of gold, silver, platinum, or palladium.
Prices are retrieved from Apmex's website.

Deploy:
    - Properly configure nginx as a reverse proxy (see gunicorn's website)
    - Run within tmux/screen: gunicorn -b 127.0.0.1:6789 -w 5 app:app

API:
    - /api/<metal name>
        - gold
        - silver
        - platinum
        - palladium
        - all

Also provides a very basic landing page displaying the last known prices.
