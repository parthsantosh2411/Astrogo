# kundali_calculations.py

import swisseph as swe
from opencage.geocoder import OpenCageGeocode
from datetime import datetime, timedelta
import pytz
from functools import lru_cache
import os


# Your OpenCage API key (Ensure this is securely stored)
opencage_api_key = 'opencage_api_key'    # Ensure this is securely stored
geocoder = OpenCageGeocode(opencage_api_key)

def sign_name(sign_number):
    """
    Maps a sign number to its corresponding zodiac sign name.
    Sign numbers are 1 to 12.
    """
    signs_english = {
        1: "Aries",
        2: "Taurus",
        3: "Gemini",
        4: "Cancer",
        5: "Leo",
        6: "Virgo",
        7: "Libra",
        8: "Scorpio",
        9: "Sagittarius",
        10: "Capricorn",
        11: "Aquarius",
        12: "Pisces"
    }
    return signs_english.get(sign_number, "Unknown Sign")

@lru_cache(maxsize=128)
def get_coordinates_from_place(place_name):
    """
    Retrieves the latitude and longitude for a given place name using the OpenCage Geocoding API.
    Implements caching to avoid redundant API calls.
    """
    result = geocoder.geocode(place_name)
    if result and len(result):
        latitude = result[0]['geometry']['lat']
        longitude = result[0]['geometry']['lng']
        return latitude, longitude
    else:
        raise ValueError(f"Coordinates not found for the place: {place_name}")

def calculate_julian_day(date_of_birth, time_of_birth):
    """
    Calculates the Julian Day for the given birth date and time.
    Timezone is fixed to Asia/Kolkata.
    """
    timezone_name = 'Asia/Kolkata'
    try:
        tz = pytz.timezone(timezone_name)
    except pytz.UnknownTimeZoneError:
        raise ValueError(f"Unknown timezone: {timezone_name}")
    
    try:
        datetime_of_birth = tz.localize(datetime.strptime(f"{date_of_birth} {time_of_birth}", '%Y-%m-%d %H:%M'))
    except ValueError:
        raise ValueError("Incorrect date or time format. Expected YYYY-MM-DD for date and HH:MM for time.")
    
    # Convert to UTC for Julian Day calculation
    datetime_of_birth_utc = datetime_of_birth.astimezone(pytz.utc)
    jd = swe.julday(
        datetime_of_birth_utc.year,
        datetime_of_birth_utc.month,
        datetime_of_birth_utc.day,
        datetime_of_birth_utc.hour + datetime_of_birth_utc.minute / 60.0 + datetime_of_birth_utc.second / 3600.0
    )
    return jd

def calculate_planetary_positions_and_houses(date_of_birth, time_of_birth, place_name):
    """
    Calculates planetary positions and assigns them to houses using the Whole Sign house system.
    Returns:
        planetary_positions: Dict of planet names to their longitude in degrees.
        planet_in_houses: Dict of planet names to their house number.
        planetary_signs: Dict of planet names to their zodiac sign.
        ascendant: Ascendant in degrees.
        asc_sign_name: Name of the Ascendant sign.
    """
    # Get coordinates
    latitude, longitude = get_coordinates_from_place(place_name)
    
    # Calculate Julian Day (UTC)
    jd = calculate_julian_day(date_of_birth, time_of_birth)
    
    # Set the sidereal mode with Lahiri ayanamsa
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    # Define planets to calculate with their corresponding Swiss Ephemeris constants
    planets = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
        'Rahu': swe.TRUE_NODE,
        'Ketu': None  # Ketu is calculated separately as opposite to Rahu
    }
    
    # Initialize dictionaries to store planetary positions and signs
    planetary_positions = {}
    planetary_signs = {}
    planet_in_houses = {}
    
    # Define the flags for sidereal calculations
    iflag = swe.FLG_SIDEREAL
    
    # Calculate planetary positions using Swiss Ephemeris
    for planet, planet_code in planets.items():
        if planet == "Ketu":
            # Ketu's position is always opposite Rahu
            rahu_position, ret = swe.calc_ut(jd, swe.TRUE_NODE, iflag)
            if ret < 0:
                raise Exception(f"Error calculating position for Rahu: {swe.get_error_message(ret)}")
            rahu_lon = rahu_position[0]  # Extract Rahu's longitude as float
            ketu_lon = (rahu_lon + 180.0) % 360.0
            planetary_positions["Ketu"] = ketu_lon
        else:
            position_data, ret = swe.calc_ut(jd, planet_code, iflag)
            if ret < 0:
                raise Exception(f"Error calculating position for {planet}: {swe.get_error_message(ret)}")
            lon = position_data[0]  # Extract longitude as float
            planetary_positions[planet] = lon
    
    # Calculate house cusps and ascendant using Whole Sign Houses in SIDEREAL mode
    hsys = 'W'  # Use Whole Sign Houses
    house_cusps, ascmc = swe.houses_ex(jd, latitude, longitude, hsys.encode(), iflag)
    ascendant = ascmc[0]  # Ascendant in degrees
    
    # Calculate the sign of the Ascendant
    asc_sign = int(ascendant / 30) + 1  # 1 to 12
    asc_sign = asc_sign if asc_sign <= 12 else asc_sign - 12
    asc_sign_name = sign_name(asc_sign)
    
    # Assign planets to houses based on their longitude and the Whole Sign house system
    for planet, lon in planetary_positions.items():
        planet_sign_number = int(lon / 30) + 1  # 1 to 12
        planet_sign_number = planet_sign_number if planet_sign_number <= 12 else planet_sign_number - 12
        planet_sign_name = sign_name(planet_sign_number)
        planetary_signs[planet] = planet_sign_name
        house = ((planet_sign_number - asc_sign) % 12) + 1  # 1 to 12
        planet_in_houses[planet] = house
    
    return planetary_positions, planet_in_houses, planetary_signs, ascendant, asc_sign_name

