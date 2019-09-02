'''
It's a simple Codeforces API wrapper, that allows you to write simple
requests to Codeforces API, provides documentated classes for results,
send code, get standings in console and so on.
'''

__version__ = '0.0.3a'

from os import makedirs
from time import time
from pathlib import Path
from hashlib import sha512
from tabulate import tabulate
from datetime import datetime
from random import SystemRandom
from robobrowser import RoboBrowser
from webbrowser import open_new_tab
from os.path import join as join_path
from requests import get as http_request
from string import ascii_lowercase, digits


class CodeforcesResponse:
    '''
    Basic class for all Codeforces API responses.
    '''

    def __init__(self, json: dict):
        '''
        Initializes user object by gived json. Json must be a dict
        object.
        '''
        for name, value in json.items():
            setattr(self, name, value)


class User(CodeforcesResponse):
    '''
    Represents a Codeforces user.
    handle                  : str. Codeforces user handle.
    email                   : str. Shown only if user allowed to share
                                   his contact info.
    vkId                    : str. User id for VK social network. Shown
                                   only if user allowed to share his
                                   contact info.
    openId                  : str. Shown only if user allowed to share
                                   his contact info.
    firstName               : str. Localized. Can be absent.
    lastName                : str. Localized. Can be absent.
    country                 : str. Localized. Can be absent.
    city                    : str. Localized. Can be absent.
    organization            : str. Localized. Can be absent.
    contribution            : int. User contribution.
    rank                    : str. Localized.
    rating                  : int.
    maxRank                 : str. Localized.
    maxRating               : int.
    lastOnlineTimeSeconds   : int. Time, when user was last seen online,
                                   in unix format.
    registrationTimeSeconds : int. Time, when user was registered, in
                                   unix format.
    friendOfCount           : int. Amount of users who have this user
                                   in friends.
    avatar                  : str. User's avatar URL.
    titlePhoto              : str. User's title photo URL.
    '''

class BlogEntry(CodeforcesResponse):
    '''
    Represents a Codeforces blog entry. May be in either short or full
    version.
    id                      : int.
    originalLocale          : str. Original locale of the blog entry.
    creationTimeSeconds     : int. Time, when blog entry was created,
                                   in unix format.
    authorHandle            : str. Author user handle.
    title                   : str. Localized.
    content                 : str. Localized. Not included in short
                                   version.
    locale                  : str.
    modificationTimeSeconds : int. Time, when blog entry has been
                                   updated, in unix format.
    allowViewHistory        : bool. If True, you can view any specific
                                    revision of the blog entry.
    tags                    : str list.
    rating                  : int.
    '''


class Comment(CodeforcesResponse):
    '''
    Represents a comment.
    id                  : int.
    creationTimeSeconds : int. Time, when comment was created, in
                               unix format.
    commentatorHandle   : str.
    locale              : str.
    text                : str.
    parentCommentId     : int. Can be absent.
    rating              : int.
    '''


class RecentAction(CodeforcesResponse):
    '''
    Represents a recent action.
    timeSeconds : int. Action time, in unix format.
    blogEntry     : BlogEntry in short form. Can be absent.
    comment     : Comment. Can be absent.
    '''

    def __init__(self, json: dict):
        super().__init__(json)
        if hasattr(self, 'blogEntry'):
            self.blogEntry = BlogEntry(self.blogEntry)
        if hasattr(self, 'comment'):
            self.comment = Comment(self.comment)


class RatingChange(CodeforcesResponse):
    '''
    Represents a participation of user in rated contest.
    contestId               : int.
    contestName             : str. Localized.
    handle                  : str. Codeforces user handle.
    rank                    : int. Place of the user in the contest.
                                   This field contains user rank on
                                   the moment of rating update. If
                                   afterwards rank changes (e.g.
                                   someone get disqualified), this
                                   field will not be update and will
                                   contain old rank.
    ratingUpdateTimeSeconds : int. Time, when rating for the contest
                                   was update, in unix-format.
    oldRating               : int. User rating before the contest.
    newRating               : int. User rating after the contest.
    '''


