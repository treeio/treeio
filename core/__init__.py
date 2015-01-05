# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

import codecs
import cStringIO as StringIO

def utf8(s):
    """
    Convert a string (UNICODE or ANSI) to a utf8 string.

    @param s String.
    @return UTF8 string.
    """
    info = codecs.lookup('utf8')
    try:
        out = StringIO.StringIO()
        srw = codecs.StreamReaderWriter(out,
                info.streamreader, info.streamwriter, 'strict')
        srw.write(s)
        return out.getvalue()
    except UnicodeError:
        # Try again by forcing convert to unicode type first.
        srw.write(_unicode(s, strict=True))
        return out.getvalue()
    finally:
        srw.close()
        out.close()

import locale

def _unicode(s, strict=False, encodings=None, throw=True):
    """
    Force to UNICODE string (UNICODE type or string type with utf8 content).

    @param s String.
    @param strict If strict is True, we always return UNICODE type string, this
                  means it will ignore to try convert it to utf8 string.
    @param encodings Native encodings for decode. It will be tried to decode
                     string, try and error.
    @param throw Raise exception if it fails to convert string.
    @return UNICODE type string or utf8 string.
    """
    try:
        if isinstance(s, unicode):
            if strict:
                return s
            else:
                return utf8(s)
        else:
            return unicode(s, 'utf8')
    except: # For UNICODE, cp950...
        try:
            return unicode(s)
        except:
            if not encodings:
                encodings = (locale.getpreferredencoding(),)

            for encoding in encodings:
                try:
                    return unicode(s, encoding)
                except:
                    pass
            else:
                if strict:
                    if throw:
                        raise
                    else:
                        return u''
                else:
                    try:
                        return str(s)
                    except:
                        if throw:
                            raise
                        else:
                            return u''
