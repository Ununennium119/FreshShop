from django.contrib import admin

from .models import SiteSetting, BusinessTime, TeamMember, SliderImage, InstagramImage, ContactInfo, DiscountAd


class BusinessTimeInline(admin.StackedInline):
    model = BusinessTime


class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ["site_name", "site_url", "is_main_setting"]
    inlines = [BusinessTimeInline]


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "is_active"]
    list_editable = ["is_active"]


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "is_responded"]


class DiscountAdAdmin(admin.ModelAdmin):
    list_display = ["text", "is_active"]
    list_editable = ["is_active"]


admin.site.register(SiteSetting, SiteSettingAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(SliderImage)
admin.site.register(InstagramImage)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(DiscountAd, DiscountAdAdmin)
