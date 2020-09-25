from django.contrib import admin
from .models import Instruction, InstructionList, SiteInfo, SiteFaq
# Register your models here.


class InstructionListInline(admin.StackedInline):
    model = InstructionList
    extra = 0


class InstructionAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ('title',)
    list_per_page = 20
    inlines = [
        InstructionListInline
    ]


admin.site.register(Instruction, InstructionAdmin)


class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'site_phone', 'site_email']

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True


admin.site.register(SiteInfo, SiteInfoAdmin)


class SiteFaqAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']
    search_fields = ['question', 'answer']
    list_per_page = 20


admin.site.register(SiteFaq, SiteFaqAdmin)
