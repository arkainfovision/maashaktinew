from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from . import models
import ast
import decimal
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags

# Create your views here.
def officialpage(request):
    faq = models.FAQs.objects.all()
    gallery = models.Gallery.objects.all()
    testimonial = models.Testimonials.objects.all()
    ourprop = list(models.Property.objects.all().filter(OurProperty = True, IsVisible= True))
    return render(request, "aboutuscopy.html", {"faqs": faq, "testimonials": testimonial, "ourprop": ourprop, "gallery": gallery})

def compare(request):
    propstobecompared = request.GET.getlist('proparr')
    proplist = propstobecompared[0].split(",")
    print(proplist)
    for i in range(0, len(proplist)):
        proplist[i] = int(proplist[i])
    data = list(models.Property.objects.values().filter(PropertyID__in = proplist, IsVisible = True))
    print(data)
    return render(request, "compare.html", {"props":data})

def contact(request):
    return render(request, "contact.html", {"title" : "Contact Us"})

def prop(request):
    return render(request, "prop.html", {"title" : "Property"})

def myprojects(request):
    return render(request, "myprojects.html", {"title" : "My Projects"})

def location(request):
    allStates = models.States.objects.all()
    locationData = models.LocationsRef.objects.all()
    return render(request, "locationform.html", {"title" : "Location Administrator", "thedata": allStates, "locationsData" : locationData})

def getCities(request):
    datatorespond = request.GET["data"]
    allcities =list(models.Cities.objects.values_list('CityName', flat=True).filter(STID=datatorespond))
    allcitiesID = list(models.Cities.objects.values_list('CTID', flat=True).filter(STID=datatorespond))
    print("JSON Accepted? : " + str(request.accepts('application/json')))
    return JsonResponse({"cities": allcities, "cityID" : allcitiesID}, safe=False)

def locationFormSubmission(request):
    locationName = request.POST["locationname"]
    locationState = request.POST["locationstate"]
    locationStateNameID = list(models.States.objects.filter(STID=locationState))[0]
    locationCity = request.POST["locationcity"]
    locationCityID = list(models.Cities.objects.filter(CityName=locationCity))[0]
    saveDataObject = models.LocationsRef(LocationName=str(locationName), LocationState=locationStateNameID, LocationCity=locationCityID, BitStatus=1)
    saveDataObject.save()
    return redirect('location')

def locationDelete(request):
    deleteData = request.GET["locid"]
    datatobedeleted = models.LocationsRef.objects.filter(LOCID=deleteData)
    print(datatobedeleted)
    datatobedeleted.delete()
    return redirect('location')

def locationUpdate(request):
    locid = request.POST["locmodify"]
    locname = request.POST["locationnamenew"]
    locstate = request.POST["locationstatenew"]
    loccity = request.POST["locationcitynew"]
    newdatatobeupdated = models.LocationsRef.objects.get(LOCID=str(locid))
    locationStateName = list(models.States.objects.filter(STID=locstate))[0]
    locationCityName = list(models.Cities.objects.filter(CityName=loccity))[0]
    newdatatobeupdated.LocationName = str(locname)
    newdatatobeupdated.LocationState = locationStateName
    newdatatobeupdated.LocationCity = locationCityName
    newdatatobeupdated.save()
    return redirect('location')



def getAreas(request):
    allStates = models.States.objects.all()
    locationData = models.LocationsRef.objects.all()
    return render(request, "areas.html", {"title": "Area Administrator", "thedata": allStates, "locationsData": locationData})

def gallery(request):
    images = models.Gallery.objects.all()
    videos = models.GalleryVideos.objects.all()
    properties = models.Property.objects.all().filter(IsVisible=True)
    youtubevideos = models.EventYoutubeVideos.objects.all()
    return render(request, "gallery.html", {"images": images, "videos": videos, "prop": properties, "yvids" : youtubevideos})