class Contest(CodeforcesResponse):
    '''
    Represents a contest on Codeforces.
    id                  : int.
    name                : str.  Localized.
    type                : Enum: CF, IOI, ICPC. Scoring system used for
                                the contest.
    phase               : Enum: BEFORE, CODING, PENDING_SYSTEM_TEST,
                                SYSTEM_TEST, FINISHED.
    frozen              : bool. If true, then the ranklist for the contest
                                is frozen and shows only submissions,
                                created before freeze.
    durationSeconds     : int.  Duration of the contest in seconds.
    startTimeSeconds    : int.  Can be absent. Contest start time in unix
                                format.
    relativeTimeSeconds : int.  Can be absent. Number of seconds, passed
                                after the start of the contest. Can be
                                negative.
    preparedBy          : str.  Can be absent. Handle of the user, how
                                created the contest.
    websiteUrl          : str.  Can be absent. URL for contest-related
                                website.
    description         : str.  Localized. Can be absent.
    difficulty          : int.  Can be absent. From 1 to 5. Larger number
                                means more difficult problems.
    kind                : str.  Localized. Can be absent. Human-readable
                                type of the contest from the following
                                categories:
                                Official ACM-ICPC Contest,
                                Official School Contest,
                                Opencup Contest,
                                School/University/City/Region Championship,
                                Training Camp Contest,
                                Official International Personal Contest,
                                Training Contest.
    icpcRegion          : str.  Localized. Can be absent. Name of the
                                ICPC Region for official ACM-ICPC contests.
    country             : str.  Localized. Can be absent.
    city                : str.  Localized. Can be absent.
    season              : str.  Can be absent.
    '''


class Member(CodeforcesResponse):
    '''
    Represents a member of a party.
    handle : str. Codeforces user handle.
    '''


class Party(CodeforcesResponse):
    '''
    Represents a party, participating in a contest.
    contestId           : int.  Can be absent. Id of the contest, in
                                which party is participating.
    members             : List of Member. Members of the party.
    participantType     : Enum: CONTESTANT, PRACTICE, VIRTUAL, MANAGER,
                                OUT_OF_COMPETITION.
    teamId              : int.  Can be absent. If party is a team,
                                then it is a unique team id. Otherwise,
                                this field is absent.
    teamName            : str.  Localized. Can be absent. If party is a
                                team or ghost, then it is a localized
                                name of the team. Otherwise, it is absent.
    ghost               : bool. If true then this party is a ghost. It
                                participated in the contest, but not on
                                Codeforces. For example, Andrew Stankevich
                                Contests in Gym has ghosts of the
                                participants from Petrozavodsk Training Camp.
    room                : int.  Can be absent. Room of the party. If absent,
                                then the party has no room.
    startTimeSeconds    : int.  Can be absent. Time, when this party started
                                a contest.
    '''

    def __init__(self, json: dict):
        super().__init__(json)
        self.members = list(map(Member, self.members))


class Problem(CodeforcesResponse):
    '''
    Represents a problem.
    contestId       : int.   Can be absent. Id of the contest, containing
                             the problem.
    problemsetName  : str.   Can be absent. Short name of the problemset
                             the problem belongs to.
    index           : str.   Usually a letter of a letter, followed by a
                             digit, that represent a problem index in a
                             contest.
    name            : str.   Localized.
    type            : Enum:  PROGRAMMING, QUESTION.
    points          : float. Can be absent. Maximum ammount of points for
                             the problem.
    rating          : int.   Can be absent. Problem rating (difficulty).
    tags            : list of str objects. Problem tags.
    '''


class ProblemStatistics(CodeforcesResponse):
    '''
    Represents a statistic data about a problem.
    contestId   : int. Can be absent. Id of the contest, containing
                       the problem.
    index       : str. Usually a letter of a letter, followed by a digit,
                       that represent a problem index in a contest.
    solvedCount : int. Number of users, who solved the problem.
    '''


