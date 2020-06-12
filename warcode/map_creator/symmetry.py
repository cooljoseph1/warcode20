class _Symmetry:
    def apply(self, x, y, width, height):
        raise NotImplementedError

class _Horizontal:
    def apply(self, x, y, width, height):
        return (x, height - y - 1)

class _Vertical:
    def apply(self, x, y, width, height):
        return (width - x - 1, y)

class _UR_Diagonal:
    def apply(self, x, y, width, height):
        return (height - y - 1, width - x - 1)

class _DR_Diagonal:
    def apply(self, x, y, width, height):
        return (y, x)

class _Radial:
    def apply(self, x, y, width, height):
        return (width - x - 1, height - y - 1)

class Symmetry:
    HORIZONTAL = _Horizontal()
    VERTICAL = _Vertical()
    UR_DIAGONAL = _UR_Diagonal()
    DR_DIAGONAL = _DR_Diagonal()
    RADIAL = _Radial()

    _name_to_symmetry = {
        "Horizontal": HORIZONTAL,
        "Vertical": VERTICAL,
        "UR Diagonal": UR_DIAGONAL,
        "DR Diagonal": DR_DIAGONAL,
        "Radial": RADIAL,
    }

    @classmethod
    def from_string(cls, name):
        return cls._name_to_symmetry[name]
