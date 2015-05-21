# Std libs
import time

# 3rd party libs
import instagram
from instagram import InstagramAPI

# User defined libs
from db import DB


################################################################################
class InstaBot(object):
    """
    Bot that uses Instagrams API
    (Not really a bot then is it huh)
    """
    MINUTE = 60
    HOUR = 60 * MINUTE
    FIVE_MINUTE = MINUTE * 5
    INFO = 0
    WARNING = 1
    ERROR = 2

    # --------------------------------------------------------------------------
    def __init__(self, token, ip, secret, tag_list, log=None, pause=None):
        """
        :param token: Access_token of account
        :param ip: Machines IP
        :param secret: Client secret
        :param tag_list: List of hastags to interact with
        :param log: Where to save info. Default "instabot.log"
        :param pause: Time to wait before interacting again. Default 1 second"
        """
        super(InstaBot, self).__init__()
        self.api = InstagramAPI(access_token=token, client_ips=ip,
                                client_secret=secret)
        self.tag_list = tag_list
        self.log = "instabot.log" if log is None else log
        self.pause = 1 if pause is None else pause
        self.db = DB()

        self.__count = 0
        self.__keep_going = True

    # --------------------------------------------------------------------------
    def __recordGeneral(self, *args):
        _list = ["Hashtag", "Num of likes", "Date"]
        with open(self.log, "a") as log:
            for index, item in enumerate(_list):
                log.write("{}: {}\n".format(_list[index], args[index]))
            log.write("\n\n\n")

    # --------------------------------------------------------------------------
    def __record(self, msg, lvl=0):
        """ Record stuff to log """
        lvl_list = ["INFO", "WARNING", "ERROR"]
        with open(self.log, "a") as log:
            log.write("##[{}]##: {}\n".format(lvl_list[lvl], msg))

    # --------------------------------------------------------------------------
    def start(self):
        """ Start the bot """
        # reset to true incase it was false
        self.__keep_going = True

        while self.__keep_going:
            try:
                self._likePics()
            except instagram.bind.InstagramAPIError as e:
                self.__record(e, self.INFO)
                time.sleep(self.HOUR + self.FIVE_MINUTE)
            except Exception as e:
                self.__record(e, self.ERROR)
                time.sleep(5)
            finally:
                # Just increment count variable
                self.__count += 1

    # --------------------------------------------------------------------------
    def stop(self):
        """ Stop the bot """
        self.__keep_going = False

    # --------------------------------------------------------------------------
    def _likePics(self):
        # TODO: If we iterate over everything, it doesn't record it. Only
        # records exceptions that we finished out limites. Not right.
        tag = self.tag_list[self.__count % len(self.tag_list)]
        recent_media, url = self.api.tag_recent_media(tag_name=tag, count=1500)
        num_likes = 0
        # iterate over the stuff
        for media in recent_media:
            _id = media.id
            # if we have not liked it, then do it
            if not self.db.isKeyInDB(_id):
                try:
                    self.api.like_media(media_id=_id)
                    num_likes += 1
                    self.db.insertValues(_id, media.get_thumbnail_url(),
                                         media.get_low_resolution_url(),
                                         media.get_standard_resolution_url())
                except instagram.bind.InstagramAPIError as e:
                    self.__recordGeneral(tag, num_likes, getTime())
                    raise e
            time.sleep(self.pause)


# ------------------------------------------------------------------------------
def getTime():
    _time = time.strftime("%I:%M:%S")
    _date = time.strftime("%m/%d/%Y")
    return "{} - {}".format(_date, _time)


if __name__ == "__main__":
    from creds import token, ip, secret
    # Pass in your own credentials
    instabot = InstaBot(token=token, ip=ip, secret=secret,
                        tag_list=["computerjoke"])
    instabot.start()