class Submission(CodeforcesResponse):
    '''
    Represents a submission.
    id                  : int.
    contestId           : int.  Can be absent.
    creationTimeSeconds : int.  Time, when submission was created,
                                in unix-format.
    relativeTimeSeconds : int.  Number of seconds, passed after the
                                start of the contest (or a virtual
                                start for virtual parties), before
                                the submission.
    problem             : Problem object.
    author              : Party object.
    programmingLanguage : str.
    verdict             : Enum: FAILED, OK, PARTIAL, COMPILATION_ERROR,
                                RUNTIME_ERROR, WRONG_ANSWER,
                                PRESENTATION_ERROR, TIME_LIMIT_EXCEEDED,
                                MEMORY_LIMIT_EXCEEDED,
                                IDLENESS_LIMIT_EXCEEDED, SECURITY_VIOLATED,
                                CRASHED, INPUT_PREPARATION_CRASHED,
                                CHALLENGED, SKIPPED, TESTING, REJECTED.
                                Can be absent.
    testset             : Enum: SAMPLES, PRETESTS, TESTS,
                                CHALLENGES, TESTS1, ..., TESTS10.
                                Testset used for judging the submission.
    passedTestCount     : int.  Number of passed tests.
    timeConsumedMillis  : int.  Maximum time in milliseconds, consumed by
                                solution for one test.
    memoryConsumedBytes : int.  Maximum memory in bytes, consumed by
                                solution for one test.
    '''

    def __init__(self, json: dict):
        super().__init__(json)
        self.problem = Problem(self.problem)
        self.author = Party(self.author)


class Hack(CodeforcesResponse):
    '''
    Represents a hack, made during Codeforces Round.
    id                  : int.
    creationTimeSeconds : int.  Hack creation time in unix format.
    hacker              : Party object.
    defender            : Party object.
    verdict             : Enum: HACK_SUCCESSFUL, HACK_UNSUCCESSFUL,
                                INVALID_INPUT, GENERATOR_INCOMPILABLE,
                                GENERATOR_CRASHED, IGNORED, TESTING,
                                OTHER. Can be absent.
    problem             : Problem object. Hacked problem.
    test                : str.  Can be absent.
    judgeProtocol       : Object with three fields: "manual", "protocol"
                          and "verdict". Field manual can have values
                          "true" and "false". If manual is "true" then
                          test for the hack was entered manually. Fields
                          "protocol" and "verdict" contain human-readable
                          description of judge protocol and hack verdict.
                          Localized. Can be absent.
    '''

    def __init__(self, json: dict):
        super().__init__(json)
        self.hacker = Party(self.hacker)
        self.defender = Party(self.defender)


class ProblemResult(CodeforcesResponse):
    '''
    Represents a submissions results of a party for a problem.
    points                      : float.
    penalty                     : int.  Penalty (in ICPC meaning) of
                                        the party for this problem.
    rejectedAttemptCount        : int.  Number of incorrect submissions.
    type                        : Enum: PRELIMINARY, FINAL. If type is
                                        PRELIMINARY then points can
                                        decrease (if, for example, solution
                                        will fail during system test).
                                        Otherwise, party can only increase
                                        points for this problem by submitting
                                        better solutions.
    bestSubmissionTimeSeconds   : int.  Number of seconds after the start of
                                        the contest before the submission,
                                        thatbrought maximal amount of points
                                        for this problem.
    '''


class RanklistRow(CodeforcesResponse):
    '''
    Represents a ranklist row.
    party                       : Party object. Party that took a
                                  corresponding place in the contest.
    rank                        : int.   Party place in the contest.
    points                      : float. Total ammount of points,
                                         scored by the party.
    penalty                     : int.   Total penalty (in ICPC meaning)
                                         of the party.
    successfulHackCount         : int.
    unsuccessfulHackCount       : int.
    problemResults              : List of ProblemResult objects.
                                  Party results for each problem.
                                  Order of the problems is the same
                                  as in "problems" field of the returned
                                  object.
    lastSubmissionTimeSeconds   : int.   For IOI contests only. Time in
                                         seconds from the start of the
                                         contest to the last submission
                                         that added some points to the
                                         total score of the party.
    '''

    def __init__(self, json: dict):
        super().__init__(json)
        self.party = Party(self.party)
        self.problemResults = list(map(ProblemResult,
                                       self.problemResults))