def eventgallery(request):
    images = models.Gallery.objects.all()
    videos = models.GalleryVideos.objects.all()
    properties = models.Property.objects.all().filter(IsVisible=True)
    eventphotos = models.EventPhotos.objects.all()
    youtubevideos = models.EventYoutubeVideos.objects.all()
    return render(request, "gallery2.html", {"images": images, "videos": videos, "prop": properties, "eventphotos" : eventphotos, "yvids" : youtubevideos})

def getAreasBasedOnStatesAndCity(request):
    citydata = models.Cities.objects.values_list('CTID', flat=True).filter(CTID=request.GET["locationcity"])[0]
    print(citydata)
    statedata = models.States.objects.values_list('STID', flat=True).filter(STID=request.GET["locationstate"])[0]
    print(statedata)
    locationData = list(models.LocationsRef.objects.values_list('LOCID','LocationName').filter(LocationCity=citydata).filter(LocationState=statedata))
    print(locationData)
    return JsonResponse({'areas': locationData}, safe=False)

def home(request):
    allStates = models.States.objects.all()
    locationData = models.LocationsRef.objects.all()
    city = models.Cities.objects.all()
    properties = models.Property.objects.all().filter(IsVisible=True)
    feedbacks = models.Feedback.objects.all()
    propinjson = serializers.serialize('json', models.Property.objects.all().filter(IsVisible=True))
    return render(request, "index.html", {"title" : "MaaShakti Property - Welcome", "state": allStates, "location" : locationData, "city": city, "property":properties, "propinjson": propinjson, "feedbacks" : feedbacks})

