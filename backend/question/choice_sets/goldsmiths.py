from django.utils.translation import gettext_lazy as _

GMSI_YEARS_PRACTICED = {
    '0': _('0 years'),
    '1': _('1 year'),
    '2': _('2 years'),
    '3': _('3 years'),
    '4-5': _('4–5 years'),
    '6-9': _('6–9 years'),
    '10+': _('10 or more years'),
}

GMSI_HOURS_DAILY_PRACTICE = {
    '0': _('0 hours'),
    '0.5': _('0.5 hours'),
    '1': _('1 hour'),
    '1.5': _('1.5 hours'),
    '2': _('2 hours'),
    '3-4': _('3-4 hours'),
    '5+': _('5 or more hours'),
}

GMSI_N_INSTRUMENTS = {
    '0': _('0'),
    '1': _('1'),
    '2': _('2'),
    '3': _('3'),
    '4': _('4'),
    '5': _('5'),
    '6+': _('6 or more'),
}

GMSI_ATTENDED_EVENTS = {
    # use floats as key, to prevent int conversions while dumping json
    '0.0': _('0'),
    '1.0': _('1'),
    '2.0': _('2'),
    '3.0': _('3'),
    '4-6': _('4-6'),
    '7-10': _('7-10'),
    '11+': _('11 or more'),
}

GMSI_DAILY_MUSIC_LISTENING = {
    '0-15': _('0-15 min'),
    '15-30': _('15-30 min'),
    '30-60': _('30-60 min'),
    '60-90': _('60-90 min'),
    '2h': _('2 hrs'),
    '2-3h': _('2-3 hrs'),
    '4h+': _('4 hrs or more'),
}

GMSI_YEARS_THEORY_TRAINING ={
    '0': _('0'),
    '0.5': _('0.5'),
    '1': _('1'),
    '2': _('2'),
    '3': _('3'),
    '4-6': _('4-6'),
    '7+': _('7 or more'),
}

GMSI_YEARS_INSTRUMENTAL_TRAINING = {
    '0': _('0'),
    '0.5': _('0.5'),
    '1': _('1'),
    '2': _('2'),
    '3-5': _('3-5'),
    '6-9': _('6-9'),
    '10+': _('10 or more'),
}
