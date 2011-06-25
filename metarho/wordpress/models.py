from django.db import models

from metarho.blog.models import Post

class WPMapping (models.Model):
    """
    Provides a simple relational table mapping between wordpress IDs for posts imported from wordpress.
    """
    post = models.OneToOneField(Post)
    wp_id = models.PositiveIntegerField(help_text="Wordpress post ID")

    def __str__(self):
        return "%s (p=%s)" % (self.post.title, self.wp_id)

    def __unicode__(self):
        return u"%s" % self.__str__()