def getprops(request):
    txntype = request.POST["txntype"]
    stateinput = request.POST["stateinput"]
    cityinput = request.POST["cityinput"]
    locationinput = request.POST["locationinput"]
    # areainput= request.POST["areainput"]
    propertytypen = request.POST["proptype"]

    bathroom = request.POST.getlist("bathrooms")
    for i in range(0, len(bathroom)):
        bathroom[i] = int(bathroom[i])
    print(bathroom)
    bedroom = request.POST.getlist("bedroom")
    for i in range(0, len(bedroom)):
        bedroom[i] = int(bedroom[i])
    print(bedroom)

    filteredproperty = models.Property.objects.all().filter(IsVisible= True)
    maxprice = 0.0
    minprice = 0.0

    if 'minprice' in request.POST and 'maxprice' in request.POST:
        if request.POST["maxprice"] != '':
            maxprice = float(request.POST["maxprice"])

            try:
                if str(request.POST["priceunit"]) == "Cr":
                    maxprice =  maxprice * 10000000
                elif str(request.POST["priceunit"]) == "Lakh":
                    maxprice =  maxprice * 100000
                elif str(request.POST["priceunit"]) == "Lakhs":
                    maxprice =  maxprice * 100000
                elif str(request.POST["priceunit"]) == "Lac":
                    maxprice =  maxprice * 100000
                elif str(request.POST["priceunit"]) == "K":
                    maxprice =  maxprice * 1000
            except:
                maxprice = 0
        if request.POST["minprice"] != '':
            minprice = float(request.POST["minprice"])

            try:
                if str(request.POST["priceunit"]) == "Cr":
                    minprice =  minprice * 10000000
                elif str(request.POST["priceunit"]) == "Lakh":
                    minprice =  minprice * 100000
                elif str(request.POST["priceunit"]) == "Lakhs":
                    minprice =  minprice * 100000
                elif str(request.POST["priceunit"]) == "Lac":
                    minprice =  minprice * 100000
                elif str(request.POST["priceunit"]) == "K":
                    minprice =  minprice * 1000
            except:
                minprice = 0
    # filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationState = stateinput), PropertyType = propertytypen, TxnType = txntype, PriceCalculatedAmount__gte = int(request.POST["minprice"]), PriceCalculatedAmount__lte = int(request.POST["maxprice"]))
    # # print(filteredproperty)
    # return JsonResponse({"properties" : filteredproperty }, safe=False)


    if txntype == "Buy" or txntype == "Rent":
        if propertytypen == "0" or propertytypen == "1":
            if txntype == "Buy" and 'minprice' in request.POST:
                if stateinput != '0':
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationState = stateinput), PropertyType = propertytypen, TxnType = txntype, PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
                    return JsonResponse({"properties" : filteredproperty }, safe=False)
                    if cityinput != '0':
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), PropertyType = propertytypen, TxnType = txntype, PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
                        if locationinput != "0":
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation = locationinput, PropertyType = propertytypen, TxnType = txntype, PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
                            # if areainput != "0":
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput,  PropertyType = propertytypen, TxnType = txntype)
                            # else:
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput, PropertyType = propertytypen, TxnType = txntype)
                        else:
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), PropertyType = propertytypen, TxnType = txntype, PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
                    else:
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyType = propertytypen, TxnType = txntype, PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
                else:
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyType = propertytypen, TxnType = txntype, PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
            elif txntype == "Rent" and 'minprice' in request.POST:
                if stateinput != '0':
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationState = stateinput), PropertyType = propertytypen, TxnType = txntype, RentCalculatedAmount__gte = minprice, RentCalculatedAmount__lte = maxprice)
                    if cityinput != '0':
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), PropertyType = propertytypen, TxnType = txntype, RentCalculatedAmount__gte = minprice, RentCalculatedAmount__lte = maxprice)
                        if locationinput != "0":
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation = locationinput, PropertyType = propertytypen, TxnType = txntype)
                            # if areainput != "0":
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput,  PropertyType = propertytypen, TxnType = txntype)
                            # else:
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput, PropertyType = propertytypen, TxnType = txntype)
                        else:
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), PropertyType = propertytypen, TxnType = txntype,  RentCalculatedAmount__gte = minprice, RentCalculatedAmount__lte = maxprice)
                    else:
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyType = propertytypen, TxnType = txntype, RentCalculatedAmount__gte = minprice, RentCalculatedAmount__lte = maxprice)
                else:
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyType = propertytypen, TxnType = txntype, RentCalculatedAmount__gte = minprice, RentCalculatedAmount__lte = maxprice)
            else:
                if stateinput != '0':
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationState = stateinput), PropertyType = propertytypen, TxnType = txntype)
                    if cityinput != '0':
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), PropertyType = propertytypen, TxnType = txntype)
                        if locationinput != "0":
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation = locationinput, PropertyType = propertytypen, TxnType = txntype)
                            # if areainput != "0":
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput,  PropertyType = propertytypen, TxnType = txntype)
                            # else:
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput, PropertyType = propertytypen, TxnType = txntype)
                        else:
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), PropertyType = propertytypen, TxnType = txntype)
                    else:
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyType = propertytypen, TxnType = txntype)
                else:
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyType = propertytypen, TxnType = txntype)







        else:
            if txntype == "Buy" and 'minprice' in request.POST:
                if stateinput != '0':
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationState = stateinput), TxnType = txntype, PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
                    if cityinput != '0':
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput),TxnType = txntype, PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
                        if locationinput != "0":
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation = locationinput, TxnType = txntype, PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
                            # if areainput != "0":
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput,  PropertyType = propertytypen, TxnType = txntype)
                            # else:
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput, PropertyType = propertytypen, TxnType = txntype)
                        else:
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), TxnType = txntype, PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
                    else:
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, TxnType = txntype,PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
                else:
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, TxnType = txntype, PriceCalculatedAmount__gte = minprice, PriceCalculatedAmount__lte = maxprice)
            elif txntype == "Rent" and 'minprice' in request.POST:
                if stateinput != '0':
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationState = stateinput), TxnType = txntype, RentCalculatedAmount__gte = minprice, RentCalculatedAmount__lte = maxprice)
                    if cityinput != '0':
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), TxnType = txntype, RentCalculatedAmount__gte = minprice, RentCalculatedAmount__lte = maxprice)
                        if locationinput != "0":
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation = locationinput, TxnType = txntype)
                            # if areainput != "0":
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput,  PropertyType = propertytypen, TxnType = txntype)
                            # else:
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput, PropertyType = propertytypen, TxnType = txntype)
                        else:
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), TxnType = txntype, RentCalculatedAmount__gte = minprice, RentCalculatedAmount__lte = maxprice)
                    else:
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput,  TxnType = txntype, RentCalculatedAmount__gte = minprice, RentCalculatedAmount__lte = maxprice)
                else:
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, TxnType = txntype,  RentCalculatedAmount__gte = minprice, RentCalculatedAmount__lte = maxprice)
            else:
                if stateinput != '0':
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationState = stateinput), TxnType = txntype)
                    if cityinput != '0':
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), TxnType = txntype)
                        if locationinput != "0":
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation = locationinput, TxnType = txntype)
                            # if areainput != "0":
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput,  PropertyType = propertytypen, TxnType = txntype)
                            # else:
                            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput, PropertyType = propertytypen, TxnType = txntype)
                        else:
                            filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), TxnType = txntype)
                    else:
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, TxnType = txntype)
                else:
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,  TxnType = txntype)







            # if stateinput != '':
            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationState = stateinput), TxnType = txntype)
            #     if cityinput != '0':
            #         filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), TxnType = txntype)
            #         if locationinput != "0":
            #             filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation = locationinput, TxnType = txntype)
            #             # if areainput != "0":
            #             #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput, TxnType = txntype)
            #             # else:
            #             #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput, TxnType = txntype)
            #         else:
            #             filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, TxnType = txntype)
            #     else:
            #         filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, TxnType = txntype)
            # else:
            #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, TxnType = txntype)
    else:
        if propertytypen == "0" or propertytypen == "1":
            if stateinput != '0':
                filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationState = stateinput), PropertyType = propertytypen)
                if cityinput != '0':
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput), PropertyType = propertytypen)
                    if locationinput != "0":
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom,PropertyLocation = locationinput, PropertyType = propertytypen)
                        # if areainput != "0":
                        #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput, PropertyType = propertytypen)
                        # else:
                        #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput, PropertyType = propertytypen)
                    else:
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyType = propertytypen)
                else:
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyType = propertytypen)
            else:
                filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyType = propertytypen)
        else:
            if stateinput != '0':
                filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationState = stateinput))
                if cityinput != '0':
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__in = models.LocationsRef.objects.filter(LocationCity = cityinput))
                    if locationinput != "0":
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation = locationinput)
                        # if areainput != "0":
                        #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput)
                        # else:
                        #     filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput, PropertyLocation = locationinput)
                    else:
                        filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput, PropertyLocation__LocationCity = cityinput)
                else:
                    filteredproperty = models.Property.objects.all().filter(IsVisible= True, Bedroom__in = bedroom, Bathroom__in = bathroom, PropertyLocation__LocationState = stateinput)
            else:
                filteredproperty = models.Property.objects.all().filter(IsVisible= True)


    print(filteredproperty)
    data = serializers.serialize('json', filteredproperty)
    return HttpResponse(data, content_type="application/json")
    return JsonResponse({"properties" : filteredproperty }, safe=False)



