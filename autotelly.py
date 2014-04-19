"""
Autotelly: Manage your Unotelly account from command-line
"""
import os
import string
import argparse
import json
from random import choice, randint

import requests
from BeautifulSoup import BeautifulSoup
from termcolor import colored

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
DNS_SERVERS = ['69.42.56.54', '23.21.182.24']


def rndstr(size=8):
    return ''.join(choice(string.ascii_lowercase+string.digits) for x in range(size))


class Session:
    token = ''
    cookies = dict()
    username = False
    password = False
    userid = False

    def get_token(self, content):
        soup = BeautifulSoup(content)
        self.token = soup.find('input', attrs={'type': 'hidden'}).get('value'),

    def get_cookies(self, headers):
        session_name, session = headers['set-cookie'].split(';')[0].split('=')
        self.cookies = {session_name: session}

    def from_response(self, response, trial=False):
        self.get_cookies(response.headers)
        self.get_token(response.text)
        if trial:
            self.username = '%s@%s.com' % (rndstr(), rndstr())
            self.password = '%s' % randint(1, 999999)


if __name__ == "__main__":
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description='Manage your Unotelly account')
    parser.add_argument('--trial', action='store_true', default=False, help='Register an anonymous trial user to test Unotelly services.')
    parser.add_argument('--autoconfig', action='store_true', default=False, help='Create a config.json file with your trial username and password.')
    parser.add_argument('--verbose', action='store_true', default=False, help='Show additional information about autotelly.')
    parser.add_argument('--username', default=False, help='Your Unotelly username. If not provided the one in config.json will be used.')
    parser.add_argument('--password', default=False, help='Your Unotelly password. If not provided the one in config.json will be used.')
    args = parser.parse_args()

    session = Session()
    if not args.trial:
        session.from_response(requests.get('http://quickstart3.unotelly.com/login'))
        # Fetch username/password from CLI arguments or config.json
        if args.username and args.password:
            print('Logging in with supplied username and password...')
            session.username, session.password = args.username, args.password
        else:
            try:
                config = json.loads(open(os.path.join(PROJECT_PATH, 'config.json'), 'r').read())
                session.username, session.password = config['username'], config['password']
            except IOError:
                print(colored('No config.json file found', 'red'))

        # Login
        print('Logging in...')
        login_form_data = {'_token': session.token, 'email': session.username, 'password': session.password}
        login = requests.post('http://quickstart3.unotelly.com/login', data=login_form_data, cookies=session.cookies)
        if 'login' in login.history[0].headers['location']:
            print(colored('Can\'t login: username or password error.', 'red'))
            exit(1)

        soup = BeautifulSoup(login.text)

        # Display account information
        if args.verbose:
            for userinfo in soup.table.findAll('td'):
                print(colored(userinfo.text, 'yellow'))

        # Update IP
        print('Updating IP adddress...')
        update_url = soup.find('a', attrs={'id': 'auto_update_ip'})['href']
        update = requests.get(update_url, cookies=session.cookies)
        network_id = update.history[0].headers['location'].split('=')[-1]
        print(colored('Network %s updated!' % network_id, 'green'))
    else:
        # Register trial account
        print('Creating anonymous trail account...')
        # Fetch session and token for registration, setup registation form data
        session.from_response(requests.get('http://quickstart3.unotelly.com/signup'), trial=True)
        registration_form_data = {'_token': session.token, 'firstname': '%s %s' % (rndstr(9), rndstr(12)), 'email': session.username, 'password': session.password}

        # Register and get userid
        registration = requests.post('http://quickstart3.unotelly.com/signup', data=registration_form_data, cookies=session.cookies)
        session.userid = registration.history[0].headers['location'].split('/')[-1]
        print('Username: {username}\nPassword: {password}'.format(username=registration_form_data['email'], password=registration_form_data['password']))

        # Enable services
        enable_netflix_us = requests.post('http://quickstart3.unotelly.com/dynamo/%s/updateAjax' % session.userid, data={'4':'1'}, cookies=session.cookies)
        response = json.loads(enable_netflix_us.text)
        print(colored(response['feedback'], 'green'))
        if response['status'] == 1:
            print(colored('Change your DNS servers to: %s' % '/ '.join(DNS_SERVERS), 'yellow'))

        if args.autoconfig:
            f = file(os.path.join(PROJECT_PATH, 'config.json'), 'w')
            f.write(json.dumps({'username': session.username, 'password': session.password}))
            f.close()
            print(colored('A config.json file was created with your trial account.', 'yellow'))
