import httplib2
import json

from metarho import settings

# Just a series of classes to play around with Open Calais for entity recognition and tag suggestion.

CALAIS_API_URL = 'http://api.opencalais.com/tag/rs/enrich'

class CalaisSocialTag:
    def __init__(self, ctag):
        """Class to handle Open Calais Social Tag Suggestions"""
        self.ctag = ctag
        self.group = ctag["_typeGroup"]
        self.id = ctag["id"]
        self.importance = ctag["importance"]
        self.name = ctag["name"]
        self.socialtag = ctag["socialTag"]

    def __str__(self):
        return "%s" % self.name

class CalaisEntity:
    def __init__(self, ctag):
        """Class to handle Open Calis entity suggestions."""
        self.ctag = ctag
        self.type = ctag["_type"]
        self.group = ctag["_typeGroup"]
        self.reference = ctag["_typeReference"]
        self.name = ctag["name"]
        self.relevance = ctag["relevance"]
        self.instances = self._instances()
        self.resolutions = self._resolutions()

    def _instances(self):
        if "instances" not in self.ctag.keys():
            return None
        return self.ctag["instances"]

    def _resolutions(self):
        if "resolutions" not in self.ctag.keys():
            return None
        return self.ctag["resolutions"]

    def __str__(self):
        s = "%s (%s) %d instances" % (self.name, self.group, len(self.instances))
        return "%s" % self.name

class CalaisTopic:
    def __init__(self, ctag):
        """Class to hangle Open Calais topic suggestions."""
        self.ctag = ctag
        self.group = ctag["_typeGroup"]
        self.name = ctag["categoryName"]
        self.category = ctag["category"]
        self.score = ctag["score"]

    def __str__(self):
        return "%s" % self.name

class CalaisSuggest:
    def __init__(self, content, type='text/html', socialtags=True):
        """
        A class that handles connecting to the Open Calais API with content and returning the
        results.

        :param content: The content to be analyzed by the API.
        :param type: Content type being sent, standard html header content-type values
        :param socialtags: Enable socialTags mediaType in the Open Calais Return
        
        """
        self.content = content
        self.headers = self._set_headers(type, socialtags)
        self.entities = []
        self.topics = []
        self.tags = []
        self._query()

    def _set_headers(self, ctype, socialtags):
        headers = {
            'x-calais-licenseID': settings.CALAIS_API_KEY,
            'content-type':  ctype,
            'accept': 'application/json',
        }
        if socialtags:
            headers["enableMetadataType"] = 'SocialTags'
        return headers

    def _query(self):
        """Query the Open Calais API if we have any content"""
        if not self.content:
            return None

        # Make the API call and return the results
        http = httplib2.Http()
        reponse, results = http.request(CALAIS_API_URL, 'POST', headers=self.headers, body=self.content)

        data = json.loads(results)
        del data["doc"] # Throw this away to parse more cleanly

        ctags = [item[1] for item in data.items()]
        self.ctags = ctags

        for ctag in ctags:
            if ctag["_typeGroup"] == 'socialTag':
                self.tags.append(CalaisSocialTag(ctag))
            if ctag["_typeGroup"] == 'entities':
                self.entities.append(CalaisEntity(ctag))
            if ctag["_typeGroup"] == 'topics':
                self.topics.append(CalaisTopic(ctag))



