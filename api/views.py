from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import Companys
from django.core.exceptions import ObjectDoesNotExist
import json
import random

# Create your views here.
def index(request):
    #menu = get_object_or_404(Companys, company='McDonalds', state='CA')
    #jsonData = menu.data
    return JsonResponse({})

def getMenuForFrontEnd(request, companyRequested, stateRequested):
    menu = get_object_or_404(Companys, company=companyRequested, state=stateRequested)
    jsonData = menu.data
    return JsonResponse(jsonData)

"""https://stackoverflow.com/questions/150505/capturing-url-parameters-in-request-get
if I want to change the request to a get instead of a post someday,
csrf exempt for now until we have forms to put cookie tokens in """
@csrf_exempt
def getUserInput(request):
    """request.POST.get() is only for form-encoded data. If you are posting JSON,
    then you should use request.body instead.
     https://stackoverflow.com/questions/49430161/how-do-i-post-to-django-using-axios"""
    jsonData = request.body
    if jsonData is None:
        return HttpResponse("json data not received successfully or no data was sent")
    jsonDictionary = json.loads(jsonData)  #convert json to python dictionary
    return generateRandomOrders(jsonDictionary)

def generateRandomOrders(userInput):
    companyRequested = userInput["company"]
    stateRequested = userInput["state"]
    amountRequested = userInput["amount"]
    menu = getMenuFromDatabase(companyRequested, stateRequested)
    if menu is not None:
        menuDictionary = menu.data
        totalNumberOfItemsInMenu = len(menuDictionary) + sum(len(v) for v in menuDictionary.keys())
        #abitrary number of times to loop
        breakWhileLoop = (amountRequested + totalNumberOfItemsInMenu) / 2
        total = 0
        iterations = 0
        randomOrder = {}
        while iterations <= breakWhileLoop:
            randomMenuItem = pickRandomMenuItem(menuDictionary)
            randomMenuItemName = randomMenuItem['name']
            randomMenuItemPrice = randomMenuItem['price']
            if (total + randomMenuItemPrice <= amountRequested):
                #check to see if menu item is already in the dictionary
                if (randomMenuItemName in randomOrder):
                    incrementCount = randomOrder[randomMenuItemName]['count'] + 1
                    randomOrder[randomMenuItemName] = { 'price' : randomMenuItemPrice, 'count' : incrementCount }
                else:
                    randomOrder[randomMenuItemName] = { 'price' : randomMenuItemPrice, 'count' : 1 }
                total = total + randomMenuItemPrice
            iterations += 1

        #checks if items were put into the random order, otherwise send back empty = true flag to denote empty random order
        if len(randomOrder) > 0:
            randomOrder['total'] = { 'price' : round(total, 2) }
        else:
            randomOrder['empty'] = True

        return JsonResponse(randomOrder)
    else:
        return HttpResponse("error in generating orders, could not find specified restaurant/state")

#later on implement getting from server cache before fetching from database
def getMenuFromDatabase(companyRequested, stateRequested):
    try:
        menu = Companys.objects.get(company=companyRequested, state=stateRequested)
        return menu
    except ObjectDoesNotExist:
        print("Company and/or State does not exist")
        return null

def pickRandomMenuItem(menu):
    randomMenuType = random.choice(list(menu.keys()))
    menuItems = menu[randomMenuType]
    randomMenuItem = random.choice(menuItems)
    return randomMenuItem
