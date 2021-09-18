from django.contrib import admin
from django.forms import *
from . import models
from searchableselect.widgets import SearchableSelect
from easy_select2 import select2_modelform
# Register your models here.
admin.site.Title = "Maa Shakti Admin Login"
admin.site.site_header= "Maa Shakti Admin Panel"
admin.site.site_title = "Maa Shakti Admin Panel"
admin.site.index_title = ""
# admin.site.register(models.ContactUs)

admin.site.register(models.EventPhotos)
admin.site.register(models.EventYoutubeVideos)
@admin.register(models.ContactUs)
class ContactUs(admin.ModelAdmin):
    list_display = ["Name", "Email", "Contact", "Message"]

@admin.register(models.PropertyTypeRef)
class PropertyTypeRef(admin.ModelAdmin):
    search_fields = ["TypeName"]
    fields = ["TypeName"]

    def has_module_permission(self, request):
        return False



@admin.register(models.Cities)
class Cities(admin.ModelAdmin):
    #autocomplete_fields = ['LocationState', 'LocationCity']
    search_fields = ['CityName']
    # def has_module_permission(self, request):
    #     return False

@admin.register(models.FurnishedType)
class FurnishedType(admin.ModelAdmin):
    search_fields = ['TypeName']
    fields = ["TypeName"]
    def has_module_permission(self, request):
        return False


@admin.register(models.States)
class States(admin.ModelAdmin):
    search_fields = ["StateName"]
    fields = ["StateName"]
    # def has_module_permission(self, request):
    #     return False


@admin.register(models.AgentRef)
class AgentRef(admin.ModelAdmin):
    search_fields = ["AgentName"]
    autocomplete_fields = ["AgentLocation"]
    def Agent_Location(self, obj):
        return obj.AgentLocation.LocationName

    list_display = ("AgentName", "AgentLocation")
    def has_module_permission(self, request):
        return False


@admin.register(models.LocationsRef)
class LocationsRef(admin.ModelAdmin):
    autocomplete_fields = ['LocationState', 'LocationCity']
    search_fields = ["LocationName"]
    fields = ["LocationName", "LocationState", "LocationCity"]
    def Location(self, obj):
        return obj.LocationName

    def State(self, obj):
        return obj.LocationState.StateName

    def City(self, obj):
        return obj.LocationCity.CityName

    list_display = ("Location", "State", "City")

    # def has_module_permission(self, request):
    #     return False

class PropertyImags(admin.StackedInline):
    model = models.PropertyImags


class FacilityForm(ModelForm):
    class Meta:
        model = models.Facilities
        exclude = ()
        widgets = {
            'FacilityName': SearchableSelect(model='models.Facilities', search_field='FacilityName', many=True)
        }


FacilityFormSelect = select2_modelform(models.PropFacilities, attrs={'width': '550px'})

