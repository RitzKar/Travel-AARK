import tkinter
import tkinter.ttk
import tkcalendar
import requests
import json
import urllib.parse
from google import genai
import pydantic
import enum
import string

# load Gemini GenAI client
def getGenAIClient():
    gemini_api_key_file=open('gemini_api_key.txt', 'r')
    gemini_api_key=gemini_api_key_file.read().strip()
    globals()["genAIClient"] = genai.Client(api_key=gemini_api_key)

# load Google Maps API key
def loadGoogleMapsAPIKey():
    google_maps_api_key_file=open('google_maps_api_key.txt', 'r')
    globals()["google_maps_api_key"]=google_maps_api_key_file.read().strip()


def loadTravelDatesFrame():
    global travelDatesFrame

    travelDatesLabel= tkinter.Label(travelDatesFrame, text='Travel Dates:', font=('Arial', 14))
    travelDatesLabel.pack(side='top', fill='both', expand=True)

    startDateFrame = tkinter.Frame(travelDatesFrame)
    startDateFrame.pack(side='top', fill='both', expand=True)

    endDateFrame = tkinter.Frame(travelDatesFrame)
    endDateFrame.pack(side='top', fill='both', expand=True)

    nodFrame = tkinter.Frame(travelDatesFrame)
    nodFrame.pack(side='top', fill='both', expand=True)

    # start date frame
    startDateLabel = tkinter.Label(startDateFrame, text='Start Date:', font=('Arial', 12))
    startDateLabel.pack(side='left', fill='both', expand=True)

    globals()["startDateEntry"] = tkcalendar.DateEntry(startDateFrame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    startDateEntry.pack(side='right', fill='none', expand=True)

    # end date frame
    endDateLabel = tkinter.Label(endDateFrame, text='End Date:', font=('Arial', 12))
    endDateLabel.pack(side='left', fill='both', expand=True)

    globals()["endDateEntry"] = tkcalendar.DateEntry(endDateFrame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    endDateEntry.bind("<<DateEntrySelected>>", lambda event: nodEntry.delete(0, tkinter.END) or nodEntry.insert(0, endDateEntry.get_date() - startDateEntry.get_date()))
    endDateEntry.pack(side='right', fill='none', expand=True)

    # number of days frame
    nodLabel = tkinter.Label(nodFrame, text='Number of Days:', font=('Arial', 12))
    nodLabel.pack(side='left', fill='both', expand=True)

    globals()["nodEntry"] = tkinter.Entry(nodFrame, width=8, font=('Arial', 10))
    nodEntry.pack(side='right', fill='none', expand=True)


def loadPassengersFrame():
    global passengersFrame

    passengersLabel= tkinter.Label(passengersFrame, text='Passengers:', font=('Arial', 14))
    passengersLabel.pack(side='top', fill='both', expand=True)

    adultsFrame = tkinter.Frame(passengersFrame)
    adultsFrame.pack(side='top', fill='both', expand=True)

    childrenFrame = tkinter.Frame(passengersFrame)
    childrenFrame.pack(side='top', fill='both', expand=True)

    seniorsFrame = tkinter.Frame(passengersFrame)
    seniorsFrame.pack(side='top', fill='both', expand=True)

    # adult passengers frame
    adultsLabel = tkinter.Label(passengersFrame, text='Adults:', font=('Arial', 12))
    adultsLabel.pack(side='left', fill='both', expand=True)

    globals()["adultsEntry"] = tkinter.Entry(passengersFrame, width=8, font=('Arial', 10))
    adultsEntry.pack(side='right', fill='none', expand=True)

    # children passengers frame
    childrenLabel = tkinter.Label(childrenFrame, text='Children (<12 years):', font=('Arial', 12))
    childrenLabel.pack(side='left', fill='both', expand=True)

    globals()["childrenEntry"] = tkinter.Entry(childrenFrame, width=8, font=('Arial', 10))
    childrenEntry.pack(side='right', fill='none', expand=True)

    # senior passengers frame
    seniorsLabel = tkinter.Label(seniorsFrame, text='Seniors (60+ years):', font=('Arial', 12))
    seniorsLabel.pack(side='left', fill='both', expand=True)

    globals()["seniorsEntry"] = tkinter.Entry(seniorsFrame, width=8, font=('Arial', 10))
    seniorsEntry.pack(side='right', fill='none', expand=True)


def loadCostsFrame():
    global costsFrame

    costsLabel = tkinter.Label(costsFrame, text='Costs:', font=('Arial', 14))
    costsLabel.pack(side='top', fill='both', expand=True)

    globals()["travel_costs"] = tkinter.StringVar(costsFrame, "Standard")

    for cost_types in ["Budget", "Standard", "Luxury"]:
        tkinter.Radiobutton(costsFrame, text=cost_types, variable=travel_costs, value=cost_types).pack(side='top', fill='both', expand=True)


def loadTopFrame():
    global topFrame

    globals()["travelDatesFrame"] = tkinter.Frame(topFrame)
    travelDatesFrame.pack(side='left', fill='both', expand='true')

    lineCanvas3= tkinter.Canvas(topFrame, width=10, height=100)
    lineCanvas3.pack(side='left', fill='both', expand=True)
    lineCanvas3.create_line(5, 0, 5, 500, fill='black')

    globals()["passengersFrame"] = tkinter.Frame(topFrame)
    passengersFrame.pack(side='left', fill='both', expand='true')

    lineCanvas4= tkinter.Canvas(topFrame, width=10, height=100)
    lineCanvas4.pack(side='left', fill='both', expand=True)
    lineCanvas4.create_line(5, 0, 5, 500, fill='black')

    globals()["costsFrame"] = tkinter.Frame(topFrame)
    costsFrame.pack(sid='left', fill='both', expand='true')

    loadTravelDatesFrame()
    loadPassengersFrame()
    loadCostsFrame()


def loadDestinationSection():
    global destinationFrame
    destinationLabel = tkinter.Label(destinationFrame, text='Destination (city / country / region):', font=('Arial', 14))
    destinationLabel.pack(side='top', fill='both', expand=True)

    globals()["destinationEntry"] = tkinter.Entry(destinationFrame, width=30, font=('Arial', 12))
    destinationEntry.pack(side='top', fill='x', expand=True, padx=10)



def loadInterestsSection():
    global interestsFrame

    interestsLabel = tkinter.Label(interestsFrame, text='Interests:', font=('Arial', 14))
    interestsLabel.pack(side='top', fill='both', expand=True)

    globals()["travel_interests"] = []
    kids_interest=tkinter.IntVar()
    adventure_interest=tkinter.IntVar()
    summer_interest=tkinter.IntVar()
    beach_interest=tkinter.IntVar()
    skiing_interest=tkinter.IntVar()
    history_interest=tkinter.IntVar()
    hiking_interest=tkinter.IntVar()
    romance_interest=tkinter.IntVar()
    party_interest=tkinter.IntVar()

    # define function to collect interests
    def collectInterests():
        global travel_interests

        travel_interests.clear()
        if kids_interest.get() == 1:
            travel_interests.append('Kids')
        if beach_interest.get() == 1:
            travel_interests.append('Beach')
        if skiing_interest.get() == 1:
            travel_interests.append('Skiing')
        if history_interest.get() == 1:
            travel_interests.append('History')
        if romance_interest.get() == 1:
            travel_interests.append('Romance')
        if party_interest.get() == 1:
            travel_interests.append('Party')
        print("Selected interests:", travel_interests)

    kidsInterestCheckbutton = tkinter.Checkbutton(interestsFrame, text='Kids', variable=kids_interest, onvalue=1, offvalue=0, font=('Arial', 12), command=collectInterests)
    kidsInterestCheckbutton.pack(side='left', fill='both', expand=True)
    beachInterestCheckbutton = tkinter.Checkbutton(interestsFrame, text='Beach', variable=beach_interest, onvalue=1, offvalue=0, font=('Arial', 12), command=collectInterests)
    beachInterestCheckbutton.pack(side='left', fill='both', expand=True)
    skiingInterestCheckbutton = tkinter.Checkbutton(interestsFrame, text='Skiing', variable=skiing_interest, onvalue=1, offvalue=0, font=('Arial', 12), command=collectInterests)
    skiingInterestCheckbutton.pack(side='left', fill='both', expand=True)

    historyInterestCheckbutton = tkinter.Checkbutton(interestsFrame, text='History', variable=history_interest, onvalue=1, offvalue=0, font=('Arial', 12), command=collectInterests)
    historyInterestCheckbutton.pack(side='left', fill='both', expand=True)
    romanceInterestCheckbutton = tkinter.Checkbutton(interestsFrame, text='Romance', variable=romance_interest, onvalue=1, offvalue=0, font=('Arial', 12), command=collectInterests)
    romanceInterestCheckbutton.pack(side='left', fill='both', expand=True)
    partyInterestCheckbutton = tkinter.Checkbutton(interestsFrame, text='Party', variable=party_interest, onvalue=1, offvalue=0, font=('Arial', 12), command=collectInterests)
    partyInterestCheckbutton.pack(side='left', fill='both', expand=True)

    


def loadMiddleFrame():
    global midFrame

    globals()["destinationFrame"] = tkinter.Frame(midFrame)
    destinationFrame.pack(side='left', fill='both', expand=True)

    lineCanvas5= tkinter.Canvas(midFrame, width=10, height=100)
    lineCanvas5.pack(side='left', fill='both', expand=True)
    lineCanvas5.create_line(5, 0, 5, 500, fill='black')

    globals()["interestsFrame"] = tkinter.Frame(midFrame)
    interestsFrame.pack(side='left', fill='both', expand=True)

    loadDestinationSection()
    loadInterestsSection()


class City(pydantic.BaseModel):
    rank: str
    city: str
    country: str
    interests: list[str]

def populateCitiesListBox():
    global destination, citiesListBox, genAIClient, travel_interests, start_date, end_date

    if destination:
        citiesListBox.delete(0, tkinter.END)  # clear the listbox
        top10cities_query=f"List the top 10 cities for tourism in {destination}"
        top10cities_query=f"{top10cities_query} for interests in {travel_interests}"
        top10cities_query=f"{top10cities_query} during the period between {start_date} and {end_date}"
        
        top10cities_response = genAIClient.models.generate_content(
            model="gemini-2.5-flash",
            contents=top10cities_query,
            config={
    	        "response_mime_type": "application/json",
                "response_schema": list[City]
            }
        )
        globals()["top10cities"] = json.loads(top10cities_response.text)
        print("Top 10 cities response:", top10cities)

        for city_entry in top10cities:
            # print(city_entry['city'])
            citiesListBox.insert(tkinter.END, f"{city_entry['rank']}. {city_entry['city']} ({city_entry['country']})")



def loadDestinationDetails():
    # collect all the data from the screen
    global startDateEntry, endDateEntry, adultsEntry, childrenEntry, seniorsEntry, destinationEntry, budgetEntry, nodEntry

    globals()["start_date"] = startDateEntry.get_date()
    globals()["end_date"] = endDateEntry.get_date()    
    globals()["destination"] = destinationEntry.get()
    globals()["travel_budget"] = travel_costs.get()

    # print the collected data
    print("Start Date:", start_date)
    print("End Date:", end_date)    
    print("Destination:", destination)    
    print("Interests:", travel_interests)

    populateCitiesListBox()
    loadDestinationMap()

def loadMapSelectedCities():
    global top10cities, citiesListBox, google_maps_api_key, destination, mapImageLabel

    # cities_list = [citiesListBox.get(i) for i in citiesListBox.curselection()]
    globals()["selected_cities"]=[]

    google_maps_api_url = f"https://maps.googleapis.com/maps/api/staticmap?"
    map_markers=[]

    for city_entry in [citiesListBox.get(i) for i in citiesListBox.curselection()]:
        city_entry_num = city_entry.split('.')[0]
        city_name=top10cities[int(city_entry_num)-1]['city']
        country_name=top10cities[int(city_entry_num)-1]['country']

        selected_cities.append({'rank': city_entry_num, 'city': city_name, 'country': country_name})

        map_markers.append(f"markers=color:blue%7Clabel:{city_entry_num}%7C{urllib.parse.quote_plus(city_name)}%2C{urllib.parse.quote_plus(country_name)}")


    if map_markers == []:
        map_markers=urllib.parse.quote_plus(destination)
        map_markers_str=f"markers={map_markers}"
    else:
        map_markers_str= '&'.join(map_markers)
    print("Map markers:", map_markers_str)
     
    google_maps_api_url= f"{google_maps_api_url}{map_markers_str}&size=1000x500&key={google_maps_api_key}"
    # print("Google Maps API URL:", google_maps_api_url)
    mapImageFile=open('selected_cities_map.png', 'wb')
    map_response=requests.get(google_maps_api_url)

    if map_response.status_code == 200:
        mapImageFile.write(map_response.content)
        mapImageFile.close()
        print("Map generated successfully!")

        googleMapSelectedCitiesImage= tkinter.PhotoImage(file='selected_cities_map.png')
        mapImageLabel.config(image=googleMapSelectedCitiesImage)
        mapImageLabel.image=googleMapSelectedCitiesImage
    else:
        print("Failed to generate map:", map_response.status_code)



def loadCitiesListSection():
    global citiesListFrame

    citiesLabel= tkinter.Label(citiesListFrame, text='Cities:', font=('Arial', 14))
    citiesLabel.pack(side='top', fill='both', expand=True)

    citiesListboxScrollbar= tkinter.Scrollbar(citiesListFrame)
    citiesListboxScrollbar.pack(side='right', fill='y')

    globals()["citiesListBox"]= tkinter.Listbox(citiesListFrame, width=30, height=10, font=('Arial', 12), yscrollcommand=citiesListboxScrollbar.set, selectmode="multiple")
    citiesListBox.pack(side='left', fill='both', expand=True)

    citiesListboxScrollbar.config(command=citiesListBox.yview)

    citiesListBox.bind('<<ListboxSelect>>', lambda event: loadMapSelectedCities())

    loadButton= tkinter.Button(destinationFrame, text='Load', font=('Arial', 16), command=lambda: loadDestinationDetails())
    loadButton.pack(side='top', fill='none', expand=False)


def getCurrentLocation():
    global google_maps_api_key

    # get location in latitude and longitude format
    google_maps_api_url= f"https://www.googleapis.com/geolocation/v1/geolocate?key={google_maps_api_key}"
    location_response = requests.post(google_maps_api_url)

    if location_response.status_code == 200:
        # print("Location response:", location_response.text)
        current_location = json.loads(location_response.text)

        # use the latitude and longitude to get the detailed location
        google_maps_api_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={current_location['location']['lat']},{current_location['location']['lng']}&key={google_maps_api_key}&result_type=political%7Clocality"
        detailed_location_response= requests.get(google_maps_api_url)
        if detailed_location_response.status_code == 200:
            detailed_current_location = json.loads(detailed_location_response.text)
            if detailed_current_location:
                # print("Detailed Current location:", json.dumps(detailed_current_location,indent=2))

                # using the detailed location, find the city (usually "types": ["locality","political"]) and the country (usually "types": ["country","political"])
                for address_component in detailed_current_location['results'][0]['address_components']:
                    if "locality" in address_component['types'] and "political" in address_component['types']:
                        globals()["current_city_name"] = address_component['long_name']
                    elif "country" in address_component['types'] and "political" in address_component['types']:
                        globals()["current_country_name"] = address_component['long_name']

                print(f"Current city: {current_city_name}, {current_country_name}")
            else:
                print("No address found for the current location.")
        else:
            print("Failed to get detailed location:", detailed_location_response.status_code)
    else:
        print("Failed to get current location:", location_response.status_code)


def loadCurrentLocationMap():
    global mapFrame, current_city_name, current_country_name, google_maps_api_key, mapImageLabel
    
    google_maps_api_url = f"https://maps.googleapis.com/maps/api/staticmap?"
    current_location=urllib.parse.quote_plus(f"{current_city_name},{current_country_name}")  # URL encode the current location

    # map_marker = f"markers=color:blue%7Clabel:{map_destination}%7C{map_destination}"
    map_marker = f"markers={current_location}"

    google_maps_api_url= f"{google_maps_api_url}{map_marker}&size=600x600&key={google_maps_api_key}"
    print("Google Maps API URL for current location:", google_maps_api_url)

    mapImageFile=open('current_location_map.png', 'wb')
    map_response=requests.get(google_maps_api_url)

    if map_response.status_code == 200:
        mapImageFile.write(map_response.content)
        mapImageFile.close()
        print("Map for Current location generated successfully!")

        googleMapCLImage= tkinter.PhotoImage(file="current_location_map.png")
        mapImageLabel.config(image=googleMapCLImage)
        mapImageLabel.image=googleMapCLImage
        # mapImageLabel.pack(side='top', fill='both', expand=True)
    else:
        print("Failed to generate map for current location:", map_response.status_code)

def loadDestinationMap():
    global mapFrame, destination, google_maps_api_key, mapImageLabel
    
    google_maps_api_url = f"https://maps.googleapis.com/maps/api/staticmap?"
    urle_destination=urllib.parse.quote_plus(destination)  # URL encode the destination

    # map_marker = f"markers=color:blue%7Clabel:{map_destination}%7C{map_destination}"
    map_marker = f"markers={urle_destination}"

    google_maps_api_url= f"{google_maps_api_url}{map_marker}&size=600x600&key={google_maps_api_key}"
    print("Google Maps API URL for destination:", google_maps_api_url)

    mapImageFile=open('destination_map.png', 'wb')
    map_response=requests.get(google_maps_api_url)

    if map_response.status_code == 200:
        mapImageFile.write(map_response.content)
        mapImageFile.close()
        print("Map for Destination generated successfully!")

        googleMapDestImage= tkinter.PhotoImage(file='destination_map.png')
        mapImageLabel.image=googleMapDestImage
        mapImageLabel.config(image=googleMapDestImage)
    else:
        print("Failed to generate map for Destination:", map_response.status_code)


def loadMapSection():
    global mapFrame

    # mapLabel = tkinter.Label(mapFrame, text='Map:', font=('Arial', 16))
    # mapLabel.pack(side='top', fill='both', expand=True)
    # Here you would load the actual map, for now we just use a placeholder

    globals()["mapImageLabel"]= tkinter.Label(mapFrame)
    mapImageLabel.pack(side='top', fill='both', expand=True)

    getCurrentLocation()
    loadCurrentLocationMap()



def loadBottomFrame():
    # globals()["bottomFrame"]= tkinter.Frame(aitFrame, background="yellow")
    global bottomFrame

    globals()["citiesListFrame"] = tkinter.Frame(bottomFrame)
    citiesListFrame.pack(side='left', fill='none', expand=True)

    lineCanvas6= tkinter.Canvas(bottomFrame, width=10, height=600)
    lineCanvas6.pack(side='left', fill='both', expand=True)
    lineCanvas6.create_line(5, 0, 5, 600, fill='black')

    globals()["mapFrame"] = tkinter.Frame(bottomFrame)
    mapFrame.pack(side='left', fill='both', expand=True)

    loadCitiesListSection()
    loadMapSection()


    
def loadAITineraryFrame():
    global aitScreen

    globals()["aitFrame"] = tkinter.Frame(aitScreen)
    aitFrame.pack(side='top', fill='both', expand=True)

    globals()["topFrame"]= tkinter.Frame(aitFrame)
    topFrame.pack(side='top', fill='both', expand=True)

    lineCanvas1= tkinter.Canvas(aitFrame, width=1200, height=10)
    lineCanvas1.pack(side='top', fill='both', expand=True)
    lineCanvas1.create_line(0, 5, 1200, 5, fill='black')

    globals()["midFrame"]= tkinter.Frame(aitFrame)
    midFrame.pack(side='top', fill='both', expand=True)

    lineCanvas2= tkinter.Canvas(aitFrame, width=1200, height=10)
    lineCanvas2.pack(side='top', fill='both', expand=True)
    lineCanvas2.create_line(0, 5, 1200, 5, fill='black')

    globals()["bottomFrame"]= tkinter.Frame(aitFrame)
    bottomFrame.pack(side='top', fill='both', expand=True)

    lineCanvas7= tkinter.Canvas(aitFrame, width=1200, height=10)
    lineCanvas7.pack(side='top', fill='both', expand=True)
    lineCanvas7.create_line(0, 5, 1200, 5, fill='black')

    nextButton= tkinter.Button(aitFrame, text='Next >>', font=('Arial', 16), command=lambda: gotoTravelPlanScreen())
    nextButton.pack(side='top', fill='none', expand=False)

    loadTopFrame()
    loadMiddleFrame()
    loadBottomFrame()

def loadAITineraryScreen():
    globals()["aitScreen"] = tkinter.Tk(screenName='AITineraryScreen',baseName='AITineraryBase',className='AITineraryClass',useTk=1)
    aitScreen.title('AITinerary')

    loadAITineraryFrame()

    aitScreen.mainloop()

##################################################################################################################################
# everything related to Travel Plan Screen below
##################################################################################################################################

def gotoTravelPlanScreen():
    # collect all the data from the screen (again)
    global startDateEntry, endDateEntry, adultsEntry, childrenEntry, seniorsEntry, destinationEntry, nodEntry, travel_costs, travel_interests, selected_cities

    globals()["start_date"] = startDateEntry.get_date()
    globals()["end_date"] = endDateEntry.get_date()
    globals()["nod"] = nodEntry.get()
    globals()["adults"] = adultsEntry.get()
    globals()["children"] = childrenEntry.get()
    globals()["seniors"] = seniorsEntry.get()
    globals()["destination"] = destinationEntry.get()
    globals()["travel_budget"] = travel_costs.get()

    # print the collected data
    print("Start Date:", start_date)
    print("End Date:", end_date)
    print("Number of Days:", nod)
    print("Adults:", adults)
    print("Children:", children)
    print("Seniors:", seniors)
    print("Destination:", destination)
    print("Interests:", travel_interests)
    print("Travel Costs:", travel_budget)
    print("Selected Cities: ", selected_cities)

    print("Going to the next window (Travel Plan Screen)...")

    loadTravelPlanScreen()

class transportation(str, enum.Enum):
    BUS = "Bus"
    TRAIN = "Train"
    FLIGHT = "Flight"
    CAR = "Car"
    FERRY = "Ferry"

class detailed_travel_day(pydantic.BaseModel):
    travel_date: str
    start_city: str
    start_country: str
    end_city: str
    end_country: str
    mode_of_transport: transportation
    transport_operating_company: str
    transport_number: str
    transport_cost: str
    start_time: str
    end_time: str
    travel_time: str

def createDetailedTravelPlan():
    global selected_cities, genAIClient, current_city_name, current_country_name, start_date, end_date, travel_budget

    print("Selected cities for travel plan:", selected_cities)

    if travel_budget == "Budget":
        detailed_travel_itinerary_query=f"Create a travel plan for {selected_cities} with least costs"
    elif travel_budget == "Standard":
        detailed_travel_itinerary_query=f"Create a travel plan for {selected_cities} with reasonable costs and travel time"
    elif travel_budget == "Luxury":
        detailed_travel_itinerary_query=f"Create a travel plan for {selected_cities} with best travel time and comfort"

    detailed_travel_itinerary_query=f"{detailed_travel_itinerary_query} starting on {start_date} at {current_city_name}, {current_country_name}"
    detailed_travel_itinerary_query=f"{detailed_travel_itinerary_query} ending on {end_date} at {current_city_name}, {current_country_name}"
    detailed_travel_itinerary_query=f"{detailed_travel_itinerary_query} including the recommended number of stays at each city"
    detailed_travel_itinerary_query=f"{detailed_travel_itinerary_query} travelling with {adults} adults, {children} children and {seniors} seniors"
    detailed_travel_itinerary_response = genAIClient.models.generate_content(
        model="gemini-2.5-flash",
        contents=detailed_travel_itinerary_query,
        config={
    	    "response_mime_type": "application/json",
            "response_schema": list[detailed_travel_day]
        }
    )
    globals()["detailed_travel_itinerary"] = json.loads(detailed_travel_itinerary_response.text)
    print("Detailed Travel Itinerary response:", detailed_travel_itinerary)


# def loadTravelPlanMap():
#     global travelPlanFrame, google_maps_api_key, selected_cities, current_city_name, current_country_name, detailed_travel_itinerary

#     google_maps_api_url = f"https://maps.googleapis.com/maps/api/staticmap?"

#     # create the API URL suffix for the paths
#     map_paths = []
#     # create the API URL suffix for the location markers
#     map_markers =[]
#     city_counter=0

#     # First add the current location
#     map_paths.append(f"{current_city_name},{current_country_name}")
#     map_markers.append(f"markers=color:blue%7Clabel:{list(string.ascii_uppercase)[city_counter]}%7C{urllib.parse.quote_plus(current_city_name)}%2C{urllib.parse.quote_plus(current_country_name)}")
#     city_counter+=1

#     for travel_days in detailed_travel_itinerary:
#         map_paths.append(f"{travel_days['end_city']},{travel_days['end_country']}")
#         map_markers.append(f"markers=color:blue%7Clabel:{list(string.ascii_uppercase)[city_counter]}%7C{urllib.parse.quote_plus(travel_days['end_city'])}%2C{urllib.parse.quote_plus(travel_days['end_country'])}")
#         city_counter+=1
        
#     map_paths_str= '|'.join(map_paths)
#     map_markers_str = '&'.join(map_markers)

#     google_maps_api_url= f"{google_maps_api_url}{map_markers_str}&path=color:blue%7Cweight:5%7C{urllib.parse.quote_plus(map_paths_str)}&size=600x600&key={google_maps_api_key}"

#     print("Google Maps Path & Marker URL: ", google_maps_api_url)
    

#     mapImageFile=open('travel_plan_map.png', 'wb')
#     map_response=requests.get(google_maps_api_url)

#     if map_response.status_code == 200:
#         mapImageFile.write(map_response.content)
#         mapImageFile.close()
#         print("Map generated successfully!")

#         travelPlanMapImage= tkinter.PhotoImage(file='travel_plan_map.png')
#         globals()["travelPlanMapLabel"]= tkinter.Label(travelPlanFrame, image=travelPlanMapImage)
#         travelPlanMapLabel.pack(side='top', fill='both', expand=True)
#     else:
#         print("Failed to generate map:", map_response.status_code)


def showTravelDetails():
    global itineraryTable, detailed_travel_itinerary, mode_of_transport

    print("Selected travel day:", itineraryTable.selection())
    print("Selected row ID:", itineraryTable.index(itineraryTable.selection()))

    index_itable=itineraryTable.index(itineraryTable.selection())
    # the below command should update the Radiobuttons in the transport mode section
    mode_of_transport.set(detailed_travel_itinerary[index_itable]['mode_of_transport'])

    print("Selected mode of transport:", mode_of_transport.get())

    loadTravelDayMap()
    loadTransportOptions()


def loadItinerary():
    global itineraryFrame

    globals()["itineraryTable"]=tkinter.ttk.Treeview(itineraryFrame, columns=('Date', 'Start City', 'End City'), show='headings', selectmode='browse')
    itineraryTable.heading('Date', text='Date')
    itineraryTable.heading('Start City', text='Start City')
    itineraryTable.heading('End City', text='End City')
    itineraryTable.pack(side='top', fill='none', expand=False)

    for travel_day in detailed_travel_itinerary:
        itineraryTable.insert('', 'end', values=(travel_day['travel_date'], f"{travel_day['start_city']}, {travel_day['start_country']}", f"{travel_day['end_city']}, {travel_day['end_country']}"))

    # Select the first row by default
    itineraryTable.selection_set(itineraryTable.get_children()[0])  # Focus on the first entry

    # itineraryTable.bind('<<TreeviewSelect>>', lambda: showTravelDetails())
    itineraryTable.bind('<<TreeviewSelect>>', lambda event: showTravelDetails())


def loadTransportMode():
    global transportModeFrame, detailed_travel_itinerary

    globals()["transportModeLabel"] = tkinter.Label(transportModeFrame, text='Mode of Transport:', font=('Arial', 14))
    transportModeLabel.pack(side='top', fill='both', expand=True)

    # mode of transport already chosen by AI
    index_itable=itineraryTable.index(itineraryTable.selection())
    globals()["mode_of_transport"] = tkinter.StringVar(transportModeFrame, detailed_travel_itinerary[index_itable]['mode_of_transport'])
    for transport_mode in transportation:
        # print("Transport mode: ", transport_mode.value)
        tkinter.Radiobutton(transportModeFrame, text=transport_mode.value, variable=mode_of_transport, value=transport_mode.value, command=loadTransportOptions).pack(side='top', fill='both', expand=True)


# def updateTransportMode():
#     global mode_of_transport

#     print("Selected mode of transport:", mode_of_transport.get())


    
def loadTPTopLeftFrame():
    global tpTopLeftFrame

    globals()["itineraryFrame"] = tkinter.Frame(tpTopLeftFrame)
    itineraryFrame.pack(side='top', fill='both', expand=True)

    lineCanvas1= tkinter.Canvas(tpTopLeftFrame, width=200, height=10)
    lineCanvas1.pack(side='top', fill='both', expand=True)
    lineCanvas1.create_line(0, 5, 1200, 5, fill='black')

    globals()["transportModeFrame"] = tkinter.Frame(tpTopLeftFrame)
    transportModeFrame.pack(side='top', fill='both', expand=True)

    # globals()["updateTransportButton"] = tkinter.Button(tpTopLeftFrame, text='Update Transport Mode', font=('Arial', 14), command=updateTransportMode)
    # updateTransportButton.pack(side='top', fill='none', expand=False)

    loadItinerary()
    loadTransportMode()


class travel_options(pydantic.BaseModel):
    transport_operating_company: str
    transport_number: str
    transport_cost: str
    start_time: str
    end_time: str
    travel_time: str


def loadTransportOptions():
    global transportOptionsFrame, detailed_travel_itinerary, itineraryTable, adults, children, seniors, mode_of_transport

    index_itable=itineraryTable.index(itineraryTable.selection())
    start_date= detailed_travel_itinerary[index_itable]['travel_date']
    start_city= f"{detailed_travel_itinerary[index_itable]['start_city']},{detailed_travel_itinerary[index_itable]['start_country']}"
    end_city=f"{detailed_travel_itinerary[index_itable]['end_city']},{detailed_travel_itinerary[index_itable]['end_country']}"
    transport_mode= mode_of_transport.get()

    transport_options_query=f"List the available transport options from {start_city} to {end_city}"
    transport_options_query=f"{transport_options_query} on {start_date} by {transport_mode} with the best costs and travel time"
    transport_options_query=f"{transport_options_query} travelling with {adults} adults, {children} children and {seniors} seniors"

    transport_options_response= genAIClient.models.generate_content(
        model="gemini-2.5-flash",
        contents=transport_options_query,
        config={
            "response_mime_type": "application/json",
            "response_schema": list[travel_options]
        }
    )
    globals()["transport_options"] = json.loads(transport_options_response.text)
    print("Transport Options response:", transport_options)

    # clear the transport options table
    transportOptionsTable.delete(*transportOptionsTable.get_children())
    for toption in transport_options:
        transportOptionsTable.insert('', 'end', values=(toption['transport_operating_company'], toption['transport_number'], toption['transport_cost'], toption['start_time'], toption['end_time'], toption['travel_time']))


def loadTransportOptionsFrame():
    global transportOptionsFrame

    globals()["transportOptionsLabel"] = tkinter.Label(transportOptionsFrame, text='Transport Options:', font=('Arial', 14))
    transportOptionsLabel.pack(side='top', fill='both', expand=True)

    globals()["transportOptionsTable"] = tkinter.ttk.Treeview(transportOptionsFrame, columns=('Company', 'Number', 'Cost', 'Start Time', 'End Time', 'Travel Time'), show='headings', selectmode='browse')
    transportOptionsTable.heading('Company', text='Company')
    transportOptionsTable.heading('Number', text='Number')
    transportOptionsTable.heading('Cost', text='Cost')
    transportOptionsTable.heading('Start Time', text='Start Time')
    transportOptionsTable.heading('End Time', text='End Time')
    transportOptionsTable.heading('Travel Time', text='Travel Time')
    transportOptionsTable.pack(side='top', fill='none', expand=False)

    # loadTransportOptions() -- this is to avoid loading the options twice (this is already loaded as part of initial loading of Travel Plan treeview)


def loadTravelDayMap():
    global travelDayMapLabel, detailed_travel_itinerary, itineraryTable, google_maps_api_key


    index_itable=itineraryTable.index(itineraryTable.selection())
    detailed_travel_day = detailed_travel_itinerary[index_itable]

    urlencoded_start_city=urllib.parse.quote_plus(f"{detailed_travel_day['start_city']},{detailed_travel_day['start_country']}")
    urlencoded_end_city=urllib.parse.quote_plus(f"{detailed_travel_day['end_city']},{detailed_travel_day['end_country']}")

    map_markers_str= f"markers=color:blue%7Clabel:A%7C{urlencoded_start_city}&markers=color:blue%7Clabel:B%7C{urlencoded_end_city}"
    map_path_str= f"path=color:blue%7Cweight:5%7C{urlencoded_start_city}%7C{urlencoded_end_city}"

    google_maps_api_url = f"https://maps.googleapis.com/maps/api/staticmap?{map_markers_str}&{map_path_str}&size=600x600&key={google_maps_api_key}"

    print(f"Google Maps API URL for travel day {index_itable}:", google_maps_api_url)

    mapImageFile=open('travel_day_map.png', 'wb')
    map_response=requests.get(google_maps_api_url)
    if map_response.status_code == 200:
        mapImageFile.write(map_response.content)
        mapImageFile.close()
        print("Map for travel day generated successfully!")
        travelDayMapImage= tkinter.PhotoImage(file='travel_day_map.png')
        travelDayMapLabel.config(image=travelDayMapImage)
        travelDayMapLabel.image=travelDayMapImage
    else:
        print("Failed to generate map for travel day:", map_response.status_code)


def loadTPTopRightFrame():
    global tpTopRightFrame, detailed_travel_itinerary, itineraryTable

    globals()["travelDayMapLabel"]= tkinter.Label(tpTopRightFrame)
    travelDayMapLabel.pack(side='top', fill='both', expand=True)

    # loadTravelDayMap() -- this is to avoid loading the Travel map twice (this is already loaded as part of initial loading of Travel Plan treeview)


def loadTPTopFrame():
    global tpTopFrame

    globals()["tpTopLeftFrame"] = tkinter.Frame(tpTopFrame)
    tpTopLeftFrame.pack(side='left', fill='both', expand=True)

    lineCanvas1= tkinter.Canvas(tpTopFrame, width=10, height=600)
    lineCanvas1.pack(side='left', fill='both', expand=True)
    lineCanvas1.create_line(5, 0, 5, 600, fill='black')

    globals()["tpTopRightFrame"] = tkinter.Frame(tpTopFrame)
    tpTopRightFrame.pack(side='left', fill='both', expand=True)

    loadTPTopLeftFrame()
    loadTPTopRightFrame()


def updateTravelPlan():
    global detailed_travel_itinerary, itineraryTable, transportOptionsTable, mode_of_transport

    index_itable=itineraryTable.index(itineraryTable.selection())
    selected_travel_option=transportOptionsTable.selection()[0]

    print("Selected Travel option IID: ", selected_travel_option)
    print("Selected travel option: ", transportOptionsTable.item(selected_travel_option)['values'])

    # transport_operating_company: str
    # transport_number: str
    # transport_cost: str
    # start_time: str
    # end_time: str
    # travel_time: str

    # detailed_travel_itinerary[index_itable]['transport_operating_company']=transportOptionsTable[index_transport_option_table]['Company']
    # detailed_travel_itinerary[index_itable]['transport_number']=transportOptionsTable[index_transport_option_table]['Number']
    # detailed_travel_itinerary[index_itable]['transport_cost']=transportOptionsTable[index_transport_option_table]['Cost']
    # detailed_travel_itinerary[index_itable]['start_time']=transportOptionsTable[index_transport_option_table]['Start Time']
    # detailed_travel_itinerary[index_itable]['end_time']=transportOptionsTable[index_transport_option_table]['End Time']
    # detailed_travel_itinerary[index_itable]['travel_time']=transportOptionsTable[index_transport_option_table]['Travel Time']

    detailed_travel_itinerary[index_itable]['mode_of_transport']=mode_of_transport.get()
    detailed_travel_itinerary[index_itable]['transport_operating_company']=transportOptionsTable.item(selected_travel_option)['values'][0]
    detailed_travel_itinerary[index_itable]['transport_number']=transportOptionsTable.item(selected_travel_option)['values'][1]
    detailed_travel_itinerary[index_itable]['transport_cost']=transportOptionsTable.item(selected_travel_option)['values'][2]
    detailed_travel_itinerary[index_itable]['start_time']=transportOptionsTable.item(selected_travel_option)['values'][3]
    detailed_travel_itinerary[index_itable]['end_time']=transportOptionsTable.item(selected_travel_option)['values'][4]
    detailed_travel_itinerary[index_itable]['travel_time']=transportOptionsTable.item(selected_travel_option)['values'][5]

    print("Updated Detailed Travel Itinerary: ", detailed_travel_itinerary)
    

def loadTPBottomFrame():
    global tpBottomFrame

    globals()["transportOptionsFrame"] = tkinter.Frame(tpBottomFrame)
    transportOptionsFrame.pack(side='top', fill='both', expand=True)

    # globals()["updateTPButton"] = tkinter.Button(tpBottomFrame, text='Update Travel Plan', font=('Arial', 14), command=updateTravelPlan)
    # updateTPButton.pack(side='top', fill='none', expand=False)

    # globals()["travelCostsFrame"] = tkinter.Frame(tpBottomFrame)
    # travelCostsFrame.pack(side='top', fill='both', expand=True)

    loadTransportOptionsFrame()


def loadTPButtonFrame():
    global tpButtonFrame

    globals()["reloadTOButton"] = tkinter.Button(tpButtonFrame, text='Reload Transport Options', font=('Arial', 14), command=loadTransportOptions)
    reloadTOButton.pack(side='left', fill='none', expand=False)

    globals()["updateTPButton"] = tkinter.Button(tpButtonFrame, text='Update Travel Plan', font=('Arial', 14), command=updateTravelPlan)
    updateTPButton.pack(side='bottom', fill='none', expand=False)

    globals()["nextTPButton"] = tkinter.Button(tpButtonFrame, text='Next >>', font=('Arial', 14))
    nextTPButton.pack(side='right', fill='none', expand=False)


def loadTravelPlanFrame():
    global travelPlanFrame

    globals()["tpTopFrame"] = tkinter.Frame(travelPlanFrame)
    tpTopFrame.pack(side='top', fill='both', expand=True)

    lineCanvas1= tkinter.Canvas(travelPlanFrame, width=1200, height=10)
    lineCanvas1.pack(side='top', fill='both', expand=True)
    lineCanvas1.create_line(0, 5, 1200, 5, fill='black')

    globals()["tpBottomFrame"] = tkinter.Frame(travelPlanFrame)
    tpBottomFrame.pack(side='top', fill='both', expand=True)

    globals()["tpButtonFrame"] = tkinter.Frame(travelPlanFrame)
    tpButtonFrame.pack(side='top', fill='both', expand=True)

    loadTPTopFrame()
    loadTPBottomFrame()
    loadTPButtonFrame()


def loadTravelPlanScreen():
    global aitScreen

    createDetailedTravelPlan()
    
    globals()["travelPlanScreen"]= tkinter.Toplevel(aitScreen)
    travelPlanScreen.title('AI generated Travel Plan')

    globals()["travelPlanFrame"] = tkinter.Frame(travelPlanScreen)
    travelPlanFrame.pack(side='top', fill='both', expand=True)

    loadTravelPlanFrame()

    travelPlanScreen.mainloop()


getGenAIClient()
loadGoogleMapsAPIKey()
loadAITineraryScreen()
