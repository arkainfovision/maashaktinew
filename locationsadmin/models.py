from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# class LocationModel(models.Model):
#     location = models.CharField(max_length=200)
#     sublocation = models.CharField(max_length=1024, default="")

class Testimonials(models.Model):
    TestimonialID = models.AutoField(primary_key=True)
    ClientImage = models.ImageField(upload_to="clientphotos", default="")
    ClientName = models.CharField(max_length=250, default="")
    ClientPosition = models.CharField(max_length=500, default="")
    ClientWords = models.TextField(default="")

    class Meta:
        verbose_name = "TESTIMONIAL"
        verbose_name_plural = "TESTIMONIAL"
        # app_label = "Others"

class FAQs(models.Model):
    FAQID = models.AutoField(primary_key=True)
    Question = models.TextField(default="")
    Answer = models.TextField(default="")

    class Meta:
        verbose_name = "FAQS"
        verbose_name_plural = "FAQS"

class BannerImages(models.Model):
    BannerID = models.AutoField(primary_key=True)
    BannerName = models.CharField(max_length=250, default="")
    BannerImageItem = models.ImageField(upload_to='homepagebanners', default="")

    class Meta:
        verbose_name = "HOME PAGE BANNER"
        verbose_name_plural = "HOME PAGE BANNER"


class Gallery(models.Model):
    GID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name = "Title")
    image = models.ImageField(upload_to='galleryimages', default="")

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'GALLERY PICTURES'
        verbose_name_plural = 'GALLERY PICTURES'

class States(models.Model):
    STID = models.AutoField(primary_key=True)
    StateName = models.CharField(max_length=200, verbose_name = "State Name")
    BitStatus = models.IntegerField(default=1)

    def __str__(self):
        return str(str(self.STID) + " => " + str(self.StateName))

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'STATE'
        verbose_name_plural = 'STATE'

class Cities(models.Model):
    CTID = models.AutoField(primary_key=True)
    CityName = models.CharField(max_length=200)
    STID =  models.ForeignKey(States, on_delete=models.CASCADE,  verbose_name="State")

    def __str__(self):
        return str(self.CityName) + ", " + str(self.STID.StateName)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'CITY'
        verbose_name_plural = 'CITY'

class Blog(models.Model):
    blogid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500, verbose_name="Blog Title")
    url = models.CharField(max_length=500, verbose_name="Blog URL")
    summary = models.TextField(verbose_name="Blog Summary")
    blogimage = models.ImageField(upload_to='blogbanner', default="")

    point1 = models.CharField(max_length=500, blank=True, verbose_name="point 1")
    point2 = models.CharField(max_length=500, blank=True, verbose_name="point 2")
    point3 = models.CharField(max_length=500, blank=True, verbose_name="point 3")
    point4 = models.CharField(max_length=500, blank=True, verbose_name="point 4")
    point5 = models.CharField(max_length=500, blank=True, verbose_name="point 5")
    point6 = models.CharField(max_length=500, blank=True, verbose_name="point 6")
    point7 = models.CharField(max_length=500, blank=True, verbose_name="point 7")
    point8 = models.CharField(max_length=500, blank=True, verbose_name="point 8")
    point9 = models.CharField(max_length=500, blank=True, verbose_name="point 9")
    point10 = models.CharField(max_length=500, blank=True, verbose_name="point 10")

    desc1 = models.TextField(blank=True, verbose_name="Description 1")
    desc2 = models.TextField(blank=True, verbose_name="Description 2")
    desc3 = models.TextField(blank=True, verbose_name="Description 3")
    desc4 = models.TextField(blank=True, verbose_name="Description 4")
    desc5 = models.TextField(blank=True, verbose_name="Description 5")
    desc6 = models.TextField(blank=True, verbose_name="Description 6")
    desc7 = models.TextField(blank=True, verbose_name="Description 7")
    desc8 = models.TextField(blank=True, verbose_name="Description 8")
    desc9 = models.TextField(blank=True, verbose_name="Description 9")
    desc10 = models.TextField(blank=True, verbose_name="Description 10")

    conclusiontopic = models.CharField(max_length=500, verbose_name="Conclusion Topic", blank=True)
    conclusiondesc = models.TextField(verbose_name="Conclusion Description", blank=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'BLOGS'
        verbose_name_plural = 'BLOGS'

class LocationsRef(models.Model):
    LOCID = models.AutoField(primary_key=True)
    LocationName = models.CharField(max_length=500, verbose_name="Location Name")
    LocationState = models.ForeignKey(States, on_delete=models.CASCADE, verbose_name="Select State")
    LocationCity = models.ForeignKey(Cities, on_delete=models.CASCADE,  verbose_name="Select City")

    BitStatus = models.IntegerField(default=1)

    def __str__(self):
        return str(self.LocationName) + ", " + str(self.LocationCity.CityName) + ", " + str(self.LocationState.StateName)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'LOCATION'
        verbose_name_plural = 'LOCATION'

class Area(models.Model):
    AreasIDs = models.AutoField(primary_key=True)
    AreaName = models.CharField(max_length=500, verbose_name="Area Name")
    LocationID = models.ForeignKey(LocationsRef, on_delete=models.CASCADE, verbose_name="Select Location")

    def __str__(self):
        return str(self.AreaName) + " | " + str(self.LocationID.LocationName) + ", " + str(self.LocationID.LocationCity.CityName) + ", " + str(self.LocationID.LocationState.StateName)

    class Meta:
        verbose_name = 'AREA'
        verbose_name_plural = 'AREA'

class AgentRef(models.Model):
    AGENTID = models.AutoField(primary_key=True)
    AgentName = models.CharField(max_length=500, verbose_name="Agent Name")
    AgentLocation = models.ForeignKey(LocationsRef, on_delete=models.CASCADE, verbose_name="Agent Location")
    def __str__(self):
        return str(self.AgentName) + " | " + str(self.AgentLocation)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'AGENT'
        verbose_name_plural = 'AGENT'

class ContactUs(models.Model):
    CONTACTID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=500, verbose_name="Name")
    Contact = models.CharField(max_length=500, verbose_name="Contact Number")
    Email = models.CharField(max_length=500, verbose_name="Email")
    Message = models.CharField(max_length=1000, verbose_name="Message")

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'CONTACT US'
        verbose_name_plural = 'CONTACT US'