def calculate_vimshottari_dasha(jd_birth):
    """
    Calculates the Vimshottari Dasha periods based on the birth Julian Day.
    Returns a list of dictionaries with 'planet', 'start_date', and 'end_date'.
    """
    # Vimshottari Dasha sequence and their lengths in years
    dasha_sequence = [
        ('Ketu', 7),
        ('Venus', 20),
        ('Sun', 6),
        ('Moon', 10),
        ('Mars', 7),
        ('Rahu', 18),
        ('Jupiter', 16),
        ('Saturn', 19),
        ('Mercury', 17)
    ]

    # Get the Moon's nakshatra at birth
    iflag = swe.FLG_SIDEREAL
    moon_position, ret = swe.calc_ut(jd_birth, swe.MOON, iflag)
    if ret < 0:
        raise Exception(f"Error calculating Moon position: {swe.get_error_message(ret)}")
    moon_lon = moon_position[0]
    nakshatra_number = int((moon_lon % 360) / 13.3333333)  # Each nakshatra is ~13.3333 degrees

    # Determine the starting dasha
    dasha_order = dasha_sequence[nakshatra_number % 9:] + dasha_sequence[:nakshatra_number % 9]

    # Calculate the fraction of the nakshatra completed
    nakshatra_pada = (moon_lon % 13.3333333) / 13.3333333  # Fraction completed
    balance_years = dasha_order[0][1] * (1 - nakshatra_pada)

    # Calculate Dasha periods
    dasha_periods = []

    # Convert jd_birth to datetime
    year, month, day, hour = swe.revjul(jd_birth, swe.GREG_CAL)
    int_hour = int(hour)
    minute = int((hour - int_hour) * 60)
    second = int((((hour - int_hour) * 60) - minute) * 60)
    current_time = datetime(year, month, day, int_hour, minute, second)

    # First Dasha
    start_date = current_time
    end_date = start_date + timedelta(days=balance_years * 365.25)
    dasha_periods.append({
        'planet': dasha_order[0][0],
        'start_date': start_date,
        'end_date': end_date
    })
    current_time = end_date

    # Subsequent Dashas
    for planet, years in dasha_order[1:]:
        start_date = current_time
        end_date = start_date + timedelta(days=years * 365.25)
        dasha_periods.append({
            'planet': planet,
            'start_date': start_date,
            'end_date': end_date
        })
        current_time = end_date

    return dasha_periods

def get_current_dasha(dasha_periods):
    """
    Finds the current Mahadasha from the list of Dasha periods.
    """
    current_time = datetime.utcnow()
    current_dasha = None
    for dasha in dasha_periods:
        if dasha['start_date'] <= current_time <= dasha['end_date']:
            current_dasha = dasha
            break
    return current_dasha

