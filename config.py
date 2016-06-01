###
# Jarvis Configuration Dictionaries
#
# creds['email'] = The email you want Jarvis to listen to.
# creds['password'] = The password for creds['email'].
# creds['maker'] = The key for your the IFTTT Maker Channel.
# creds['sender'] = The email address authorized to talk to Jarvis.
###

creds = dict(
    email = "<INSERT EMAIL HERE>",
    password = "<INSERT PASSWORD HERE>",
    maker = "<INSERT MAKER TOKEN HERE>",
    sender = "<INSERT SENDER HERE>"
)

imap = dict(
    server = "imap.gmail.com",
    port = "993",
    folder = "INBOX"
)

smtp = dict (
    server = "smtp.gmail.com",
    port = "465"
)
