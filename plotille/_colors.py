# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

# The MIT License

# Copyright (c) 2017 Tammo Ippen, tammo.ippen@posteo.de

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import six


def color(text, fg=None, bg=None, kind='names'):
    '''Surround `text` with control characters for coloring

    c.f. http://en.wikipedia.org/wiki/ANSI_escape_code

    There are 3 color modes enabled:
        - `names`:  corresponds to 3/4 bit encoding; provide colors as lower case
                    with underscore names, e.g. 'red', 'bright_green'
        - `byte`: corresponds to 8-bit encoding; provide colors as int \in [0, 255];
                  compare 256-color lookup table
        - `rgb`: corresponds to 24-bit encoding; provide colors either in 3- or 6-character
                 hex encoding or provide as a list / tuple with three ints (\in [0, 255] each)

    Parameters:
        text: str        Some text to surround.
        fg: multiple     Specify the foreground / text color.
        bg: multiple     Specify the background color.
        color_kind: str  Specify color input mode; 'names'(default), 'byte' or 'rgb'

    Returns:
        str: `text` enclosed with corresponding coloring controls
    '''
    start = ''
    if kind == 'names':
        start = _names(fg, bg)
    elif kind == 'byte':
        start = _byte(fg, bg)
    elif kind == 'rgb':
        if isinstance(fg, six.string_types):
            fg = _hex2rgb(fg)
        if isinstance(bg, six.string_types):
            bg = _hex2rgb(bg)

        start = _rgb(fg, bg)
    else:
        raise ValueError('Invalid kind "{}". Use one of "names", "byte" or "rgb".'.format(kind))

    if start:
        return start + text + '\x1b[0m'
    return text


def _names(fg, bg):
    '''3/4 bit encoding part

    c.f. https://en.wikipedia.org/wiki/ANSI_escape_code#3.2F4_bit

    Parameters:

    '''
    if not (fg is None or fg in _FOREGROUNDS):
        raise ValueError('Invalid color name fg = "{}"'.format(fg))
    if not (bg is None or bg in _BACKGROUNDS):
        raise ValueError('Invalid color name bg = "{}"'.format(bg))

    fg_ = _FOREGROUNDS.get(fg, '')
    bg_ = _BACKGROUNDS.get(bg, '')

    return _join_codes(fg_, bg_)


def _byte(fg, bg):
    '''8-bite encoding part

    c.f. https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
    '''
    if not (fg is None or (isinstance(fg, int) and 0 <= fg <= 255)):
        raise ValueError('Invalid fg = {}. Allowed int in [0, 255].'.format(fg))
    if not (bg is None or (isinstance(bg, int) and 0 <= bg <= 255)):
        raise ValueError('Invalid bg = {}. Allowed int in [0, 255].'.format(bg))

    fg_ = ''
    if fg is not None:
        fg_ = '38;5;' + six.text_type(fg)
    bg_ = ''
    if bg is not None:
        bg_ = '48;5;' + six.text_type(bg)

    return _join_codes(fg_, bg_)


def _hex2rgb(h):
    '''Transform rgb hex representation into rgb tuple of ints representation'''
    assert isinstance(h, six.string_types)
    if h.lower().startswith('0x'):
        h = h[2:]
    if len(h) == 3:
        return (int(h[0]*2, base=16), int(h[1]*2, base=16), int(h[2]*2, base=16))
    if len(h) == 6:
        return (int(h[0:2], base=16), int(h[2:4], base=16), int(h[4:6], base=16))

    raise ValueError('Invalid hex RGB value.')


def _rgb(fg, bg):
    '''24-bit encoding part

    c.f. https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
    '''
    assert fg is None or (isinstance(fg, (list, tuple)) and len(fg) == 3)
    assert bg is None or (isinstance(bg, (list, tuple)) and len(bg) == 3)
    fg_ = ''
    if fg is not None:
        fg_ = '38;2;' + ';'.join(map(six.text_type, fg))
    bg_ = ''
    if bg is not None:
        bg_ = '48;2;' + ';'.join(map(six.text_type, bg))

    return _join_codes(fg_, bg_)


def _join_codes(fg, bg):
    '''Join `fg` and `bg` with ; and surround with correct esc sequence.'''
    colors = ';'.join(filter(lambda c: len(c) > 0, (fg, bg)))
    if colors:
        return '\x1b[' + colors + 'm'

    return ''


_BACKGROUNDS = dict(
    black='40',
    red='41',
    green='42',
    yellow='43',
    blue='44',
    magenta='45',
    cyan='46',
    white='47',
    bright_black='100',
    bright_red='101',
    bright_green='102',
    bright_yellow='103',
    bright_blue='104',
    bright_magenta='105',
    bright_cyan='106',
    bright_white='107',
)

_FOREGROUNDS = dict(
    black='30',
    red='31',
    green='32',
    yellow='33',
    blue='34',
    magenta='35',
    cyan='36',
    white='37',
    bright_black='1;30',
    bright_red='1;31',
    bright_green='1;32',
    bright_yellow='1;33',
    bright_blue='1;34',
    bright_magenta='1;35',
    bright_cyan='1;36',
    bright_white='1;37',
)