def calculate_antardasha(current_dasha, dasha_periods):
    """
    Calculates the current Antardasha within the current Mahadasha.
    """
    if not current_dasha:
        return None  # No current Mahadasha found

    # Vimshottari Dasha cycle has a total of 120 years
    # Each Mahadasha is divided into Antardashas based on the sequence
    dasha_sequence = [
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 
        'Rahu', 'Jupiter', 'Saturn', 'Mercury'
    ]

    mahadasha_planet = current_dasha['planet']
    try:
        start_index = dasha_sequence.index(mahadasha_planet)
    except ValueError:
        raise Exception(f"Mahadasha planet {mahadasha_planet} not found in the sequence.")

    # Define Antardasha sequence starting from Mahadasha planet
    antardasha_sequence = dasha_sequence[start_index:] + dasha_sequence[:start_index]

    # Define the lengths of each Antardasha in years
    antardasha_lengths = {
        'Ketu': 7,
        'Venus': 20,
        'Sun': 6,
        'Moon': 10,
        'Mars': 7,
        'Rahu': 18,
        'Jupiter': 16,
        'Saturn': 19,
        'Mercury': 17
    }

    # Total Mahadasha duration in days
    total_dasha_duration = (current_dasha['end_date'] - current_dasha['start_date']).days

    # Calculate the duration of each Antardasha
    antardasha_periods = []
    cumulative_days = 0
    for planet in antardasha_sequence:
        duration_years = antardasha_lengths[planet]
        duration_days = (duration_years / 120.0) * total_dasha_duration
        start = current_dasha['start_date'] + timedelta(days=cumulative_days)
        end = start + timedelta(days=duration_days)
        antardasha_periods.append({
            'planet': planet,
            'start_date': start,
            'end_date': end
        })
        cumulative_days += duration_days

    # Find current Antardasha
    current_antardasha = None
    for antardasha in antardasha_periods:
        if antardasha['start_date'] <= datetime.utcnow() <= antardasha['end_date']:
            current_antardasha = antardasha
            break

    return current_antardasha

def determine_house_rulers(asc_sign):
    """
    Determines the ruling planet for each house based on the Ascendant sign using Whole Sign Houses.
    """
    # Each house corresponds to a sign in Whole Sign Houses
    sign_rulers = {
        "Aries": "Mars",
        "Taurus": "Venus",
        "Gemini": "Mercury",
        "Cancer": "Moon",
        "Leo": "Sun",
        "Virgo": "Mercury",
        "Libra": "Venus",
        "Scorpio": "Mars",
        "Sagittarius": "Jupiter",
        "Capricorn": "Saturn",
        "Aquarius": "Saturn",
        "Pisces": "Jupiter"
    }
    
    house_rulers = {}
    for house in range(1, 13):
        # In Whole Sign Houses, each house corresponds to a sign
        sign_index = (asc_sign + house - 2) % 12 + 1  # Adjusted for 1-based indexing
        sign_name_str = sign_name(sign_index)
        ruler = sign_rulers.get(sign_name_str, "Unknown")
        house_rulers[house] = ruler
    return house_rulers

def get_planetary_strength(planet, sign):
    """
    Determines the strength of a planet based on its sign.
    Returns:
        strength: String indicating the strength ('Strong', 'Exalted', 'Debilitated', 'Weak', 'Neutral')
        is_benefic: Boolean indicating if the planet is benefic
    """
    # Define benefic and malefic planets
    benefics = ['Sun', 'Venus', 'Jupiter', 'Mercury', 'Moon']
    malefics = ['Mars', 'Saturn', 'Rahu', 'Ketu']
    
    # Define exaltation and debilitation signs
    exaltation = {
        'Sun': 'Aries',
        'Moon': 'Taurus',
        'Mars': 'Capricorn',
        'Mercury': 'Virgo',
        'Jupiter': 'Cancer',
        'Venus': 'Pisces',
        'Saturn': 'Libra'
        # Rahu and Ketu have no exaltation/debilitation
    }
    
    debilitation = {
        'Sun': 'Libra',
        'Moon': 'Scorpio',
        'Mars': 'Cancer',
        'Mercury': 'Pisces',
        'Jupiter': 'Capricorn',
        'Venus': 'Virgo',
        'Saturn': 'Aries'
        # Rahu and Ketu have no exaltation/debilitation
    }
    
    # Define own signs
    own_signs = {
        'Sun': ['Leo'],
        'Moon': ['Cancer'],
        'Mars': ['Aries', 'Scorpio'],
        'Mercury': ['Gemini', 'Virgo'],
        'Jupiter': ['Sagittarius', 'Pisces'],
        'Venus': ['Taurus', 'Libra'],
        'Saturn': ['Capricorn', 'Aquarius']
        # Rahu and Ketu do not have own signs
    }
    
    # Determine strength
    if planet in exaltation and sign == exaltation[planet]:
        strength = 'Exalted'
    elif planet in debilitation and sign == debilitation[planet]:
        strength = 'Debilitated'
    elif planet in own_signs and sign in own_signs[planet]:
        strength = 'Strong'
    elif planet in malefics and sign in ['Cancer', 'Capricorn', 'Virgo', 'Pisces']:
        strength = 'Weak'
    elif planet in benefics and sign in ['Scorpio', 'Libra', 'Capricorn', 'Aquarius']:
        strength = 'Weak'
    else:
        strength = 'Neutral'
    
    # Determine if benefic
    is_benefic = planet in benefics
    
    return strength, is_benefic

