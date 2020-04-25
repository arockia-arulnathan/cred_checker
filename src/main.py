import sys
import os
import time
import yaml
from getpass import getpass
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from util.common import Configuration
from logzero import logger as LOG_OBJ
import argparse
from cred_checker import Cred_Checker


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)

def generate_results(data):

    for provider, result in data.items():
        if result['status']:
            LOG_OBJ.info(f"[+] {provider} - Success")
        else:
            LOG_OBJ.error(f"[-] {provider} - Failed")

def main():
    try:
        for site in sites:
            site_status, site_result = checker_obj.site_checker(site_name=site)
            credential_check_results[site] = {'status': site_status, 'message': site_result}
        generate_results(data = credential_check_results)
    except Exception as e:
        LOG_OBJ.error(f"Exception occurred. Exception: {str(e)}")

if __name__ == "__main__":
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(BASE_PATH,'util/config.yaml')) as f_handle:
        CONFIG = yaml.load(f_handle.read(), Loader=yaml.FullLoader)
    parser = argparse.ArgumentParser(description="Credential Checker V 1.0",add_help=False, formatter_class=CapitalisedHelpFormatter)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                help='Show this help message and exit.')
    parser.add_argument('-l','--list_sites', help='List available social media sites', action='store_true')
    parser.add_argument('-cs','--custom_sites', help='Specific sites to check. Use comma separated site codes in the sites list')
    parser.add_argument('-u', '--username', help='Ignore this param to enter password during runtime')
    parser.add_argument('-p', '--password', help='Ignore this param to enter password during runtime')
    args = parser.parse_args()
    credential_check_results = {}

    # List the available sites
    if args.list_sites:
        sites = CONFIG.keys()
        for i,site in enumerate(sites):
            print(f"{i+1}. {site.capitalize()}")

    # Check for username and password
    if args.username:
        USERNAME = args.username
    else:
        USERNAME = input("Enter the username: ")
    if args.password:
        PASSWORD = args.password
    else:
        PASSWORD = getpass("Enter the password: ")
    
    # Populate the sites list from user input or all sites.
    if args.custom_sites:
        sites = args.custom_sites.split(",")
        site_check = [True if x in CONFIG.keys() else False  for x in sites ]
        if not all(site_check):
            LOG_OBJ.warn("Please check the sites list")
    else:
        sites = CONFIG.keys()

    checker_obj = Cred_Checker(username=USERNAME, password=PASSWORD, log_obj=LOG_OBJ)
    main()