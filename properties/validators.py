from django.utils.translation import gettext as _

APARTMENT = 'APT'
HOUSE = 'HOU'
LAND = 'LAN'
COMMERCIAL = 'COM'
FARM = 'FAR'

NEW = 'NEW'
OFFPLAN = 'PLA'
STARTED = 'STA'
USED = 'USE'

SALE = 'SALE'
RENT = 'RENT'
TRENT = 'TEMR'
SWAP = 'SWAP'

TIPO_PRO = [
    (APARTMENT, _('Apartment')),
    (HOUSE, _('House')),
    (LAND, _('Land')),
    (FARM, _('Farm')),
    (COMMERCIAL, _('Commercial')),
]

STATUS_PRO = [
    (NEW, _('New')),
    (OFFPLAN, _('Off-plans')),
    (STARTED, _('On construction')),
    (USED, _('Used')),
]

TIPO_BUS = [
    (SALE, _('Sale')),
    (RENT, _('Rent')),
    (TRENT, _('Temporal Rent')),
    (SWAP, _('Swap')),
]