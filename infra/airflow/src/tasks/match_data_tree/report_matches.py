import requests

def report_matches_to_mongo():

    response = requests.post('https://api:8080/reporter/match')