class PropertyTypeRef(models.Model):
    TypeID = models.AutoField(primary_key=True)
    TypeName = models.CharField(max_length=250, verbose_name="Property Type")
    BitStatus = models.IntegerField(default=1)

    def __str__(self):
        return str(self.TypeName)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'PROPERTY TYPE'
        verbose_name_plural = 'PROPERTY TYPE'

class FurnishedType(models.Model):
    TypeID = models.AutoField(primary_key=True)
    TypeName = models.CharField(max_length=250, verbose_name="Furnished Type")
    BitStatus = models.IntegerField(default=1)

    def __str__(self):
        return str(self.TypeName)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'FURNISHED TYPE'
        verbose_name_plural = 'FURNISHED TYPE'

# class PropertyImages(models.Model):
#     PropertyID = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name = "Property ID")

class Facilities(models.Model):
    FacilityID = models.AutoField(primary_key=True)
    FacilityName = models.CharField(max_length=250, verbose_name="Facility Name")
    # Icon = models.TextField()

    def __str__(self):
        return str(self.FacilityName)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'FACILITY'
        verbose_name_plural = 'FACILITY'



class Property(models.Model):
    TXNTYPEOPTIONS = (
        ('BUY', 'BUY'),
        ('RENT', 'RENT'),
    )

    TXNTYPEOPTIONSUSER = (
        ('BUY', 'BUY'),
        ('RENT', 'RENT'),
    )

    PRICEUNITS = (
        ('Cr', 'Cr'),
        ('Lakhs', 'Lakhs'),
        ('K', 'K'),
    )

    FurnishedOptions = (
        ('Furnished', 'Furnished'),
        ('Semi Furnished', 'Semi Furnished'),
        ('Unfurnished', 'Unfurnished'),
    )

    PossessionOptions = (
        ('Ready to Move', 'Ready to Move'),
        ('Under Construction', 'Under Construction')
    )


    CustomerStatusOptions = (
        ('Any', 'Any'),
        ('Family', 'Family'),
        ('Bachelor', 'Bachelor')
    )

    CustomerFeastOptions = (
        ('Any', 'Any'),
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg')
        )

    PetsAllowedOptions = (
        ('Allowed', 'Allowed'),
        ('Not Allowed', 'Not Allowed')
        )

    PropertyID = models.AutoField(primary_key=True)
    PropertyLocation = models.ForeignKey(LocationsRef, on_delete=models.CASCADE, verbose_name = "PROPERTY LOCATION")
    Area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name="AREA", null=True)
    AgentID = models.ForeignKey(AgentRef, on_delete=models.CASCADE, verbose_name = "AGENT")
    PropertyType = models.ForeignKey(PropertyTypeRef, on_delete=models.CASCADE, verbose_name = "PROPERTY TYPE")
    TxnType = models.CharField(max_length=200, default="", choices=TXNTYPEOPTIONSUSER, verbose_name = "TRANSACTION STATUS")
    Title = models.CharField(max_length=5000, verbose_name = "PROPERTY TITLE")
    FacilityID = models.ManyToManyField(Facilities, blank=True, verbose_name="FACILITY NAME")
    PropertyImage = models.ImageField(upload_to='propertybanner', default="building.png", verbose_name="PROPERTY PROFILE MAIN IMAGE")
    Price = models.FloatField(blank=True, null=True, default="", verbose_name = "PRICE")
    PriceUnit = models.CharField(max_length=250, default="", choices=PRICEUNITS, verbose_name = "")
    PropertyAddress = models.CharField(max_length=250, verbose_name='ADDRESS LINE 1', default="", blank=True)
    PropertyAddress1 = models.CharField(max_length=250, verbose_name='ADDRESS LINE 2', default="", blank=True)
    ShortDescription = models.TextField(verbose_name = "PROPERTY DESCRIPTION", max_length=5000, default="", blank=True)
    Availability = models.CharField(max_length=250, default="Available", blank=True, verbose_name = "AVAILABLE")
    CarpetArea = models.FloatField(verbose_name="CARPET AREA")
    FloorNumber = models.CharField(max_length=250, default="", verbose_name = "FLOOR NUMBER")
    Parking = models.IntegerField(verbose_name = "PARKING", default=0)
    TransactionType = models.CharField(max_length=250, default="", choices=TXNTYPEOPTIONS, verbose_name = "TRANSACTION TYPE")
    Furnished = models.CharField(max_length=250, default="", choices=FurnishedOptions, verbose_name = "FURNISHED")
    FurnishedDesc = models.TextField(default="", verbose_name = "FURNISHED DESCRIPTION", blank=True)
    TotalFloor = models.CharField(max_length=250, default="", verbose_name = "TOTAL FLOORS")
    PropertySize = models.FloatField(verbose_name = "SUPER BUILT UP", blank=True, null=True)
    PossessionStatus = models.CharField(max_length=250, default="", choices=PossessionOptions, verbose_name = "POSSESSION STATUS")
    PossessionDate = models.DateField(null=True, blank=True, verbose_name="POSSESSION DATE")
    RateSQFT = models.FloatField(null=True, default="", blank=True, verbose_name = "RATE PER SQRFT")
    BuiltUpArea = models.FloatField(verbose_name = "BUILTUP AREA")
    Balcony = models.IntegerField(default = 0, verbose_name = "BALCONY")
    # BedType = models.CharField(max_length=250, default="", verbose_name = "Bed Type")
    # Beds = models.IntegerField(default="")
    Bathroom = models.IntegerField(default = 0, verbose_name = "BATHROOM")
    Bedroom = models.IntegerField(default = 0, verbose_name = "BEDROOM")
    # RoomType = models.CharField(max_length=250, default="", verbose_name = "Room Type")
    # CheckIn = models.CharField(max_length=250, default="", verbose_name = "Check In")
    # CheckOut = models.CharField(max_length=250, default="", verbose_name = "Check Out")
    OurProperty = models.BooleanField(default=False, verbose_name="OUR PROPERTY?")
    InGallery = models.BooleanField(default=False, verbose_name="IN GALLERY?")
    IsVisible = models.BooleanField(default=True, verbose_name="IS VISIBLE?")
    FacilityOne = models.BooleanField(default=True, verbose_name="Party Hall")
    FacilityTwo = models.BooleanField(default=True, verbose_name="Fully Equipped Gymnasium")
    FacilityThree = models.BooleanField(default=True, verbose_name="Business Centre/Library")
    FacilityFour = models.BooleanField(default=True, verbose_name="Indoor Games Area")
    FacilityFive = models.BooleanField(default=True, verbose_name="Spa Treatment Room")
    FacilitySix = models.BooleanField(default=True, verbose_name="Swimming Pool and Kids Pool")
    FacilitySeven = models.BooleanField(default=True, verbose_name="Children’s Play Area")
    FacilityEight = models.BooleanField(default=True, verbose_name="Swimming Pool")
    FacilityNine = models.BooleanField(default=True, verbose_name="Terrace Garden")
    FacilityTen = models.BooleanField(default=True, verbose_name="Shopping Centre")

    FurnishOne = models.BooleanField(default=True, verbose_name="Washing Machine", blank=True)
    FurnishTwo = models.BooleanField(default=True, verbose_name="Water Purifier", blank=True)
    FurnishThree = models.BooleanField(default=True, verbose_name="Microwave", blank=True)
    FurnishFour = models.BooleanField(default=True, verbose_name="Curtains", blank=True)
    FurnishFive = models.BooleanField(default=True, verbose_name="Chimney", blank=True)
    FurnishSix = models.BooleanField(default=True, verbose_name="Exhaust Fan", blank=True)
    FurnishSeven = models.BooleanField(default=True, verbose_name="Sofa", blank=True)
    FurnishEight = models.BooleanField(default=True, verbose_name="Dining Table", blank=True)
    FurnishNine = models.BooleanField(default=True, verbose_name="Stove", blank=True)
    FurnishTen = models.BooleanField(default=True, verbose_name="Modular Kitchen", blank=True)
    FurnishEleven = models.BooleanField(default=True, verbose_name="Fridge", blank=True)

    FurnishThingOne = models.IntegerField(default = 0, verbose_name="WARDROBE")
    FurnishThingTwo = models.IntegerField(default = 0, verbose_name="BEDS")
    FurnishThingThree = models.IntegerField(default = 0, verbose_name="FANS")
    FurnishThingFour = models.IntegerField(default = 0, verbose_name="LIGHT")
    FurnishThingFive = models.IntegerField(default = 0, verbose_name="AC")
    FurnishThingSix = models.IntegerField(default = 0, verbose_name="GEYSER")
    FurnishThingSeven = models.IntegerField(default = 0, verbose_name="TV")


    RentAmount = models.FloatField(blank=True, null=True, verbose_name = "RENT AMOUNT")
    CustomerStatus = models.CharField(max_length=250, default="", choices=CustomerStatusOptions, verbose_name = "CUSTOMER STATUS")
    CustomerFeast = models.CharField(max_length=250, default="", choices=CustomerFeastOptions, verbose_name = "CUSTOMER FEAST")
    PetsAllowed = models.CharField(max_length=250, default="", choices=PetsAllowedOptions, verbose_name="PET ALLOWED?")
    RentPossessionDate = models.DateField(null=True, blank=True, verbose_name="RENT POSSESSION DATE")
    Deposit = models.CharField(max_length=250, default="", verbose_name="DEPOSIT AMOUNT", blank=True, null=True)
    DepositUnit = models.CharField(max_length=250, default="", choices=PRICEUNITS, verbose_name="DEPOSIT UNIT", blank=True, null=True)
    RentAmountUnit = models.CharField(max_length=250, default="", choices=PRICEUNITS, verbose_name = "")


    RentCalculatedAmount = models.FloatField(blank=True, null=True, default = float(0), verbose_name = "RENT AMOUNT CALCULATED")
    PriceCalculatedAmount = models.FloatField(blank=True, null=True, default = float(0), verbose_name = "PRICE AMOUNT CALCULATED")

    def save(self, *args, **kwargs):

        if self.TxnType == "BUY":
            # consider price part
            try:
                saveprice = 0
                if self.PriceUnit == "Cr":
                    saveprice = self.Price * 10000000
                elif self.PriceUnit == "Lakh":
                    saveprice = self.Price * 100000
                elif self.PriceUnit == "Lakhs":
                    saveprice = self.Price * 100000
                elif self.PriceUnit == "Lac":
                    saveprice = self.Price * 100000
                elif self.PriceUnit == "K":
                    saveprice = self.Price * 1000

                self.PriceCalculatedAmount = saveprice
            except:
                saveprice = 0
                self.PriceCalculatedAmount = saveprice


        else:
            # consider rent part
            try:
                saverent = 0
                if self.RentAmountUnit == "Cr":
                    saverent = self.RentAmount * 10000000
                elif self.RentAmountUnit == "Lakh":
                    saverent = self.RentAmount * 100000
                elif self.RentAmountUnit == "Lakhs":
                    saverent = self.RentAmount * 100000
                elif self.RentAmountUnit == "Lac":
                    saverent = self.RentAmount * 100000
                elif self.RentAmountUnit == "K":
                    saverent = self.RentAmount * 1000

                self.RentCalculatedAmount = saverent
            except:
                saverent = 0
                self.RentCalculatedAmount = saverent

        super(Property, self).save(*args, *kwargs)

    def __str__(self):
        return str(str(self.PropertyID) + " | " + str(self.Title) + " | " + str(self.ShortDescription))

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'PROPERTY'
        verbose_name_plural = 'PROPERTIES'