def search(request):
    #query = request.GET["query"]
    # print(request.GET)
    txninput = request.GET["txninput"]
    locationnumber = request.GET["locationinput"]
    stateid = str(request.GET["stateinput"])
    cityid = request.GET["cityinput"]
    # print(proptype)
    #resultofproperties = list(models.Property.objects.values_list('Title', flat=True).filter(Title__contains=query))
    prop = list(models.Property.objects.all().filter(PropertyLocation = locationnumber, IsVisible = True, TxnType = txninput))
    # propprice = list(models.Property.objects.values_list('Price', flat=True).filter(PropertyLocation = locationnumber))
    # propaddress = list(models.Property.objects.values_list('PropertyAddress', flat=True).filter(PropertyLocation = locationnumber))
    # #print(resultonlocation)
    # return JsonResponse({'status': "OK", "query": locationnumber, "resultsonlocation": {"name": propname, "price": propprice, "address": propaddress}}, safe=False)
    allStates = models.States.objects.all()
    # allamenities = models.Facilities.objects.all()
    allproptypes = models.PropertyTypeRef.objects.all()
    locationData = models.LocationsRef.objects.all()
    city = models.Cities.objects.all()
    recommendation = models.Property.objects.all().filter(IsVisible = True, TxnType = txninput)[:4]
    return render(request, "search.html", {"recom":recommendation, "txninput": txninput, "locationid":locationnumber, "prop":prop, "state": allStates, "location" : locationData, "city": city, "cityid": cityid, "stateid": stateid, "allproptypes": allproptypes})

