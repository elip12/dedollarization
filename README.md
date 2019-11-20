# Instructions
I assume you already have python3 installed.
1. Install otree: `pip3 install -U otree`
1. Create a project: `otree startproject producer_consumer`. The name doesn't
really matter.
1. Navigate into the project directory: `cd producer_consumer`.
1. Clone this repo: `git clone https://github.com/elip12/producer_consumer.git`
1. Edit SESSION_CONFIGS in the settings.py file to look like this:
```
SESSION_CONFIGS = [
    dict(
        name='producer_consumer',
        num_demo_participants=16,
        app_sequence=['producer_consumer'],
        probability_of_same_group=0.5,
        token_store_cost_homogeneous=0,
        token_store_cost_heterogeneous=0,
    ),
 ]
 ```
 1. Start the server: `otree devserver`
 1. Navigate to `localhost:8000` in your browser.
 1. Play the experiment.

Change the number of players: change `players_per_group` in models.py,
and for the demo change `num_demo_participants` in settings.py.

Change the probabilities and the penalties for storing tokens in the session configs.

# Tests
To run the tests: `otree test producer_consumer`. Do this from outer otree directory
(the one with settings.py, not the one you cloned).
The tests should not fail. Warnings are fine.

# TODO - Eli and Skyler

### backend: branch `backend-updates`
- *DONE* everyone will be only 1 color, the other color will be automated
    - *DONE* change models.py, method creating_session
- automated agent rule:
	- only accept own color currency
    - *DONE* for now, always trade if possible
- new treatments:
	- taxes on trading foreign currency:
        - possibility of both or only 1 player paying tax
        - at what time during the trade is this tax invoked?
            tax invoked at time of trade. seller (initially has good) has tax invoked, iff they receive foreign currency
        - can players be taxed for both accepting and storing foreign currency
        in the same round?
        - add options for all possibilities of who is taxed
        - tax has 2 things: amount, and percent-paid-by-consumer, percent-paid-by-producer
- export all data from automated traders


### frontend: branch `frontend-updates`
- depict state in more graphical manner:q

	- graphical representation of object and tokens
    - if you have a token, you will see a red or blue coin thing on your screen.
    - if you have an object, you will see a loaf of bread or something on your screen.
    - if your trading partner has a coin, you will see their coin thing somewhere else.
    - same with if they have an object.
    - changes will be made directly in the templates, using django's if-else
    syntax, and the images or vectors will be static image files.
- history table (each row is 1 period)
	- can use `player.in_round(#)` to get info from previous rounds
    - shows all pertinent information about your previous trades
	- wants graph of history as well as table
        - high charts
    treatments:
    1. only stuff about your previous trades
	2. also how many foreign currencies were accepted in that period for the entire group
        - easiest way is probably to make a method that cycles through all players
        in group in all prevoius rounds, so as not to introduce a new data structure
        that stores specifically foreign currency info

    table
        acceptance rate for domestic-domestic trades ofr foreign
        acceptance rate for domestic-foreign trades of foreign
        demo on monday, release by wednesday
