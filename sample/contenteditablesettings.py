""" Defines Models that are allowed to be edited using contenteditable """

from newspaper.models import Article

CONTENTEDITABLE_MODELS = {
    'article': [Article, ['title', 'text']],
}