class CodeforcesAPI:
    '''
    A wrapper class for simple and convenient use of Codeforces.com
    API and page requests. You don't need to read any info about API
    if you don't need anything unusual to do with it.
    '''

    _site_link = 'http://codeforces.com/'
    _api_link = 'http://codeforces.com/api/'

    def __init__(self,
                 key: str = None,
                 secret: str = None,
                 lang: str = 'en'):
        '''
        Initialize a Codeforces wrapper for single user.
        key      : str. User API key from https://codeforces.com/settings/api
        secret   : str. User API secret from https://codeforces.com/settings/api
        lang : str. Local language for requests. Can be \"en\" or \"ru\"
        '''
        self.key = key
        self.secret = secret
        self.lang = lang

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, value):
        self._secret = value

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value: str):
        if value == 'ru' or value == 'en':
            self._lang = value
        else:
            raise TypeError('Language can be only \"en\" \
                             or \"ru\", not {}'.format(value))

    def _to_http(self, param, value):
        '''
        Convert param into HTTP format: param=value.
        '''
        if isinstance(value, list):
            value = ';'.join(map(str, value))
        else:
            value = str(value)
        return '{}={}'.format(param, value)

    def _sorted_str_kwargs(self, **kwargs):
        '''
        Returns list of params and values, sorted lexicographically.
        '''
        lst = list()
        for param, value in kwargs.items():
            if value is not None:
                lst.append(self._to_http(param, value))
        return sorted(lst)

    def _get_url(self, **kwargs):
        '''
        Create url by sorted lexicographically kwargs:
        param_1=value_1&param_2=value_2...param_n=value_n.
        '''
        return '&'.join(self._sorted_str_kwargs(**kwargs))

    def _url_api_request(self, method: str, **kwargs):
        '''
        Creates url for API request. Uses key and secret from
        https://codeforces.com/settings/api if provided.
        '''
        kwargs['lang'] = self.lang
        if self._key is not None and self._secret is not None:
            kwargs['time'] = int(time())
            kwargs['apiKey'] = self._key
            rand = ''.join(SystemRandom().choice(ascii_lowercase +
                                                 digits) for i in range(6))
            sig = rand + sha512((rand + '/' + method + '?' +
                                 self._get_url(**kwargs) + '#' +
                                 self._secret).encode('utf-8')).hexdigest()
            kwargs['apiSig'] = sig
        return self._get_url(**kwargs)

    def _check_request(self, request):
        if not request.ok:
            raise ConnectionError('Request status \
                                  is {}'.format(self.last_api.status_code))

    def request_api(self, method: str, **kwargs):
        '''
        Requests http://codeforces.com/api/<method_name> and returns
        json object with info from site. Type of method must be a
        string.
        Uses key and secret if provided. Make sure you have set
        correct system time.
        Checks the request.Response object for valid answer.
        Raises ConnectionError if request is not OK.
        Cryptographically secure.
        Creates last_api dict. Contains JSON with last API request result.
        Example: cf.request_api('user.info', handles=['tourist', 'Petr'])
        '''
        self.last_api = http_request(
            self._api_link +
            method + '?' +
            self._url_api_request(method, **kwargs)
        )
        self._check_request(self.last_api)
        self.last_api = self.last_api.json()
        if self.last_api['status'] != 'OK':
            raise ConnectionError('Codeforces API error: \
                                  {}', self.last_api['comment'])
        return self.last_api

    def blogEntry_comments(self, blogEntryId: int):
        '''
        Codeforces API name: blogEntry.comments.
        Returns a list of Comment to the specified blog entry.
        blogEntry_id (Required): int. id of the blog entry. It can be
                                      seen in blog entry URL.
        Example: cf.blogEntry_comments(blogEntryId=79)
        '''
        self.request_api('blogEntry.comments',
                         blogEntryId=blogEntryId)
        return list(map(Comment, self.last_api['result']))

    def blogEntry_view(self, blogEntryId: int):
        '''
        Codeforces API name: blogEntry.view.
        Returns BlogEntry.
        blogEntryId (Required): int. Id of the blog entry. It can be
                                     seen in blog entry URL.
        Example: cf.blogEntry_view(blogEntryId=79)
        '''
        self.request_api('blogEntry.view',
                         blogEntryId=blogEntryId)
        return BlogEntry(self.last_api['result'])

    def contest_hacks(self, contestId: int):
        '''
        Codeforces API name: contest.hacks.
        Returns list of Hack in the specified contests. Full
        information about hacks is available only after some
        time after the contest end. During the contest user can
        see only own hacks.
        contestId (Required): int. Id of the contest. It is not the
                                   round number. It can be seen in
                                   contest URL.
                                   For example: .../contest/566/status
        Example: cf.contest_hacks(contestId=566)
        '''
        self.request_api('contest.hacks',
                         contestId=contestId)
        return list(map(Hack, self.last_api['result']))

    def contest_list(self, gym: bool = False):
        '''
        Codeforces API name: contest.list.
        Returns information about all available contest as list of
        contest_ob. If this method is called not anonymously, then
        all available contests for a calling user will be returned
        too, including mashups and private gyms.
        gym : bool. If true - than gym contests are returned. Otherwide,
                    regular contests are returned.
        Example: cf.contest_list(gym=True)
        '''
        self.request_api('contest.list',
                         gym=gym)
        return list(map(Contest, self.last_api['result']))

    def contest_ratingChanges(self, contestId: int):
        '''
        Codeforces API name: contest.ratingChanges.
        Returns rating changes after the contest as list
        of RatingChange.
        contestId (Required): int. Id of the contest. It is not
                                    the round number. It can be
                                    seen in contest URL.
        Example: cf.contest_ratingChanges(contestId=566)
        '''
        self.request_api('contest.ratingChanges',
                         contestId=contestId)
        return list(map(RatingChange, self.last_api['result']))

    def contest_standings(self, contestId: int, from_row: int = None,
                          count: int = None, handles: str = None, room: int = None,
                          showUnofficial: bool = None):
        '''
        Codeforces API name: contest.standings.
        Returns the description of the contest and the
        requested part of the standings as list of 3 lists:
        1)  List of Contest object.
        2)  List of Problem objects.
        3)  List of RanklistRow objects.
        contestId (Required): int. Id of the contest. It is not
                                    the round number. It can be
                                    seen in contest URL.
                                    For example: .../contest/566/status
        from_row (API: from) : int. 1-based index of the standings
                                    row to start the ranklist.
        count                : int. Number of standing rows to return.
        handles              : str or list of str. Semicolon-separated list
                                                   of handles. No more than
                                                   10000 handles is accepted.
        room                 : int. If specified, than only participants
                                    from this room will be shown in the
                                    result. If not — all the participants
                                    will be shown.
        showUnofficial       : bool. If true than all participants (virtual,
                                     out of competition) are shown.
                                     Otherwise, only official contestants
                                     are shown.
        Example: cf.contest_standings(contestId=566,
                                      from_row=1,
                                      count=5,
                                      showUnofficial=True)
        '''
        # NOTE: from is a keyword in Python.
        if isinstance(handles, str):
            handles = [handles]
        if handles is not None and len(handles) > 10000:
            raise TypeError('handles len is {}. \
                            Maximum: 10000'.format(len(handles)))
        kwargs = {
            'contestId': contestId,
            'from': from_row,
            'count': count,
            'handles': handles,
            'room': room,
            'showUnofficial': showUnofficial
        }
        self.request_api('contest.standings', **kwargs)
        return [Contest(self.last_api['result']['contest']),
                list(map(Problem, self.last_api['result']['problems'])),
                list(map(RanklistRow, self.last_api['result']['rows']))]

    def contest_status(self, contestId: int, handle: str = None,
                       from_sub: int = None, count: int = None):
        '''
        Codeforces API name: contest.status
        Returns submissions as list of Submission for specified contest.
        Optionally can return submissions of specified user.
        contestId (Required) : int. Id of the contest. It is not the
                                    round number. It can be seen in
                                    contest URL.
                                    For example: .../contest/566/status
        handle               : str. Codeforces user handle.
        from_sub (API: from) : int. 1-based index of the first submission
                                    to return.
        count                : int. Number of returned submissions.
        Example: cf.contest_status(contestId=566, from_sub=1, count=10)
        '''
        # NOTE: from is a keyword in Python.
        kwargs = {
            'contestId': contestId,
            'handle': handle,
            'from': from_sub,
            'count': count
        }
        self.request_api('contest.status', **kwargs)
        return list(map(Submission, self.last_api['result']))

    def problemset_problems(self, tags: list = None, problemsetName: str = None):
        '''
        Codeforces API name: problemset.problems.
        Returns all problems from problemset as list of two lists:
        1)  List of Problem objects.
        2)  List of ProblemStatistics objests.
        Problems can be filtered by tags.
        tags           : list of str. Semicilon-separated list of tags.
        problemsetName : str. Custom problemset's short name, like 'acmsguru'
        Example: cf.problemset_problems(tags=['implementation'])
        '''

        self.request_api('problemset.problems',
                         tags=tags,
                         problemsetName=problemsetName)
        return [list(map(Problem,
                         self.last_api['result']['problems'])),
                list(map(ProblemStatistics,
                         self.last_api['result']['problemStatistics']))]

    def problemset_recentStatus(self, count: int, problemsetName: str = None):
        '''
        Codeforces API name: problemset.recentStatus.
        Returns recent submissions as list of Submission objects.
        count (Required) : int. Number of submissions to return.
                                Can be up to 1000.
        problemsetName   : str. Custom problemset's short name,
                                like 'acmsguru'.
        Example: cf.problemset_recent_status(count=10)
        '''
        if count > 1000:
            raise TypeError('count is {}. Maximim: 1000'.format(count))
        self.request_api('problemset.recentStatus',
                         count=count,
                         problemsetName=problemsetName)
        return list(map(Submission, self.last_api['result']))

    def recentActions(self, maxCount: int):
        '''
        Codeforces API name: recentActions.
        Returns recent actions as list of RecentAction objects.
        maxCount (Required) : int. Number of recent actions to return.
                                   Can be up to 100.
        Example: cf.recentActions(maxCount=30)
        '''
        if maxCount > 100:
            raise TypeError('maxCount is {}. Maximum: 100'.format(maxCount))
        self.request_api('recentActions', maxCount=maxCount)
        return list(map(RecentAction, self.last_api['result']))

    def user_blogEntries(self, handle: str):
        '''
        Codeforces API name: user.blogEntries.
        Returns a list of all user's blog entries as list
        of BlogEntry in short form.
        handle (Required) : str. Codeforces user handle.
        Example: cf.user_blogEntries(handle='Fefer_Ivan')
        '''
        self.request_api('user.blogEntries', handle=handle)
        return list(map(BlogEntry, self.last_api['result']))

    def user_friends(self, onlyOnline: bool = False):
        '''
        Codeforces API name: user.friends.
        Returns authorized user's friends as list of str.
        Using this method requires authorization.
        onlyOnline : bool. If true - only online friends
                           are returned. Otherwise, all
                           friends are returned.
        Example: cf.user_friends(onlyOnline=True)
        '''
        self.request_api('user.friends', onlyOnline=onlyOnline)
        return self.last_api['result']

    def user_info(self, handles: int):
        '''
        Codeforces API name: user.info.
        Returns information about one or several users as
        User or list of User.
        handles (Required) : str or list of str. Semicolon-separated
                                                 list of handles. No
                                                 more than 10000 handles
                                                 is accepted.
        Examples: cf.user_info(handles='tourist')
                  cf.user_info(handles=['DmitryH', 'Fefer_Ivan'])
        '''
        if isinstance(handles, str):
            handles = [handles]
        if len(handles) > 10000:
            raise TypeError('handles len is {}. \
                             Maximum: 10000'.format(len(handles)))
        self.request_api('user.info',
                         handles=handles)
        if len(self.last_api['result']) == 1:
            return User(self.last_api['result'][0])
        else:
            return list(map(User, self.last_api['result']))

    def user_ratedList(self, active_only: bool = False):
        '''
        Codeforces API name: user.ratedList.
        Returns the list users who have participated
        in at least one rated contest as list of
        User objects.
        active_only : bool. If true then only users,
                            who participated in rated
                            contest during the last
                            month are returned. Otherwise,
                            all users with at least one
                            rated contest are returned.
        Example: cf.user_ratedList(active_only=True)
        '''
        self.request_api('user.ratedList', activeOnly=active_only)
        return list(map(User, self.last_api['result']))

    def user_rating(self, handle: str):
        '''
        Codeforces API name: user.rating.
        Returns rating history of the specified user as list
        of RatingChange objects.
        handle (Required) : str. Codeforces user handle.
        Example: cf.user_rating(handle='Fefer_Ivan')
        '''
        self.request_api('user.rating',
                         handle=handle)
        return list(map(RatingChange, self.last_api['result']))

    def user_status(self, handle: str, from_sub: int = None, count: int = None):
        '''
        Codeforces API name: user.status.
        Returns submissions of specified user as list of
        Submission objects.
        handle (Required)   : str. Codeforces user handle.
        from_sub (API: from): int. 1-based index of the first
                                   submission to return.
        count               : int. Number of returned submissions.
        Example: cf.user_status(handle='Fefer_Ivan',
                                from_sub=1,
                                count=10)
        '''
        # NOTE: from is a keyword in Python
        kwargs = {
            'handle': handle,
            'from': from_sub,
            'count': count
        }
        self.request_api('user.status', **kwargs)
        return list(map(Submission, self.last_api['result']))


