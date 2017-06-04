Spot price checker
------------------

Provides a simple API for getting the current spot price of gold, silver, other metals, or popular digital currencies.
Metal prices are retrieved from Provident Metals.
Digital currency prices are obtained from Coinbase.

Deploy:
    - Properly configure nginx as a reverse proxy (see gunicorn's website)
    - Run within tmux/screen: gunicorn -b 127.0.0.1:6789 -w 5 wsgi:application

API:
    - /api/<metal name>
        - gold
        - silver
        - etc.
        - all

Also provides a very basic landing page displaying the last known prices.