def blogs(request):
    blogs = models.Blog.objects.all()
    return render(request, "newblogs.html", {"blogs": blogs})

def aboutus(request):
    faq = models.FAQs.objects.all()
    gallery = models.Gallery.objects.all()
    testimonial = models.Testimonials.objects.all()
    ourprop = list(models.Property.objects.all().filter(OurProperty = True, IsVisible= True))
    return render(request, "aboutus.html", {"faqs": faq, "testimonials": testimonial, "ourprop": ourprop, "gallery": gallery})

def thanks(request):
    return render(request, "thanks.html")

def propertybytype(request):
    typeofprop = request.GET["typeofprop"]
    allStates = models.States.objects.all()
    allproptypes = models.PropertyTypeRef.objects.all()
    locationData = models.LocationsRef.objects.all()
    city = models.Cities.objects.all()
    props = models.Property.objects.all().filter(IsVisible= True, PropertyType = typeofprop)
    return render(request, "propertybytype.html", {"props":props, "state": allStates, "location" : locationData, "city": city, "allproptypes": allproptypes, "typeofprop" : typeofprop} )

def addcontact(request):
    name = request.POST["name"]
    contact = request.POST["contact"]
    email = request.POST["email"]
    message = request.POST["message"]

    try:
        subject = 'Enquiry for Maashakti from ' + str(name)
        message = 'Name : ' + str(name) + '\nContact : ' + str(contact) + '\nEmail : ' + str(email) + '\nMessage: ' + str(message) + '\nThank You'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = settings.SEND_TO_EMAIL
        send_mail( subject, message, email_from, recipient_list )
    except:
        print("Email sending failed...")
    savecontact = models.ContactUs(Name=str(name), Contact=str(contact), Email=str(email), Message=str(message))
    savecontact.save()

    return redirect('thanks')


def feedback(request):
    return render(request, "feedback.html")

def addfeedback(request):
    exp = request.POST["experience"]
    comments = request.POST["comments"]
    email = request.POST["email"]
    name = request.POST["name"]

    savefeedback = models.Feedback(Experience=str(exp), Comment=str(comments), Name=str(name), Email=str(email))
    savefeedback.save()
    return redirect('thanks')