class PropertyImags(models.Model):
    TheProperty = models.ForeignKey(Property,  on_delete=models.CASCADE, default=None)
    Images = models.ImageField("propertyIndividualImages", default="")

    def __str__(self):
        return str(self.TheProperty.Title)


class Feedback(models.Model):
    FeedBackID = models.AutoField(primary_key=True)
    Experience = models.CharField(max_length=250)
    Comment = models.CharField(max_length=500)
    Name = models.CharField(max_length=250)
    Email = models.CharField(max_length=250)


    class Meta:
        db_table = ''
        managed = True
        verbose_name = "FEEDBACK"
        verbose_name_plural = 'FEEDBACK'

    def __str__(self):
        return str(self.Name)




class PropFacilities(models.Model):
    ID = models.AutoField(primary_key=True)
    PropertyID = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name="Select Property")
    FacilityID = models.ManyToManyField(Facilities)
    # Icon = models.TextField() , on_delete=models.CASCADE, verbose_name="Select Facility"

    def __str__(self):
        return str(str(self.PropertyID))

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'PROPERTY FACILITY'
        verbose_name_plural = 'PROPERTY FACILITY'

class NearByStations(models.Model):
    StationID = models.AutoField(primary_key=True)
    PropertyID = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name="Select Property")
    MetroTrain = models.CharField(max_length=250, verbose_name="Metro Train")
    Schools = models.CharField(max_length=250)
    Airport = models.CharField(max_length=250)
    CreatedBy = models.CharField(max_length=250)
    UpdatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.MetroTrain)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'NEAR BY STATION'
        verbose_name_plural = 'NEAR BY STATION'

