<h1 align="center">Project 3 - Generalized Tic Tac Toe</h1>


## Table of Contents

- [Build](#install)
- [Usage](#usage)
- [Implementation](#implementation)
- [Dependencies](#dependencies)

## Build
To build and run application execute the following commands.

```shell
python app/main.py -team_id=1388 -turn=2
```

To run the unit test cases, run the following command.

```shell
python -m unittest tests/test_board.py
```


## Usage
To run this program as an agent, we need to configure following parameters in ```app/config.ini```.
<li> The `api_key` parameter is API key for accessing game server, and it is required param </li>
<li> The `timeout` parameter is second in which game server declares our agent out of game. Currently, it is ignored </li>
<li> The `user_id` parameter is user id in game server, and it should be consistent with api_key. It is required param </li>
<li> The `game_id` parameter is game in which agent is playing. It is required param</li>
<li> The `board_size` parameter is size of the board in game. It is required param</li>
<li> The `target` parameter is the target in game. It is required param</li>
<li>The `team_id` parameter is the team id. It is required param, and it can also be passed as command line argument. </li>
<li>The `turn` parameter denotes if the agent is first to start or second. It is required param </li>
It accepts the following command line argument(s) <br>

## Implementation
```app/client/game_server_client.py``` class is responsible for making the api calls to server. <br>
```app/model/board.py``` class represents board in tic-tac-toe and provides some utility functions to use in game such
as making move, syncing state from with server board string etc. <br>
```app/config.py``` is responsible for parsing the config values from  ```app/config.ini``` and command line. <br>
```app/minimax.py``` implements standard minimax algorithm with alpha beta pruning. <br>
and finally main.py is driver of the whole program.


## Dependencies
The project uses the python's requests library to make the api calls to the server. In the testing process we have used
python3.
