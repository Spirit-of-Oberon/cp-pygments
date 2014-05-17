class ComponentPascalLexer(RegexLexer):
    """
    For `Component Pascal <http://www.oberon.ch/pdf/CP-Lang.pdf>`_ source code.

    .. versionadded:: 0.1
    """
    name = 'Component Pascal'
    aliases = ['ComponentPascal', 'CP']
    filenames = ['*.cp', '*.cps']
    mimetypes = ['text/x-component-pascal']

    flags = re.MULTILINE | re.DOTALL

    tokens = {
        'whitespace': [
            (r'\n+', Text), # blank lines
            (r'\s+', Text), # whitespace
        ],
        'identifiers': [
            (r'([a-zA-Z_\$][\w\$]*)', Name),
        ],
        'numliterals': [
            (r'[0-9A-F]+X', Number.Hex),                  # char code
            (r'[0-9A-F]+[HL]', Number.Hex),               # hexadecimal number
            (r'[0-9]+\.[0-9]+E[+-][0-9]+', Number.Float), # real number
            (r'[0-9]+\.[0-9]+', Number.Float),            # real number
            (r'[0-9]+', Number.Integer),                  # decimal whole number
        ],
        'strings': [
            (r"'(\\\\|\\'|[^'])*'", String), # single quoted string
            (r'"(\\\\|\\"|[^"])*"', String), # double quoted string
        ],
        'operators': [
            (r'[*/+=#~&<>\^-]', Operator),
            (r':=', Operator),   # assignment
            (r'^', Operator),    # pointer deref
            (r'\.\.', Operator), # ellipsis or range
        ],
        'punctuation': [
            (r'[\(\)\[\]{},.:;|]', Punctuation),
        ],
        'comments': [
            (r'\(\*([^\$].*?)\*\)', Comment.Multiline),
            # TO DO: nesting of (* ... *) comments
        ],
        'pragmas': [
            # ???
        ],
        'root': [
            include('whitespace'),
            include('comments'),
            include('pragmas'),
            include('identifiers'),
            include('numliterals'),
            include('strings'),
            include('operators'),
            include('punctuation'),
        ]
    }

    cp_reserved_words = [
        # 36 reserved words
        'ABSTRACT', 'ARRAY', 'BEGIN', 'BY', 'CASE', 'CLOSE', 'CONST', 'DIV',
        'DO', 'ELSE', 'ELSIF', 'EMPTY', 'END', 'EXIT', 'EXTENSIBLE', 'FOR',
        'IF', 'IMPORT', 'IN', 'IS', 'LIMITED', 'LOOP', 'MOD', 'MODULE', 'NIL',
        'OF', 'OR', 'OUT', 'POINTER', 'PROCEDURE', 'RECORD', 'REPEAT', 'RETURN',
        'THEN', 'TO', 'TYPE', 'UNTIL', 'VAR', 'WHILE', 'WITH'
    ]

    cp_pervasives = [
        # 36 pervasives
        'ABS', 'ANYPTR', 'ANYREC', 'ASH', 'ASSERT', 'BITS', 'BOOLEAN', 'BYTE',
        'CAP', 'CHAR', 'CHR', 'DEC', 'ENTIER', 'EXCL', 'HALT', 'INC', 'INCL',
        'INF', 'INTEGER', 'FALSE', 'LEN', 'LONG', 'LONGINT', 'MAX', 'MIN',
        'NEW', 'ODD', 'ORD', 'REAL', 'SET', 'SHORT', 'SHORTCHAR', 'SHORTINT',
        'SHORTREAL', 'SIZE', 'TRUE'
    ]

    def __init__(self, **options):
        self.reserved_words = set()
        self.pervasives = set()
        self.reserved_words.update(self.cp_reserved_words)
        self.pervasives.update(self.cp_pervasives)
        # initialise
        RegexLexer.__init__(self, **options)

    def get_tokens_unprocessed(self, text):
        for index, token, value in \
            RegexLexer.get_tokens_unprocessed(self, text):
            # check for reserved words and pervasives
            if token is Name:
                if value in self.reserved_words:
                    token = Keyword.Reserved
                elif value in self.pervasives:
                    token = Keyword.Pervasive
            # return result
            yield index, token, value
