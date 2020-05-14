from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from profiles.models import Profile

__all__ = ('ProfileDocument',)

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])


# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@INDEX.doc_type
class ProfileDocument(Document):
    id = fields.IntegerField(attr='id')
    name = fields.TextField(
        attr='name_indexing',
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )
    is_guide = fields.TextField(
        attr='is_guide_indexing',
        fields={
            'suggest': fields.CompletionField(),
            'raw': fields.KeywordField()
        }, )
    sport = fields.ObjectField(
        properties={
            'id': fields.IntegerField(
                fields={
                    'raw': fields.KeywordField()
                }
            ),
            'level': fields.IntegerField(
                fields={
                    'raw': fields.KeywordField()
                }
            ),
            'sporttype': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(
                        fields={
                            'raw': fields.KeywordField()
                        },
                    ),
                    'title': fields.TextField(
                        fields={
                            'raw': fields.KeywordField()
                        },)
                }
            ),
        }
    )

    number_rating = fields.IntegerField(attr='number_rating')

    average_rating = fields.FloatField()

    location = fields.ObjectField(
        properties={
            'coordinates': fields.GeoPointField(attr="location_field_indexing"),
            'place_name': fields.TextField(
                fields={
                    'raw': fields.KeywordField()
                },),
            'text': fields.TextField(
                fields={
                    'raw': fields.KeywordField()
                },)
        }
    )

    # def get_instances_from_related(self, related_instance):
    #     """If related_models is set, define how to retrieve the Car instance(s) from the related model.
    #     The related_models option should be used with caution because it can lead in the index
    #     to the updating of a lot of items.
    #     """
    #     if isinstance(related_instance, User):
    #         return related_instance.profile.all()
    #     elif isinstance(related_instance, Sport):
    #         return related_instance.profile

    class Django(object):
        """Inner nested class Django."""

        model = Profile  # The model associate with this Document
