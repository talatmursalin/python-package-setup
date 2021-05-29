from pkgcli.utils.unicode import utf8text


class SpecificationError(Exception):
    def __init__(self, msg):
        super(SpecificationError, self).__init__(utf8text(msg))
