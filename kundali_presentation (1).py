# kundali_presentation.py
from datetime import datetime
from kundali_calculations import calculate_kundali, sign_name

def display_ascendant_and_planetary_positions(report):
    """
    Retrieves the Ascendant sign and planetary positions from the Kundali report.

    Parameters:
        report (dict): The Kundali report dictionary obtained from `calculate_kundali`.

    Returns:
        dict: A dictionary containing the Ascendant sign information and planetary positions.
    """
    asc_sign = report.get('asc_sign_name', "Unknown")
    ascendant = report.get('ascendant', 0.0)
    planetary_info = {}

    for planet, details in report.items():
        if planet in ['Mahadasha', 'Antardasha', 'kundali_summary', 'planetary_positions',
                      'planet_in_houses', 'house_rulers', 'dasha_periods',
                      'current_dasha', 'current_antardasha']:
            continue
        planetary_info[planet] = {
            'Position': f"{details.get('position', 0.0):.2f}°",
            'Sign': details.get('planetary_sign', "Unknown")
        }

    ascendant_info = {
        'Ascendant Sign': f"{asc_sign} ({ascendant:.2f}°)"
    }

    return {
        'ascendant_info': ascendant_info,
        'planetary_info': planetary_info
    }

def display_house_rulers(report):
    """
    Retrieves the ruling planets for each house from the Kundali report.

    Parameters:
        report (dict): The Kundali report dictionary obtained from `calculate_kundali`.

    Returns:
        dict: A dictionary mapping each house to its ruling planet.
    """
    house_rulers = report.get('house_rulers', {})
    
    house_rulers_info = {}
    for house, ruler in house_rulers.items():
        house_rulers_info[f"House {house}"] = ruler
    
    return house_rulers_info

def display_planets_in_houses(report):
    """
    Retrieves which planets are in which houses along with their strengths and nature.

    Parameters:
        report (dict): The Kundali report dictionary obtained from `calculate_kundali`.

    Returns:
        dict: A dictionary containing detailed information about each planet's house placement.
    """
    planets_in_houses = report.get('planet_in_houses', {})
    planetary_info = report.get('report', {})  # Assuming 'report' key contains planetary data

    planets_info = {}
    for planet, house in planets_in_houses.items():
        planet_details = report.get(planet, {})
        ruler = planet_details.get('house_ruler', "Unknown")
        strength = planet_details.get('strength', "Unknown")
        nature = 'Benefic' if planet_details.get('benefic', False) else 'Malefic'
        sign = planet_details.get('planetary_sign', "Unknown")
        planets_info[planet] = {
            'House': house,
            'House Ruler': ruler,
            'Strength': strength,
            'Nature': nature,
            'Sign': sign
        }
    
    return planets_info

def display_dasha_periods(report):
    """
    Retrieves the Vimshottari Dasha periods from the Kundali report.

    Parameters:
        report (dict): The Kundali report dictionary obtained from `calculate_kundali`.

    Returns:
        list: A list of dictionaries, each containing details of a Dasha period.
    """
    dasha_periods = report.get('dasha_periods', [])
    
    dasha_info = []
    for dasha in dasha_periods:
        dasha_info.append({
            'Planet': dasha.get('planet', "Unknown"),
            'Start Date': dasha.get('start_date', "").strftime('%Y-%m-%d') if isinstance(dasha.get('start_date'), datetime) else "",
            'End Date': dasha.get('end_date', "").strftime('%Y-%m-%d') if isinstance(dasha.get('end_date'), datetime) else ""
        })
    
    return dasha_info

def display_current_dasha(report):
    """
    Retrieves the current Mahadasha period from the Kundali report.

    Parameters:
        report (dict): The Kundali report dictionary obtained from `calculate_kundali`.

    Returns:
        dict or str: A dictionary containing current Mahadasha details or an error message.
    """
    current_dasha = report.get('current_dasha', None)
    
    if current_dasha:
        dasha_info = {
            'Planet': current_dasha.get('planet', "Unknown"),
            'Start Date': current_dasha.get('start_date', "").strftime('%Y-%m-%d') if isinstance(current_dasha.get('start_date'), datetime) else "",
            'End Date': current_dasha.get('end_date', "").strftime('%Y-%m-%d') if isinstance(current_dasha.get('end_date'), datetime) else ""
        }
    else:
        dasha_info = "No current Mahadasha found."
    
    return dasha_info

def display_current_antardasha(report):
    """
    Retrieves the current Antardasha period from the Kundali report.

    Parameters:
        report (dict): The Kundali report dictionary obtained from `calculate_kundali`.

    Returns:
        dict or str: A dictionary containing current Antardasha details or an error message.
    """
    current_antardasha = report.get('current_antardasha', None)
    
    if current_antardasha:
        antardasha_info = {
            'Planet': current_antardasha.get('planet', "Unknown"),
            'Start Date': current_antardasha.get('start_date', "").strftime('%Y-%m-%d') if isinstance(current_antardasha.get('start_date'), datetime) else "",
            'End Date': current_antardasha.get('end_date', "").strftime('%Y-%m-%d') if isinstance(current_antardasha.get('end_date'), datetime) else ""
        }
    else:
        antardasha_info = "No current Antardasha found."
    
    return antardasha_info

def display_overall_summary(report):
    """
    Retrieves the overall Kundali summary from the Kundali report.

    Parameters:
        report (dict): The Kundali report dictionary obtained from `calculate_kundali`.

    Returns:
        str: A string containing the overall Kundali summary.
    """
    summary = report.get('kundali_summary', "No summary available.")
    return summary
