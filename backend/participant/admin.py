from django.contrib import admin
from .models import Participant
# from experiment.models.profile import Profile


# class ProfileInline(admin.TabularInline):
#     """Profile inline admin for SessionAdmin"""

#     model = Profile
#     extra = 0


class ParticipantAdmin(admin.ModelAdmin):
    # inlines = [ProfileInline]
    list_per_page = 50
    search_fields = ['unique_hash', 'id', 'country_code']
    list_display = ('__str__',
                    'country_code',
                    'session_count',
                    )
    list_filter = [
        ('session__experiment', admin.RelatedOnlyFieldListFilter)
    ]


admin.site.register(Participant, ParticipantAdmin)
