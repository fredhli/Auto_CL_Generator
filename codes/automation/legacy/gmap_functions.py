import re
import os
import googlemaps
from pprint import pprint
from fuzzywuzzy import fuzz

us_state_dict = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

ca_province_dict = {
    "AB": "Alberta",
    "BC": "British Columbia",
    "MB": "Manitoba",
    "NB": "New Brunswick",
    "NL": "Newfoundland and Labrador",
    "NS": "Nova Scotia",
    "NT": "Northwest Territories",
    "NU": "Nunavut",
    "ON": "Ontario",
    "PE": "Prince Edward Island",
    "QC": "Quebec",
    "SK": "Saskatchewan",
    "YT": "Yukon",
}


def get_client(gmap_api_key="AIzaSyD8SB4p5_IaHVQUPF_xtiFck-juQwmLkrE"):
    return googlemaps.Client(key=gmap_api_key)


def geolocate(city):
    client = get_client()
    geocode_result = client.geocode(city)

    location = geocode_result[0]["geometry"]["location"]

    lat = location["lat"]
    lng = location["lng"]

    return lat, lng


def nearby_search_address(city, company_name, company_country, radius=100000):
    client = get_client()
    lat, lng = geolocate(city)
    try:
        places = client.places_nearby(
            location=(lat, lng), radius=radius, name=company_name
        )
        address_line_1 = places["results"][0]["vicinity"]
        address_line_1 = address_line_1.split(",")[0]
        address_line_2 = places["results"][0]["name"]

        split_words = [
            "Suite",
            "Floor",
            "Unit",
            "Building",
            "Room",
            "Apartment",
            "Level",
            "Block",
            "Lot",
            "Shop",
            "House",
            "Number",
            "#",
        ]

        for word in split_words:
            if word in address_line_1:
                address_line_1 = address_line_1.split(word)[0].strip()
                address_line_2 = (
                    word + " " + address_line_1.split(word)[1]).strip()
                if word == "#":
                    address_line_2 = address_line_2.replace(word, "No.")
                break

        try:
            address_line_3 = places["results"][0]["plus_code"]["compound_code"]
        except KeyError:
            if company_country == "":
                assert False, "type in company country and try again"
            else:
                address_line_3 = f"{city}, {company_country}"

        address_line_3 = re.sub(r"[A-Z0-9\+]{6,} ", "", address_line_3).strip()

        similarity = fuzz.token_sort_ratio(company_name, address_line_2)
        if similarity <= 60:
            assert False, "Low similarity"

        try:
            results = address_line_3.split(",")
            company_city = results[0].strip()
            company_state = results[1].strip()
            company_country = results[2].strip()

            if company_state in us_state_dict.values():
                company_state_abbr = [
                    abbr
                    for abbr, name in us_state_dict.items()
                    if name == company_state
                ][0]
                address_line_3 = (
                    f"{company_city}, {company_state_abbr}, {company_country}"
                )
            elif company_state in ca_province_dict.values():
                company_state_abbr = [
                    abbr
                    for abbr, name in ca_province_dict.items()
                    if name == company_state
                ][0]
                address_line_3 = (
                    f"{company_city}, {company_state_abbr}, {company_country}"
                )
            else:
                address_line_3 = address_line_3
        except IndexError:
            address_line_3 = address_line_3

    except IndexError:
        assert False, "No results found"

    return address_line_1, address_line_2, address_line_3