class ext_CodeforcesAPI(CodeforcesAPI):
    '''
    This class provides comfortable functionality
    for in-contest and problemset submissions.
    last_verdict           : Submission. Contains last result of request to
                                         get_lastVerdict.
    last_page              : str. Contains str with HTML page from last
                                  get_page request.
    last_contestStatements : list of str. Contains HTML page with all
                                          contest results. Result of last
                                          get_contestStatements.
    '''

    def __init__(self,
                 handle: str = None,
                 workingDir: str = None,
                 **kwargs):
        '''
        Initialize the extended wrapper.
        handle     : str. Your handle from Codeforces.
        workingDir : str. Absolute path to working directory.
                          If not provided, data will be saved
                          and founded in directory with this file.
        **kwargs   : Used for initialization of CodeforcesAPI.
        '''
        CodeforcesAPI.__init__(self, **kwargs)
        self._handle = handle
        self._workingDir = workingDir

    @property
    def get_workingDir(self):
        '''
        Returns current working directory.
        '''
        if self._workingDir is None:
            return str(Path(__file__).parent.absolute())
        else:
            return self._workingDir

    def _file_save(self, file: str, path: str, name: str):
        '''
        Saves file str as <name> in working directory.
        If workingDir is not provided, data will be
        saved in directory with this file.
        '''
        try:
            makedirs(join_path(self.get_workingDir, path))
        except FileExistsError:
            pass
        with open(join_path(self.get_workingDir, path, name), 'w') as stream:
            stream.write(str(file))

    def _hack_format(self, succ: int, unsucc: int):
        '''
        Create str with hacks:
        +<succ>:-<unsucc>.
        '''
        if succ == 0:
            if unsucc == 0:
                return ''
            else:
                return '-' + str(unsucc)
        else:
            if unsucc == 0:
                return '+' + str(succ)
            else:
                return '+{}:-{}'.format(succ, unsucc)

    def _problem_format(self, problem: ProblemResult):
        '''
        Create str with problem result.
        '''
        if problem.points != 0:
            return '+{:<2} ({:02d}:{:02d})'.format(problem.rejectedAttemptCount or '',
                                                   problem.bestSubmissionTimeSeconds // 3600,
                                                   problem.bestSubmissionTimeSeconds % 3600 // 60)
        elif problem.rejectedAttemptCount != 0:
            return '-{:<2}'.format(problem.rejectedAttemptCount)
        else:
            return ''

    def _party_format(self, party: Party):
        '''
        Create string with handles of party members.
        '''
        return ', '.join(i.handle for i in party.members)

    def _problem_symb(self, num: int):
        '''
        Return symbols for problems: A, B, C...
        '''
        return [chr(ord('A') + i) for i in range(num)]

    def get_verdicts(self, handle: str, from_sub: int = 1,
                     count: int = 10, mode: str = 'fancy_grid'):
        '''
        Get the table of latest verdicts of user.
        '''
        self.last_verdict = self.user_status(
            handle=handle,
            from_sub=from_sub,
            count=count
        )

        if len(self.last_verdict):
            if self.lang == 'en':
                cols = ['#', 'When', 'Who', 'Problem',
                        'Lang', 'Verdict', 'Time', 'Memory']
            else:
                cols = ['#', 'Когда', 'Кто', 'Задача',
                        'Язык', 'Вердикт', 'Время', 'Память']
            rows = []
            for tmp in self.last_verdict:
                rows.append([tmp.id,
                             datetime.fromtimestamp(
                                 tmp.creationTimeSeconds
                             ).strftime("%d.%m.%Y %H:%M"),
                             handle,
                             tmp.problem.name,
                             tmp.programmingLanguage,
                             tmp.verdict,
                             tmp.timeConsumedMillis,
                             int(tmp.memoryConsumedBytes / 1024 + 0.5)
                            ])
            return tabulate(rows, cols, tablefmt=mode)
        else:
            return ''

    def get_lastVerdict(self, handle: str = None, mode: str = 'fancy_grid'):
        '''
        Returns result of the latest user submission and return
        table using tabulate. You can choose mode for tabulate.
        If handle is None, provided handle used.
        '''
        if handle is None:
            handle = self._handle
        return self.get_verdicts(
            handle=handle,
            from_sub=1,
            count=1,
            mode=mode
        )

    def get_page(self, link: str, **params):
        '''
        Requests and returns HTML page by link with params:
        http://codeforces.com/<link>
        '''
        params['locale'] = self.lang
        self.last_page = http_request(self._site_link + link, params=params)
        self._check_request(self.last_page)
        return self.last_page.text

    def get_contestStatements(self, contestId: int):
        '''
        Get all problem statements from contest
        by contestId in HTML format.
        '''
        self.last_contestStatements = \
            self.get_page('contest/{}/problems'.format(contestId))
        return self.last_contestStatements

    def save_contestStatements(self, contestId: int):
        '''
        Save the webpage with contest statements
        in your working directory.
        '''
        self._file_save(self.get_contestStatements(contestId),
                        join_path(
                            self.get_workingDir,
                            'statements', str(contestId)
                        ),
                        'webpage.html'
        )

    def open_contestStatements(self, contestId: int):
        '''
        Opens the contest statements. If the
        statements are not saved, they will
        be downloaded.
        '''
        filename = join_path(
            self.get_workingDir,
            'statements', str(contestId), 'webpage.html'
        )
        if not Path(filename).is_file():
            self.save_contestStatements(contestId)
        open_new_tab('file://' + filename)

    def contest_standingsTable(self, contestId: int, from_row: int = 1,
                               count: int = 100, mode: str = 'fancy_grid'):
        '''
        Get the contest standings by contestId and return table
        by tabulate. You can choose mode for tabulate.
        '''
        request = self.contest_standings(contestId=contestId,
                                         from_row=from_row,
                                         count=count)[2]
        rows, cols = list(), list()
        if self.lang == 'en':
            cols = ['#', 'Who', 'Hacks',
                    *self._problem_symb(len(request[0].problemResults)),
                    'Penalty']
        else:
            cols = ['#', 'Кто', 'Взломы',
                    *self._problem_symb(len(request[0].problemResults)),
                    'Пенальти']
        for i in request:
            rows.append([i.rank,
                         self._party_format(i.party),
                         self._hack_format(i.successfulHackCount,
                                           i.unsuccessfulHackCount),
                         *(self._problem_format(i.problemResults[j])
                           for j in range(len(i.problemResults))),
                         i.penalty])
        return tabulate(rows, cols, tablefmt=mode)