# class PropertyDetails(models.Model):
#     PropertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
#     CarpetArea = models.CharField(max_length=250)
#     FloorNumber = models.CharField(max_length=250)
#     TransactionType = models.CharField(max_length=250)
#     Furnished = models.CharField(max_length=250)
#     TotalFloor = models.CharField(max_length=250)
#     PropertySize = models.CharField(max_length=250)
#     PossessionStatus = models.CharField(max_length=250)
#     RateSQFT = models.CharField(max_length=250)
#     BuiltUpArea = models.CharField(max_length=250)
#     CreatedBy = models.CharField(max_length=250)
#     UpdatedAt = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.PropertyID)

#     class Meta:
#         db_table = ''
#         managed = True
#         verbose_name = 'PROPERTY DETAIL'
#         verbose_name_plural = 'PROPERTY DETAIL'

class RoleMaster(models.Model):
    RoleID = models.AutoField(primary_key=True)
    RoleName = models.CharField(max_length=250, verbose_name="Role")

    def __str__(self):
        return str(self.RoleName)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'AGENT ROLE'
        verbose_name_plural = 'AGENT ROLE'


# class Spaces(models.Model):
#     SpaceID = models.AutoField(primary_key=True)
#     PropertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
#     Accommodates = models.IntegerField()
#     BedType = models.CharField(max_length=250)
#     Beds = models.IntegerField()
#     Bathroom = models.IntegerField(max_length=250)
#     Bedroom = models.IntegerField()
#     RoomType = models.CharField(max_length=250)
#     CheckIn = models.CharField(max_length=250)
#     CheckOut = models.CharField(max_length=250)
#     CreatedBy = models.CharField(max_length=250)
#     UpdatedAt = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.PropertyID)

#     class Meta:
#         db_table = ''
#         managed = True
#         verbose_name = 'PROPERTY SPACE'
#         verbose_name_plural = 'PROPERTY SPACE'

class GalleryVideos(models.Model):
    vidid = models.AutoField(primary_key=True)
    videotitle = models.CharField(max_length=500)
    video = models.FileField(upload_to="videosofgallery", default="")

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'GALLERY VIDEOS'
        verbose_name_plural = 'GALLERY VIDEOS'


class EventPhotos(models.Model):
    PhotoTitle = models.CharField(max_length = 255)
    Photo = models.ImageField(upload_to = "eventphotos")

    class Meta:
        verbose_name = 'EVENT PHOTO'
        verbose_name_plural = 'EVENT PHOTOS'


class EventYoutubeVideos(models.Model):
    YoutubeTitle = models.CharField(max_length = 255)
    YoutubeUrl = models.CharField(max_length = 255)

    def __str__(self):
        return str(self.YoutubeTitle)
    class Meta:
        verbose_name = 'EVENT YOUTUBE VIDEO'
        verbose_name_plural = 'EVENT YOUTUBE VIDEOS'

