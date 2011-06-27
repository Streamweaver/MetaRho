import xmlrpclib

LJ_API_URL = "http://www.livejournal.com/interface/xmlrpc"
LJ_TIME_FORMAT = r"%Y-%m-%d %H:%M:%S"

class LJTarget:
    """Interacts with LiveJournal via the XML-RPC API.  This is an experimental PROTOTYPE"""
    user_agent = "metarho xpost"
    clientversion = "0.1-dev"

    def _get_auth_challenge(self):

    def _get_headers(self):
        headers = {

        }
        return headers

    def create_event(self, post, privacy='private'):
        """Sends a post to the API as a new item."""

