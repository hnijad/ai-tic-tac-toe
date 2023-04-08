import configparser
import argparse

config = configparser.ConfigParser()
config.read('app/config.ini')

parser = argparse.ArgumentParser()
parser.add_argument("-team_id", "--team_id", help="team id")
parser.add_argument("-turn", "--turn", help="turn")

args = parser.parse_args()
if args.team_id:
    config.set("input", "team_id", args.team_id)

if args.turn:
    config.set("input", "turn", args.turn)


def get_input_config(key):
    return config['input'].getint(key)


def get_general_config(key):
    return config['general'][key]
