from django.utils.translation import gettext_lazy as _

from experiment.actions.question import DropdownQuestion, RadiosQuestion, TextQuestion

region_choices = {
    'HD': '华东（山东、江苏、安徽、浙江、福建、江西、上海）',
    'HN': '华南（广东、广西、海南）',
    'HZ': '华中（湖北、湖南、河南、江西）',
    'HB': '华北（北京、天津、河北、山西、内蒙古）',
    'XB': '西北（宁夏、新疆、青海、陕西、甘肃）',
    'XN': '西南（四川、云南、贵州、西藏、重庆）',
    'DB': '东北（辽宁、吉林、黑龙江）',
    'GAT': '港澳台（香港、澳门、台湾）',
    'QT': '国外',
    'no_answer': '不想回答'
}

OTHER = [
    DropdownQuestion(
        key='dgf_region_of_origin',
        text=_(
            "In which region did you spend the most formative years of your childhood and youth?"
        ),
        choices=region_choices,
    ),
    DropdownQuestion(
        key='dgf_region_of_residence',
        text=_("In which region do you currently reside?"),
        choices=region_choices,
    ),
    RadiosQuestion(
        key='dgf_gender_identity_zh',
        text="您目前对自己的性别认识?",
        choices={
            'male': "男",
            'Female': "女",
            'Others': "其他",
            'no_answer': "不想回答",
        },
    ),
    DropdownQuestion(
        key='dgf_genre_preference_zh',
        text=_("To which group of musical genres do you currently listen most?"),
        choices={
            'unpretentious': _("Pop/Country/Religious"),
            'Chinese artistic': _("Folk/Mountain songs"),
            'sophisticated': _("Western classical music/Jazz/Opera/Musical"),
            'classical': _("Chinese opera"),
            'intense': _("Rock/Punk/Metal"),
            'mellow': _("Dance/Electronic/New Age"),
            'contemporary': _("Hip-hop/R&B/Funk"),
        },
    ),
    TextQuestion(
        key='contact',
        explainer=_(
            "Thank you so much for your feedback! Feel free to include your contact information if you would like a reply or skip if you wish to remain anonymous."
        ),
        text=_("Contact (optional):"),
    ),
]