def make_personalized_report(planet_in_houses, house_rulers, dasha_periods, current_dasha, current_antardasha, planetary_positions, planetary_signs, asc_sign_name, ascendant):
    """
    Creates a personalized astrological report without predictions.
    Returns a dictionary containing all relevant astrological data.
    """
    report = {}
    
    # Add planetary information
    for planet, house in planet_in_houses.items():
        sign = planetary_signs.get(planet, "Unknown")
        strength, is_benefic = get_planetary_strength(planet, sign)
        report[planet] = {
            'house': house,
            'house_ruler': house_rulers.get(house, "Unknown"),
            'strength': strength,
            'benefic': is_benefic,
            'position': planetary_positions.get(planet, 0),
            'planetary_sign': sign
        }
    
    # Add Dasha information
    report['Mahadasha'] = {}
    if current_dasha:
        report['Mahadasha'] = {
            'planet': current_dasha['planet'],
            'start_date': current_dasha['start_date'].strftime('%Y-%m-%d'),
            'end_date': current_dasha['end_date'].strftime('%Y-%m-%d')
        }
    
    report['Antardasha'] = {}
    if current_antardasha:
        report['Antardasha'] = {
            'planet': current_antardasha['planet'],
            'start_date': current_antardasha['start_date'].strftime('%Y-%m-%d'),
            'end_date': current_antardasha['end_date'].strftime('%Y-%m-%d')
        }

    # Prepare overall summary
    kundali_summary = prepare_kundali_summary(
        planetary_positions, planet_in_houses, house_rulers, report, asc_sign_name, ascendant
    )
    
    report['kundali_summary'] = kundali_summary
    
    # Add additional data if necessary
    report['planetary_positions'] = planetary_positions
    report['planet_in_houses'] = planet_in_houses
    report['house_rulers'] = house_rulers
    report['dasha_periods'] = dasha_periods
    report['current_dasha'] = current_dasha
    report['current_antardasha'] = current_antardasha
    
    return report

def prepare_kundali_summary(planetary_positions, planet_in_houses, house_rulers, report, asc_sign_name, ascendant):
    """
    Prepares a detailed summary of the Kundali report to be used as context for the chatbot.
    """
    summary = "Kundali Report Summary:\n"
    summary += f"Ascendant (Lagna): {asc_sign_name} ({ascendant:.2f}°)\n\n"
    summary += "Planetary Positions:\n"
    for planet, details in report.items():
        if planet in ['Mahadasha', 'Antardasha', 'kundali_summary']:
            continue
        sign_number = int(details['position'] / 30) + 1
        sign_number = sign_number if sign_number <= 12 else sign_number - 12
        sign_name_str = sign_name(sign_number)
        summary += (f"{planet}: {details['position']:.2f}° in {sign_name_str}, "
                   f"House {details['house']} ({details['house_ruler']}), "
                   f"Strength: {details['strength']}, Nature: {'Benefic' if details['benefic'] else 'Malefic'}\n")
    
    summary += "\nCurrent Mahadasha: "
    if report.get('Mahadasha'):
        summary += (f"{report['Mahadasha']['planet']} (from {report['Mahadasha']['start_date']} "
                   f"to {report['Mahadasha']['end_date']})\n")
    else:
        summary += "Not Found\n"
    
    summary += "Current Antardasha: "
    if report.get('Antardasha'):
        summary += (f"{report['Antardasha']['planet']} (from {report['Antardasha']['start_date']} "
                   f"to {report['Antardasha']['end_date']})\n")
    else:
        summary += "No current Antardasha found.\n"
    
    return summary

def calculate_kundali(date_of_birth, time_of_birth, place_name):
    """
    High-level function to calculate Kundali based on user input.
    Returns a dictionary with all relevant astrological data.
    """
    # Step 1: Calculate planetary positions and houses
    planetary_positions, planet_in_houses, planetary_signs, ascendant, asc_sign_name = calculate_planetary_positions_and_houses(
        date_of_birth, time_of_birth, place_name
    )
    
    # Step 2: Determine house rulers
    house_rulers = determine_house_rulers(int(ascendant / 30) + 1)
    
    # Step 3: Calculate Dasha periods
    jd_birth = calculate_julian_day(date_of_birth, time_of_birth)
    dasha_periods = calculate_vimshottari_dasha(jd_birth)
    current_dasha = get_current_dasha(dasha_periods)
    current_antardasha = calculate_antardasha(current_dasha, dasha_periods)
    
    # Step 4: Create personalized report
    report = make_personalized_report(
        planet_in_houses, house_rulers, dasha_periods, current_dasha, current_antardasha,
        planetary_positions, planetary_signs, asc_sign_name, ascendant
    )
    
    return report


