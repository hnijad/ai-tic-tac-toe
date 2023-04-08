import requests
from requests.adapters import HTTPAdapter, Retry


class GameServerClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'userid': '1180',
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-api-key': '<api_key>',
            'User-Agent': 'Python 3.9'
        }
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def make_move(self, team_id, game_id, x, y):
        url = "https://www.notexponential.com/aip2pgaming/api/index.php"
        data = {
            "teamId": team_id,
            "type": "move",
            "gameId": game_id,
            "move": str(x) + "," + str(y)
        }
        response = self.session.post(url, data=data, timeout=30)
        return response.json()

    def get_board(self, game_id):
        url = "https://www.notexponential.com/aip2pgaming/api/index.php?type=boardString&gameId=" + str(game_id)
        response = self.session.get(url)
        return response.json()['output']