@admin.register(models.Property)
class Property(admin.ModelAdmin):
    list_filter = ["IsVisible", "PropertyType", "TxnType", "PriceUnit", "Availability", "OurProperty"]
    form = FacilityFormSelect
    inlines = [PropertyImags]
    search_fields = ["Title"]
    autocomplete_fields = ["PropertyLocation", "AgentID", "PropertyType", "Area"]

    def get_faci(self, obj):
        return " | ".join([p.FacilityName for p in obj.FacilityID.all()])
    list_display = ["PropertyID", "get_faci"]
    formfield_overrides = {
        models.PropFacilities.FacilityID: {'widget': SearchableSelect(model='models.Facilities', search_field='FacilityName')},
    }

    def show(self, obj):
        return str("EDIT")

    def Location_Of_Property(self, obj):
        return obj.PropertyLocation.LocationName

    def Agent_Name(self, obj):
        return obj.AgentID.AgentName

    def Property_Type_Name(self, obj):
        return obj.PropertyType.TypeName
    # fields = ("AgentID", "PropertyType",("FacilityOne", "FacilityTwo", "FacilityThree", "FacilityFour", "FacilityFive", "FacilitySix", "FacilitySeven", "FacilityEight", "FacilityNine", "FacilityTen"), "FacilityID", "PropertyImage", "TxnType", "Title", ("Price", "PriceUnit"), "PropertyLocation", "Area", "PropertyAddress", "PropertyAddress1", "ShortDescription", "Availability", ("CarpetArea", "RateSQFT"),("BuiltUpArea", "PropertySize"), ("FloorNumber", "Parking"), "TransactionType", "Furnished", "FurnishedDesc", "TotalFloor", "PossessionStatus",  ("Balcony", "Bathroom", "Bedroom"), ("OurProperty", "InGallery", "IsVisible"))
    list_display = ("show", "IsVisible", "Title", "PropertyImage", "TxnType", "Price", "PriceUnit", "PropertyAddress", "Availability", "OurProperty")
    readonly_fields = ("PriceCalculatedAmount", "RentCalculatedAmount")

    fieldsets = (
        ("Please fill the information below", {
            'fields': ("AgentID", "PropertyType")
        }),

        ("Other Required Informations", {
            'fields': ("TxnType", "Title", "PropertyLocation", "Area", "PropertyAddress", "PropertyAddress1", "ShortDescription", "Availability", ("CarpetArea", "RateSQFT"),("BuiltUpArea", "PropertySize"), ("FloorNumber", "Parking"), "TotalFloor", ("Balcony", "Bathroom", "Bedroom"), ("OurProperty", "InGallery", "IsVisible"))
        }),

        ("BUY Exclusive Fields", {
            'fields': ("Price", "PriceUnit",  "PriceCalculatedAmount", "PossessionStatus", "PossessionDate")
        }),

        ("RENT Exclusive Fields", {
            'fields': ("RentAmount", "RentAmountUnit", "RentCalculatedAmount",  "Deposit", "DepositUnit", "CustomerStatus", "CustomerFeast", "PetsAllowed", "RentPossessionDate")
        }),


        ("Basic Facilities", {
            'fields': (("FacilityOne", "FacilityTwo", "FacilityThree", "FacilityFour", "FacilityFive"), ("FacilitySix", "FacilitySeven", "FacilityEight", "FacilityNine", "FacilityTen"))
        }),

        ("Additional Facilities", {
            'fields': ("FacilityID",)
        }),

        ("Furnishing Details", {
            'fields': ("Furnished", ("FurnishOne", "FurnishTwo", "FurnishThree", "FurnishFour"), ("FurnishFive", "FurnishSix", "FurnishSeven", "FurnishEight"), ("FurnishNine", "FurnishTen", "FurnishEleven"), ("FurnishThingOne" , "FurnishThingTwo" , "FurnishThingThree" , "FurnishThingFour" , "FurnishThingFive" , "FurnishThingSix" , "FurnishThingSeven"), "FurnishedDesc", "PropertyImage")
        }),

        )


    def make_invisible(modeladmin, request, queryset):
        queryset.update(IsVisible=False)

    def make_visible(modeladmin, request, queryset):
        queryset.update(IsVisible=True)

    actions = [make_invisible, make_visible]

@admin.register(models.Facilities)
class Facilities(admin.ModelAdmin):
    search_fields = ["FacilityName"]
    fields = ["FacilityName"]


class PropFacilitiesAdmin(admin.ModelAdmin):
    fields = ["PropertyID", "FacilityID"]
    autocomplete_fields = ["PropertyID"]
    def get_faci(self, obj):
        return " | ".join([p.FacilityName for p in obj.FacilityID.all()])
    list_display = ["PropertyID", "get_faci"]
    formfield_overrides = {
        models.PropFacilities.FacilityID: {'widget': SearchableSelect(model='models.Facilities', search_field='FacilityName', limit=10)},
    }

    def has_module_permission(self, request):
        return False

admin.site.register(models.PropFacilities, PropFacilitiesAdmin)

@admin.register(models.NearByStations)
class NearByStations(admin.ModelAdmin):
    fields = ["PropertyID", "MetroTrain", "Schools", "Airport"]
    def has_module_permission(self, request):
        return False

# @admin.register(models.PropertyDetails)
# class PropertyDetails(admin.ModelAdmin):
#     pass

@admin.register(models.RoleMaster)
class RoleMaster(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

@admin.register(models.Blog)
class Blog(admin.ModelAdmin):
    search_fields = ["title"]
    fields = ["blogimage", "title", "url", "summary", "point1", "point2", "point3", "point4", "point5", "point6", "point7", "point8", "point9", "point10", "desc1", "desc2", "desc3", "desc4", "desc5", "desc6", "desc7", "desc8", "desc9", "desc10", "conclusiontopic", "conclusiondesc"]
    list_display = ("title", "url")



@admin.register(models.Feedback)
class Feedback(admin.ModelAdmin):
    pass

@admin.register(models.Gallery)
class Gallery(admin.ModelAdmin):
    # fields = ["title", "image"]
    list_display = ("title", "image")

# @admin.register(models.Spaces)
# class Spaces(admin.ModelAdmin):
#     pass


@admin.register(models.BannerImages)
class BannerImages(admin.ModelAdmin):
    list_display = ["BannerName", "BannerImageItem"]

@admin.register(models.FAQs)
class FAQ(admin.ModelAdmin):
    list_display = ["FAQID", "Question", "Answer"]

@admin.register(models.Area)
class Area(admin.ModelAdmin):
    autocomplete_fields = ["LocationID"]
    search_fields = ["AreaName"]
    list_display = ["AreaName", "LocationID"]
    # def has_module_permission(self, request):
    #     return False

@admin.register(models.Testimonials)
class Testimonials(admin.ModelAdmin):
    list_display = ["ClientImage", "ClientName", "ClientPosition", "ClientWords"]

@admin.register(models.GalleryVideos)
class GalleryVideos(admin.ModelAdmin):
    pass