class Utility:

    def num2words(self, num):
        num = decimal.Decimal(num)
        decimal_part = num - int(num)
        num = int(num)

        if decimal_part:
            return num2words(num) + " point " + (" ".join(num2words(i) for i in str(decimal_part)[2:]))

        under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
        tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
        above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakhs', 10000000: 'Crores'}

        if num < 20:
            return under_20[num]

        if num < 100:
            return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

        # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
        pivot = max([key for key in above_100.keys() if key <= num])

        return self.num2words(num // pivot) + ' ' + above_100[pivot] + ('' if num % pivot==0 else ' ' + num2words(num % pivot))





def individualproperty(request):
    propid = request.GET["property"]
    photosoftheproperty = models.PropertyImags.objects.all().filter(TheProperty = propid)
    propertydetails = models.Property.objects.all().filter(IsVisible= True, PropertyID=propid)
    propertycurrencydetails = models.Property.objects.values_list("Price", "PriceUnit").filter(IsVisible= True, PropertyID=propid)
    priceunit = str(propertycurrencydetails[0][1])
    finalWordOfCurrency = "Currency"
    try:
        pricetobeconverted = int(propertycurrencydetails[0][0])
        price = 0
        finalWordOfCurrency = ""
        if priceunit == "Cr":
            price = pricetobeconverted * 10000000
            print(price)
        elif priceunit == "Lakh":
            price = pricetobeconverted * 100000
            print(price)
        elif priceunit == "Lakhs":
            price = pricetobeconverted * 100000
            print(price)
        elif priceunit == "Lac":
            price = pricetobeconverted * 100000
            print(price)
        elif priceunit == "K":
            price = pricetobeconverted * 1000
            print(price)

        util = Utility()
        finalWordOfCurrency = str(util.num2words(decimal.Decimal(str(price))))
        print(finalWordOfCurrency)
    except:
        finalWordOfCurrency = "Unable To Convert"
        print(finalWordOfCurrency)

    facs = models.Property.objects.all().filter(IsVisible= True, PropertyID=propid)
    allStates = models.States.objects.all()
    allproptypes = models.PropertyTypeRef.objects.all()
    return render(request, "property.html", {"allimages":photosoftheproperty, "facs": facs, "propertydetails" : propertydetails, "state": allStates, "allproptypes": allproptypes, "priceword" : finalWordOfCurrency})



def individualblog(request):
    blogid = request.GET["blogid"]
    blogdetails = models.Blog.objects.all().filter(url=blogid)
    return render(request, "individualBlog.html", {"blog" : blogdetails})


def getsingleprop(request):
    propid = request.GET["prop"]
    print("Got Request")
    data = serializers.serialize('json', models.Property.objects.all().filter(IsVisible= True, PropertyID = propid))
    print(data)
    print(request.accepts('application/json'))
    return HttpResponse(data, content_type="application/json")
    return JsonResponse(data, safe=False)


def areasBasedOnLocationRef(request):
    locid = request.GET["locid"]
    print(locid)
    data = list(models.Area.objects.values_list("AreaName", flat=True).filter(LocationID = locid))

    return JsonResponse({"data": data}, safe=False)


def interior(request):
    return render(request, "interior.html")

def finance(request):
    return render(request, "finance.html")

def property_consultant(request):
    return render(request, "property_consultant.html")


def allpropertypage(request):
    allStates = models.States.objects.all()
    locationData = models.LocationsRef.objects.all()
    city = models.Cities.objects.all()
    properties = models.Property.objects.all().filter(IsVisible=True)
    feedbacks = models.Feedback.objects.all()
    propinjson = serializers.serialize('json', models.Property.objects.all().filter(IsVisible=True))
    return render(request, "allpropview.html", {"title" : "MaaShakti Property - Welcome", "state": allStates, "location" : locationData, "city": city, "property":properties, "propinjson": propinjson, "feedbacks" : feedbacks})


def forgotpass(request):
    try:
        subject = 'Forgot Pass MAASHAKTI'
        htmlmessage = '<small>Hi,\n<br>Your username and password for administration is<br>\n<b>Username: maashakti</b><br>\n<b>Password: shakti@12345</b>\n<br>Do not share this information with anyone. In case of an enquiry contact us.\n\n<br>Thank You</small>'
        normalmessage = '<small>Hi,\nYour username and password for administration is\n<b>Username: maashakti</b>\nPassword: shakti@12345\nDo not share this information with anyone. In case of an enquiry contact us.\n\nThank You</small>'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = settings.SEND_TO_EMAIL
        message = strip_tags(normalmessage)
        send_mail( subject, message, email_from, recipient_list, html_message=htmlmessage )
        return redirect('thanks')
    except:
        print("Email sending failed...")
        return HttpResponse("Error sending information. Please contact the site admin.")



def newpagefunc(request):
    return render(request, "newpage.html", {})