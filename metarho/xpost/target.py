import xmlrpclib, hashlib

from tagging.models import Tag

from metarho import settings

class LJError(xmlrpclib.Error):
    pass

class LJxmlrpc:
    """
    Interacts with LiveJournal via the XML-RPC API.  This is an experimental PROTOTYPE.
    
    General LJ feature documentation http://www.livejournal.com/doc/server/ljp.csp.xml-rpc.protocol.html
    """
    API_URL = "http://www.livejournal.com/interface/xmlrpc"
    TIME_FORMAT = r"%Y-%m-%d %H:%M:%S"

    user_agent = "metarho xpost"
    clientversion = "0.1-dev"

    def __init__(self):
        self.transport = xmlrpclib.Transport()
        self.server = xmlrpclib.ServerProxy(self.API_URL, self.transport)
        self.api = self.server.LJ.XMLRPC
        self.ljuser = settings.LJ_USERNAME
        self.ljpasshex = hashlib.md5(settings.LJ_PASSWORD).hexdigest()

    def _get_auth_challenge(self):
        """
        Returns the auth challenge dict from the LJ server.
        Documentation of return at http://www.livejournal.com/doc/server/ljp.csp.auth.challresp.html
        ."""
        return self.api.getchallenge()

    def _init_data(self):
        """
        Creates and returns some header values for a request.
        """
        ljauth = self._get_auth_challenge()

        args = {
            'clientversion': self.clientversion,
            'auth_method': 'challenge',
            'auth_challenge': ljauth['challenge'],
            'username': self.ljuser,
            'auth_response': hashlib.md5(ljauth['challenge'] + self.ljpasshex).hexdigest()
        }
        return args

    def create_or_update(self, post, privacy='private'):
        """
        Sends a post to the API to create or update it as appropriate.
        postevent - http://www.livejournal.com/doc/server/ljp.csp.xml-rpc.postevent.html
        editevent - http://www.livejournal.com/doc/server/ljp.csp.xml-rpc.editevent.html
        """

        data = self._init_data()

        # @NOTE use private security for testing so I don't spam folks.
        data['security'] = privacy # Can be public, private.  Friends security more complex.
        
        # Set Post Date Information
        data['year'] = post.pub_date.year
        data['mon'] = post.pub_date.month
        data['day'] = post.pub_date.day
        data['hour'] = post.pub_date.hour
        data['min'] = post.pub_date.minute
        
        # Finnally set post information.
        data['subject'] = post.title
        data['event'] = post.content
        tags = [tag.name for tag in Tag.objects.get_for_object(post)]
        data['props'] = {'taglist': ", ".join(tags)}

        lj_itemid = post.postmeta_set.filter(key='lj_itemid')

        if lj_itemid: # If an LJ item for this already exists update it.
            data['itemid'] = lj_itemid[0].value
            return self.api.editevent(data)

        # If no lj_itemid treat it as a new post, post it and set the lj_itemid and lj_permalink
        # in post meta

        # {'itemid': 3066, 'url': 'http://streamweaver.livejournal.com/785033.html', 'anum': 137}
        response = self.api.postevent(data)
        post.postmeta_set.create(
            key = 'lj_itemid',
            value = response['itemid'],
        )
        post.postmeta_set.create(
            key = 'lj_permalink',
            value = response['url'],
        )
        return response
