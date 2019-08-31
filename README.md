# Instructions
I assume you already have python3 installed.
1. Install otree: `pip3 install -U otree`
1. Create a project: `otree startproject consumer_producer`
    Make sure your project is called consumer_producer.
1. Navigate into the project directory: `cd consumer_producer`
1. Clone this repo: `git clone https://github.com/elip12/producer_consumer.git`
1. Edit SESSION_CONFIGS in the settings.py file to look like this:
```
SESSION_CONFIGS = [
    dict(
        name='consumer_producer',
        num_demo_participants=8,
        app_sequence=['consumer_producer']
    ),
 ]
 ```
 1. Start the server: `otree devserver`
 1. Navigate to `localhost:8000` in your browser.
 1. Play the experiment.

 Please tell me about any bugs that come up, I know there are a few.
 This is a prototype; not all features of the game have been implemented.

 For ease of testing, I am using 2 groups of 4 instead of 2 groups of 8.
 To change this, change num_demo_participants in settings.py,
 and players_per_group in models.py.

 Features not yet implemented:
    - storing tokens costs money
    - payoffs
    - ...

