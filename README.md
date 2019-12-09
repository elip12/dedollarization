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
- *DONE* change repo name to dedollarization
- change experiment to not use PEN, use some nonspecific currency that represents
points. write code at the end of the final round that converts points to PEN (peruvian soles)
via some conversion function you dont need to care about the specifics of rn.
- change the definition of a foreign currency transaction. This applies to
bot behavior, and to the table column (FRONTEND). A foreign transaction is possible when
    1. both traders are the same color
    2. trade is possible; one is producer and one is consumer
    3. consumer posesses a foreign currency; if consumer is red, currency is blue, vice versa
A foreign transaction "occurs" when the above occurs, AND
    4. The producer attempted to trade. If the consumer did not attempt to trade, we don't care.
Update the bot and tax behavior accordingly. only encounters in which the first 1 condiitons are met are taxable
- change the token store costs to only change when a token is held for a full round. talk to me if this doesnt make sense
- *DONE* update tests to work with bots
- update tests to be comprehensive

### frontend: branch `frontend-updates`
- smaller token graphics *DONE*
- look into otree support for multiple languages 
Looks doable: https://otree.readthedocs.io/en/latest/misc/internationalization.html
- change trade dropdown to radio buttons *DONE*
- make UI conform to google doc Kristian shared: table on right side, text on left side
right now table is below text. make text take up 30% of width and table take up 70% of width
- make a parameter in the settings file for toggling the visibility of the foreign transactions
column, and make the column only display if the toggle is on. see session.config *DONE* 
- ensure table has most recent rounds on top and most distant on bottom *DONE*
- remove the "your group" col from the table *DONE*
- add a "partner's group" col to the table *DONE*
- add trade possible, trade attempted columns to table *DONE*
- change "traded" col to "trade succeeded" col *DONE*
- change True, False to Yes, No in all relevant table cols *DONE*
- change column "Payoff" to "Round Payoff" *DONE*
- see the thing in the backend about foreign transactions. 
change that table col to make each col row value a decimal representation of the fraction 
[foreign transaction "occurrences / foreign transaction possibilities] *DONE*
- add optional "Tax Paid" and "Storage Cost Paid" cols to the table, and add settings.py toggles for them *DONE*

