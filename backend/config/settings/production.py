from .base import *
import os

print("###################################################################################")
print("########              Started with Production Settings        #####################")
print("###################################################################################")

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
)