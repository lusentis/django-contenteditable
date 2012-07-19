""" Defines Models that are allowed to be edited using contenteditable """

from newspaper.models import Article
from chunks.models import Chunk

CONTENTEDITABLE_MODELS = {
    'article': (Article, ('title', 'text')),
    'chunk': (Chunk, ('content',)),
}
