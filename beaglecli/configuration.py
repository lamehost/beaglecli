"""
Configuration directives for the package.
"""
import os

from jsonschema import Draft4Validator, validators
from jsonschema.exceptions import ValidationError

import yaml
import yamlordereddictloader


def extend_with_default(validator_class):
    """
    Wrapper around jsonschema validator_class to add support for default values.

    Returns:
        Extended validator_class
    """
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        """
        Function to set default values
        """
        for _property, subschema in properties.iteritems():
            if "default" in subschema:
                instance.setdefault(_property, subschema["default"])

        for error in validate_properties(validator, properties, instance, schema):
            yield error

    return validators.extend(
        validator_class, {"properties" : set_defaults},
    )

DefaultValidatingDraft4Validator = extend_with_default(Draft4Validator)


def get_defaults(schema):
    """
    Gets default values from the schema

    Args:
        schema: jsonschema

    Returns:
        dict: dict with default values
    """
    result = ""
    try:
        _type = schema['type']
    except KeyError:
        return result
    except TypeError:
        raise SyntaxError('Error while parsing configuration file: "type" keyword missing at %s')

    if _type == 'object':
        result = dict(
            (k, get_defaults(v)) for k, v in schema['properties'].iteritems()
        )
    elif _type == 'array':
        result = [get_defaults(schema['items'])]
    else:
        try:
            result = schema['default']
        except KeyError:
            result = result

    return result


def updatedict(original, updates):
    """
    Updates the original dictionary with items in updates.
    If key already exists it overwrites the values else it creates it

    Args:
        original: original dictionary
        updates: items to be inserted in the dictionary

    Returns:
        dict: updated dictionary
    """
    for key, value in updates.items():
        if key not in original or type(value) != type(original[key]):
            original[key] = value
        elif isinstance(value, dict):
            original[key] = updatedict(original[key], value)
        else:
            original[key] = value

    return original


def keys_to_lower(item):
    """
    Normalize dict keys to lowercase.

    Args:
        dict: dict to be normalized

    Returns:
        Normalized dict
    """
    result = False
    if isinstance(item, list):
        result = [keys_to_lower(v) for v in item]
    elif isinstance(item, dict):
        result = dict((k.lower(), keys_to_lower(v)) for k, v in item.iteritems())
    else:
        result = item

    return result


def get_config(filename, lower_keys=True, create_default=True):
    """
    Gets default config and overwrite it with the content of filename.
    If the file does not exist, it creates it.

    Default config is generated by applying get_defaults() to local file named configuration.yaml .
    Content of filename by assuming the content is formatted in YAML.

    Args:
        filename: name of the YAML configuration file
        lower_keys: transform keys to lowercase
        create_default: create a new file with default settings

    Returns:
        dict: configuration statements
    """

    base_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(base_dir, 'configuration.yml')) as stream:
        try:
            configschema = yaml.load(stream, Loader=yamlordereddictloader.Loader)
        except yaml.scanner.ScannerError, error:
            raise SyntaxError('Error while parsing default configuration file: %s' % error)

    if os.path.exists(filename):
        with open(filename, 'r') as stream:
            defaults = get_defaults(configschema)
            try:
                config = yaml.load(stream)
            except (yaml.scanner.ScannerError), error:
                raise SyntaxError(error)
            config = updatedict(defaults, config)
            if lower_keys:
                config = keys_to_lower(config)
    elif create_default:
        config = get_defaults(configschema)
        try:
            with open(filename, 'w') as stream:
                yaml.dump(config, stream, default_flow_style=False)
                print 'Created configuration file: %s' % filename
        except IOError:
            raise IOError('Unable to create configuration file: %s' % filename)
    else:
        raise IOError('Unable to open configuration file: %s' % filename)

    try:
        DefaultValidatingDraft4Validator(configschema).validate(config)
    except ValidationError, error:
        raise SyntaxError('Error while parsing configuration file: %s' % error.message)
    return config
