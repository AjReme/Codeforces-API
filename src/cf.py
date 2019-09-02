from pathlib import Path
from json import load, dump
from tabulate import tabulate
from argparse import ArgumentParser
from cfapi import ext_CodeforcesAPI


SETTINGS_PATH = 'settings.json'


def cf_api():
    update_apinfo_f()
    with open(SETTINGS_PATH, 'r') as file:
        ret = ext_CodeforcesAPI(**load(file))
    return ret


def update_apinfo_f(**kwargs):
    if not Path(SETTINGS_PATH).is_file():
        open(SETTINGS_PATH, 'w+').close()
        settings = {}
    else:
        with open(SETTINGS_PATH, 'r+') as file:
            settings = load(file)
    for name, value in kwargs.items():
        if value is None:
            if settings.get(name) is None:
                settings[name] = None
        else:
            settings[name] = value
    with open(SETTINGS_PATH, 'w') as file:
        dump(settings, file, indent=4)


def last_verdict_f(**kwargs):
    print(cf_api().get_lastVerdict(**kwargs))


def user_verdicts_f(**kwargs):
    print(cf_api().get_verdicts(**kwargs))


def contest_statements_f(**kwargs):
    cf_api().open_contestStatements(contestId=kwargs['contest-number'])


def contest_standings_f(**kwargs):
    kwargs['contestId'] = kwargs['ID']
    del kwargs['ID']
    print(cf_api().contest_standingsTable(**kwargs))


parser = ArgumentParser(description='Codeforces.com API requests')
subparsers = parser.add_subparsers(help='Main commands')


update_apinfo = subparsers.add_parser(
    'update-api-info',
    help='Update key, secret or language'
)
update_apinfo.add_argument(
    '--key',
    nargs='?',
    type=str,
    help='API key'
)
update_apinfo.add_argument(
    '--secret',
    nargs='?',
    type=str,
    help='API secret'
)
update_apinfo.add_argument(
    '--lang',
    nargs='?',
    type=str,
    default='en',
    help='Language. Can be \"en\" or \"ru\"'
)
update_apinfo.add_argument(
    '--handle',
    nargs='?',
    type=str,
    help='Your handle'
)
update_apinfo.set_defaults(func=update_apinfo_f)


last_verdict = subparsers.add_parser(
    'last-verdict',
    help='Get last verdict of specified user.\
          You can provide handle or use your own'
)
last_verdict.add_argument(
    '--handle',
    nargs='?',
    type=str,
    help='Handle of user'
)
last_verdict.set_defaults(func=last_verdict_f)


user_verdicts = subparsers.add_parser(
    'user-verdicts',
    help='Get last verdict of specified user.'
)
user_verdicts.add_argument(
    '--handle',
    type=str,
    default=None,
    help='Handle of user'
)
user_verdicts.add_argument(
    '--from-sub',
    nargs='?',
    type=int,
    default=1,
    help='From which submission to start?'
)
user_verdicts.add_argument(
    '--count',
    nargs='?',
    type=int,
    default=10,
    help='How many submissions to show?'
)
user_verdicts.add_argument(
    '--mode',
    nargs='?',
    type=str,
    default='fancy_grid',
    help='Mode for tabulate'
)
user_verdicts.set_defaults(func=user_verdicts_f)


contest_statements = subparsers.add_parser(
    'open-statements',
    help='Save and open statements of contest #XXX in browser'
)
contest_statements.add_argument(
    'contest-number',
    type=int,
    help='# of contests'
)
contest_statements.set_defaults(func=contest_statements_f)


contest_standings = subparsers.add_parser(
    'contest-standings',
    help='Show current contest standings'
)
contest_standings.add_argument(
    'ID',
    type=int,
    help='Contest ID'
)
contest_standings.add_argument(
    '--from-row',
    nargs='?',
    type=int,
    default=1,
    help='From which line to show results?'
)
contest_standings.add_argument(
    '--count',
    nargs='?',
    type=int,
    default=100,
    help='How many lines to show?'
)
contest_standings.add_argument(
    '--mode',
    nargs='?',
    type=str,
    default='fancy_grid',
    help='Mode for tabulate'
)
contest_standings.set_defaults(func=contest_standings_f)

args = dict(parser.parse_args()._get_kwargs())
args['func'](**dict((i, j) for i, j in args.items() if i != 'func'))

print('Success!')
