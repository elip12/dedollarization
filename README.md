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

