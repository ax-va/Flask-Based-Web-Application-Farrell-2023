from random import sample
from typing import List


class BannerColors:
    """ Chooses randomly 5 colors from the colors that are CSS-valid and available in the class """
    COLORS = [
        'aqua',
        'blue',
        'darkcyan',
        'darkkhaki',
        'firebrick',
        'gold',
        'gray',
        'green',
        'greenyellow',
        'indigo',
        'khaki',
        'lightcoral',
        'lime',
        'olive',
        'pink',
        'purple',
        'red',
        'salmon',
        'sienna',
        'silver',
        'skyblue',
        'tan',
        'violet',
        'yellow',
    ]

    @staticmethod
    def get_colors() -> List[str]:
        """ Returns randomly 5 colors """
        return sample(BannerColors.COLORS, 5)
