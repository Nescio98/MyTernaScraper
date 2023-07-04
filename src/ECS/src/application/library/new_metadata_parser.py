import os


def parse(file_name):
    """
    Parse the given file name and extract relevant information.

    Parameters
    ----------
    file_name : str
        The file name to be parsed.

    Returns
    -------
    dict
        A dictionary containing the parsed information.

    """
    if not file_name:
        return {}
    parts = [group for group in os.path.basename(file_name).strip().split('.') if group not in ['txt', 'csv']]
    if len(parts) == 4:
        a, rup, b, version = parts
        keys = ('type', 'date', 'rup', 'x', 'version', 'path')
        dictionary = dict(zip(keys, (*a.split('_'), rup, b, version, os.path.dirname(file_name))))
        dictionary['plant'] = dictionary['rup'].split('_')[0] if dictionary['type'] == 'NEW' else dictionary['type']
        dictionary['type'] = 'OLD' if dictionary['type'] != 'NEW' else dictionary['type']
        return dictionary
    elif len(parts) == 5:
        a, rup, b, version, validation = parts
        keys = ('type', 'date', 'rup', 'x', 'version', 'path', 'validation')
        return dict(zip(keys, (*a.split('_'), rup, b, version, os.path.dirname(file_name), validation)))
    else:
        return {}


def file_name(parsed):
    """
    Generate the file name from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    str
        The generated file name.

    """
    return f"{parsed['plant']}_{parsed['date']}.{parsed['rup']}.{parsed['x']}.{parsed['version']}.txt"


def date(parsed):
    """
    Extract the year and month from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    tuple
        A tuple containing the year and month.

    """
    return parsed['date'][0:4], parsed['date'][4:6] # year, month


def path(parsed):
    """
    Extract the path from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    str
        The path.

    """
    return parsed['path']


def full_path(parsed):
    """
    Generate the full path of the file from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    str
        The full path of the file.

    """
    return os.path.join(path(parsed), file_name(parsed))


def is_relevant(parsed):
    """
    Check if the parsed information corresponds to a relevant plant.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    bool
        True if the plant is relevant, False otherwise.

    """
    return parsed['plant'] == 'UPR' # Check this out


def plant(parsed):
    """
    Extract the plant information from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    str
        The plant information.

    """
    return parsed['plant']


def x(parsed):
    """
    Extract the 'x' information from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    str
        The 'x' information.

    """
    return parsed['x']


def power_type(parsed):
    """
    Extract the power type from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    str
        The power type.

    """
    return parsed['x'].split('_', 1)[0]


def pretty_power_type(parsed):
    """
    Generate a pretty representation of the power type from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    str
        The pretty representation of the power type.

    """
    switcher = {
        'PVI': 'injection', # immissione
        'PVP': 'withdrawal', # prelievo
        # Misure energia elettrica prodotta per singola sezione, incentivazione GSE
        'PVG': 'generation', # generazione (da ignorare)
        'PVF': 'PVF',
        'ICV': 'ICV'
    }
    return switcher.get(power_type(parsed), '')


def is_withdrawal(parsed):
    """
    Check if the parsed information corresponds to a withdrawal.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    bool
        True if it is a withdrawal, False otherwise.

    """
    return pretty_power_type(parsed) == 'withdrawal'


def is_injection(parsed):
    """
    Check if the parsed information corresponds to an injection.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    bool
        True if it is an injection, False otherwise.

    """
    return pretty_power_type(parsed) == 'injection'


def sapr(parsed):
    """
    Extract the SAPR information from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    str
        The SAPR information.

    """
    if parsed.get('rup') == 'UPN_A221709_01':
        return 'A221709'
    else:
        return parsed['x'].split('_', 1)[1][0:7] if len(parsed['x'].split('_', 1)[1]) == 11 else ''


def section(parsed):
    """
    Extract the section information from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    int
        The section information.

    """
    return int(parsed[x].split('_')[-1])


def rup(parsed):
    """
    Extract the RUP information from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    str
        The RUP information.

    """
    return parsed['rup']


def unit(parsed):
    """
    Extract the unit information from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    str
        The unit information.

    """
    return rup(parsed) if not sapr(parsed) and len(rup(parsed).split('_')) == 4 else ''


def version(parsed):
    """
    Extract the version information from the parsed information.

    Parameters
    ----------
    parsed : dict
        The parsed information.

    Returns
    -------
    int
        The version information.

    """
    return int(parsed['version'])
