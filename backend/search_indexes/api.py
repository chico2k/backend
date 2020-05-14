from rest_framework.views import APIView
from main.management.rest_framework.utils import ExceptionHandlerMixin
from rest_framework.response import Response
from rest_framework.parsers import BaseParser, JSONParser
import requests
import json
from rest_framework import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from elasticsearch_dsl import MultiSearch, Search

from elasticsearch_dsl import connections

from elasticsearch_dsl import MultiSearch, Search
from config.settings.local import es
from elasticsearch import Elasticsearch

class ndjsonParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'application/x-ndjson'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.getvalue()


class ElasticSearchMultiAPI(ExceptionHandlerMixin, APIView):
    """
    ElasticSearchAPI Multi Search Proxy
    """
    parser_classes = [ndjsonParser, ]

    def post(self, request, index):
        query = request.data.decode("utf-8")
        res = es.msearch(index=index, body=query)
        return Response(res)

class ElasticSearchSingleAPI(ExceptionHandlerMixin, APIView):
    """
    ElasticSearchAPI Single Search Proxy
    """
    parser_classes = [JSONParser, ]

    def post(self, request, index):
        query = request.data
        res = es.search(index=index, body=query)
        return Response(res)
