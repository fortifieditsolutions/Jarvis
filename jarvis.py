#!/usr/bin/python3

import imaplib
import config
import email
import requests
import sys
import re

###
# Jarvis - An IFTTT Automation Bot
#
# @author = Travis Garrell
# @email = tgarrelmn@gmail.com
###

class Jarvis():
    '''
    The bot is designed to be instanciated in a script to be extended, or to be run using the
    self contained main declaration below.
    '''

    def __init__(self, _email, _password, _sender, _maker, _imap_server, _imap_port, _imap_folder):
        '''
        _email = The email address used to login to the bot's IMAP account.
        _password = The password for the bot's IMAP account.
        _sender = An email that is authorized to communicate with the bot.
        _maker = The IFTTT Maker Channel Token.
        _imap_server = The IMAP server the bot will communicate with.
        _imap_port = The Port of the IMAP server the bot will communicate with.
        _imap_folder = The IMAP Folder the bot will read from.
        '''

        '''
        Strings used to generate the URLs for Maker Channel Requests.
        '''
        self.MAKER_REQUEST_PREFIX = "https://maker.ifttt.com/trigger/"
        self.MAKER_REQUEST_SUFFIX = "/with/key/"

        '''
        Instance Variables.
        '''
        self._email = _email
        self._password = _password
        self._sender = _sender
        self._maker = _maker
        self._imap_server = _imap_server
        self._imap_port = _imap_port
        self._imap_folder = _imap_folder

    def get_email(self):
        return self._email

    def get_maker(self):
        return self._maker

    def imap_connection(self):
        '''
        Creates an IMAP connection using imaplib and the provided credentials
        and connection information. It will use whatever folder was specified
        during Jarvis' creation.
        '''
        M = imaplib.IMAP4_SSL(host=self._imap_server, port=self._imap_port)

        try:
            rv, data = M.login(self._email,self._password)
        except imaplib.IMAP4.error:
            print("Login Failed. Exiting...")
            sys.exit(1)


        rv, data = M.select(self._imap_folder)
        return M

    def process_mailbox(self,M):
        '''
        Process the mailbox. Will filter for only messages from a specified email address.
        Iterates through the messages, sends the subject line off for processing, ignoring the body.
        Finally, it deletes the processed message and then continues iteration.
        '''
        mail_filter = '(FROM {sender})'.format(sender=self._sender)
        rv, data = M.search(None, mail_filter)
        if rv != 'OK':
            return
        for num in data[0].split():
            rv, data = M.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("ERROR getting message", num)
                return

            try:
                msg = email.message_from_bytes(data[0][1])
                subject_header = email.header.make_header(email.header.decode_header(msg['Subject']))
                subject = str(subject_header)
                print(subject)
                self.process_subject(subject.lower())
            except Exception as e:
                print(str(e))
            print("Deleting Message...")
            '''
            Message Deletion per RFC
            '''
            M.store(num, '+FLAGS', '\\Deleted')
            M.expunge()
        return

    def process_subject(self, subject):
        '''
        Process the subject.
        Add custom patern matching on the subject here.
        The more vague the pattern, the more natural speech is allowed.
        '''
        if subject.find('lights') != -1:
            self.handle_lights(subject)

    ##############################
    # Endpoint Handlers
    ##############################
    def handle_lights(self, subject):
        '''
        How to handle when the word lights appears in the subject.
        The more vague the pattern matchin, the more natural speech is allowed.
        Each function name (ie. jarvis_lights_on) corresponds to the "event name" referenced
        in a Maker IFTTT Recipe for easier mapping.
        '''

        if subject.find('on') != -1:
            self.jarvis_lights_on()
        if subject.find('off') != -1:
            self.jarvis_lights_off()
        if subject.find('toggle') != -1:
            self.jarvis_lights_toggle()
        if subject.find('set') != -1:
            brightness_list = re.findall('\d+',subject)
            brightness = brightness_list[0]
            if int(brightness) > 100:
                brightness = "100"
            elif int(brightness) < 0:
                brightness = "0"
            self.jarvis_lights_brightness(brightness)

    ##############################
    # Maker Handlers
    ##############################
    def make_url(self, event_name):
        '''
        Create the URL that will be used to trigger an IFTTT Maker event.
        '''
        url = self.MAKER_REQUEST_PREFIX+event_name+self.MAKER_REQUEST_SUFFIX+self._maker
        return url

    def send_request(self, url):
        '''
        Send the HTTP GET request to the IFTTT Maker channel.
        '''
        requests.get(url)

    def send_post(self, url, post_data):
        '''
        Send the HTTP POST request to the IFTTT Maker channel.
        '''
        requests.post(url,data=post_data)

    def jarvis_lights_on(self):
        '''
        Turn on the lights.
        '''
        event_name = "jarvis_lights_on"
        maker_url = self.make_url(event_name)
        self.send_request(maker_url)
    def jarvis_lights_off(self):
        '''
        Turn off the lights.
        '''
        event_name = "jarvis_lights_off"
        maker_url = self.make_url(event_name)
        self.send_request(maker_url)
    def jarvis_lights_toggle(self):
        '''
        Toggle the lights.
        '''
        event_name = "jarvis_lights_toggle"
        maker_url = self.make_url(event_name)
        self.send_request(maker_url)

    def jarvis_lights_brightness(self, brightness):
        '''
        Set the brightness for the lights.
        '''
        event_name = "jarvis_lights_brightness"
        maker_url = self.make_url(event_name)
        post_data = "{\"value1\":\"%s\"}" % brightness
        self.send_post(maker_url, post_data)

if __name__ == '__main__':

    '''
    Read the config file (config.py) for these values
    '''
    _email = config.creds['email']
    _password = config.creds['password']
    _sender = config.creds['sender']
    _maker = config.creds['maker']
    _imap_server = config.imap['server']
    _imap_port = config.imap['port']
    _imap_folder = config.imap['folder']

    '''
    Instanciate Jarvis
    '''
    jarvis = Jarvis(_email, _password, _sender, _maker, _imap_server, _imap_port, _imap_folder)

    '''
    Get an IMAP Connection
    '''
    M = jarvis.imap_connection()

    '''
    Process Library
    '''
    jarvis.process_mailbox(M)
