from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer
from reviews.models import Review

__all__ = ('ReviewDocument',)

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES['search_indexes.documents.review'])


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
class ReviewDocument(Document):
    id = fields.IntegerField(attr='id')
    title = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    description = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.KeywordField(),
            'suggest': fields.CompletionField(),
        }
    )

    rating = fields.FloatField()

    created_date = fields.DateField()

    author = fields.ObjectField(
        properties={
            'id': fields.IntegerField(
                fields={
                    'raw': fields.KeywordField()
                }
            ),
            'name': fields.TextField(
                attr='name_indexing',
                analyzer=html_strip,
                fields={
                    'raw': fields.KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            )
        }
    )

    profile = fields.ObjectField(
        properties={
            'id': fields.IntegerField(
                fields={
                    'raw': fields.KeywordField()
                }
            )
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
    #     elif isinstance(related_instance, Review):
    #         return related_instance.review

    class Django(object):
        """Inner nested class Django."""
        model = Review  # The model associate with this Document
