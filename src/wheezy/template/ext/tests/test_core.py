
""" Unit tests for ``wheezy.templates.ext.core``.
"""

import unittest


class CleanSourceTestCase(unittest.TestCase):
    """ Test the ``clean_source``.
    """

    def test_new_line(self):
        """ Replace windows new line with linux new line.
        """
        from wheezy.template.ext.core import clean_source
        assert 'a\nb' == clean_source('a\r\nb')

    def test_leading_whitespace(self):
        """ Remove leading whitespace before @ symbol.
        """
        from wheezy.template.ext.core import clean_source
        assert 'a\n@b' == clean_source('a\n  @b')
        assert '@b' == clean_source('  @b')

    def test_ignore(self):
        """ Ignore double @.
        """
        from wheezy.template.ext.core import clean_source
        assert 'a\n  @@b' == clean_source('a\n  @@b')
        assert '  @@b' == clean_source('  @@b')


class LexerTestCase(unittest.TestCase):
    """ Test the ``CoreExtension``.
    """

    def setUp(self):
        from wheezy.template.engine import Engine
        from wheezy.template.ext.core import CoreExtension
        self.engine = Engine(extensions=[CoreExtension()])
        self.lexer = self.engine.lexer

    def test_stmt_token(self):
        """ Test statement token.
        """
        tokens = self.lexer.tokenize('@require(title, users)\n')
        assert (1, 'require', 'require(title, users)') == tokens[0]

    def test_var_token(self):
        """ Test variable token.
        """
        tokens = self.lexer.tokenize('@user.name ')
        assert (1, 'var', 'user.name') == tokens[0]
        tokens = self.lexer.tokenize('@user.pref[i].fmt() ')
        assert (1, 'var', 'user.pref[i].fmt()') == tokens[0]

    def test_markup_token(self):
        """ Test markup token.
        """
        tokens = self.lexer.tokenize(' test ')
        assert 1 == len(tokens)
        assert (1, 'markup', ' test ') == tokens[0]

    def test_markup_token_escape(self):
        """ Test markup token with escape.
        """
        tokens = self.lexer.tokenize('support@@acme.org')
        assert 1 == len(tokens)
        assert (1, 'markup', 'support@acme.org') == tokens[0]
