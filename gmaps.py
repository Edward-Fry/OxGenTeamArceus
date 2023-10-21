"""

This file gets the locations and pictures of places from google maps
"""

import googlemaps

gmaps = googlemaps.Client(key='AIzaSyCzInNDgtJ9TUJYHQViJCM_qczxmQT1y7Q')

# # Geocoding an address
# geocode_result = gmaps.geocode('Kenwood House')

def get_places_from_text(text) -> list[dict]:
    """
    Gets the places from the text
    """
    return gmaps.places(text)['results']

def get_place_name_from_place(place: dict) -> str:
    """
    Gets the name from the place
    """
    return place['name']

def get_location_from_place(place: dict) -> tuple[float, float]:
    """
    Gets the location from the place
    """
    location = place['geometry']['location']
    return location['lat'], location['lng']

def get_and_render_image_details_from_place(place: dict) -> str:
    """
    Gets the image_ref, max_height, max_width from the place
    """
    photo = place['photos'][0]
    reference, max_height, max_width = photo['photo_reference'], photo['height'], photo['width']

    raw_image_data = gmaps.places_photo(reference, max_width=max_width, max_height=max_height)

    byte_string = b''

    # f = open('image.jpg', 'wb') # write the image to a file
    for chunk in raw_image_data:
        if chunk:
            byte_string += chunk
            # f.write(chunk)
    # f.close()
    return byte_string


def get_places_images_and_locations_from_text(search_text: str) -> list[dict]:
    """
    Finds the places and information from the text
    """
    places = get_places_from_text(search_text)
    places_and_information = []
    if len(places) > 0:
        for place in places:
            name = get_place_name_from_place(place)
            lat, lng = get_location_from_place(place)
            image = get_and_render_image_details_from_place(place)
            places_and_information.append({'name' : name,'lat': lat, 'lng': lng, 'image': image})
    else:
        print('No places found')

    return places_and_information

if __name__ == "__main__":
    # search for places with the word 'Kenwood House' in them
    place_information = get_places_images_and_locations_from_text('Kenwood House')
    # print(place_information)

    dud = 0
