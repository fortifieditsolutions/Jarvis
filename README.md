JARVIS - An IFTTT Automation Bot
=================================

Introduction
------------
Using If This Then That (IFTTT) it is possible to automate a wide variety of tasks from Internet of Things (IoT) connected
"Smart Devices" to simple social media micromanaging, IFTTT can probably do it. Potentially the most powerful Channel on IFTTT
is the GMail channel, which allows you to create Recipes that will run upon receiving an email that matches a particular search 
or even send an email as a response to a trigger.

The problem, however, is that the GMail channel is sometimes slow to respond, owing to IFTTT's 15 minute polling intervals. That's
where Jarvis comes in. Jarvis acts as a middle man or a bridge between you and IFTTT.

Logic Flow
----------
The flow of logic goes a little something like this:
- Send an email to an email account readable by Jarvis.
- Jarvis listens for new mail from you, and you alone.
- Jarvis processes the subject line of the email and determines what should be done.
- A request to the Maker IFTTT Channel is made.
- A previously created recipe that is triggered by a Maker Event is run.
- The email is then removed from Jarvis' inbox, so repeats do not occur.
- Jarvis goes back to listening for new emails.

Benefits
---------
To name a few benefits of utilizing Jarvis as a bridge:
- Faster response times than the GMail Channel of IFTTT.
- Execute more IFTTT recipes with a single trigger (think of it like a Macro).
- Voice dictatioin for emails on phones and smart watches allow you to have natural speech input.

Setup
-----
Jarvis requires the following:
- Python3
- A gmail account for the bot to use (NOTE: You may have to enable "less secure app connection" in the gmail settings
- An IFTTT Account
Jarvis requires the following Python libraries:
- imaplib
- email
- requests
- sys

Configuration
--------------
Jarvis, when run as a standalone script, will read in values from an imported "config.py" file. This config file contains
nothing more than a few python dictionary definitions containing the necessary information for Jarvis to connect.
In the provided config.py file, update the values for the "creds" dictionary as follows:
- email: This is the email address that Jarvis will use to connect over IMAP.
- password: This is the password for the IMAP account Jarvis will use.
- maker: This is your IFTTT Maker Channel key, which can be found here: https://maker.ifttt.com/
- sender: This is the only email authorized to communicate with Jarvis. Jarvis will ignore all other emails.
