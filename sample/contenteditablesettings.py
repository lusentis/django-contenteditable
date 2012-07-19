""" Defines Models that are allowed to be edited using contenteditable """

CONTENTEDITABLE_MODELS = (
    ('newspaper.article', ('title', 'text')),
    ('chunks.chunk', ('content',)),
)
