def flatten_json(nested_json):
    from testmodule import constant as cs

    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        # if the type is dict
        if type(x) is dict:
            for a in x.keys():
                # get the parent name node
                if cs.children in x.keys() and cs.name in x.keys():
                    temp_val = name + cs.double_underscore + x[cs.name]
                    if name not in out.keys():
                        out[name] = [temp_val]
                    else:
                        if name + temp_val not in out[name]:
                            child_val = out[name]
                            child_val.append(temp_val)
                            out[name] = child_val

                    if a == cs.children:
                        flatten(x[cs.children], temp_val)
                    else:
                        if temp_val in out.keys():
                            if temp_val not in out[temp_val]:
                                list_val = out[temp_val]
                                list_val.append(temp_val + cs.double_underscore + a)
                                out[temp_val] = list_val
                        else:
                            out[temp_val] = [temp_val + cs.double_underscore + a]
                        flatten(x[a], temp_val + cs.double_underscore + a)
                else:
                    temp_val = name + cs.double_underscore + a
                    if name in out.keys():
                        if temp_val not in out[name]:
                            list_val = out[name]
                            list_val.append(temp_val)
                            out[name] = list_val
                    else:
                        out[name] = [temp_val]
                    flatten(x[a], temp_val)
        # if the type is list
        elif type(x) is list:
            for a in x:
                flatten(a, name)
        # if it a constant value
        else:
            if (x is None) or (str(x).strip() == cs.empty_string):
                out[name] = []
            elif name in out.keys():
                list_val = out[name]
                list_val.append(name + cs.double_underscore + str(x))
                out[name] = list_val
            else:
                out[name] = [name + cs.double_underscore + str(x)]

    flatten(nested_json[cs.entities], cs.entities)

    return out


def json_reader(json_data):
    import json
    """

    :param json_data: full path of json file
    :return: dictionary
    """
    # read file
    with open(json_data, 'r') as myfile:
        data = myfile.read()

    # parse file
    obj = json.loads(data)
    return obj


def get_key(datamodel, key):
    """
    search any key in the nested dictionay,
    if found get the value
    :param datamodel:
    :param key:
    :return:
    """
    if type(datamodel) is dict:
        for data_key in datamodel.keys():
            if key == data_key:
                return True, key, datamodel[data_key]
            elif type(datamodel[data_key]) == type([]):
                for key_val in datamodel[data_key]:
                    result = get_key(key_val, key)
                    if result is not None and result[0] == True:
                        return result
            elif type(datamodel[data_key]) is dict:
                result = get_key(datamodel[data_key], key)
                if result is not None and result[0] == True:
                    return result
    elif type(datamodel) == type([]):
        for key_val in datamodel:
            result = get_key(datamodel[key_val], key)
            if result is not None and result[0] == True:
                return result


def get_entities(state_schema_entity, key_name):
    """
    get all the key found in the nested dict
    :param state_schema_entity:
    :param key_name:
    :return:
    """
    list_entities = []

    for key in state_schema_entity:
        for key_val in key.keys():
            if key_val == key_name:
                list_entities.append(key[key_name])

    return list_entities


def get_data_struct(data_model, prop_file):
    """

    :param data_model: data_model json as dictionary
    :param prop_file: property file - data_model_prop.json defined at omniustest/properties
    :return:
    """
    data_model_schema = {}
    entities = {}
    json_prop = json_reader(prop_file)
    for key in list(json_prop.keys()):
        result = get_key(data_model, json_prop[key])
        if result is not None and result[0] == True:
            data_model_schema[key] = result[2]

    entities['entities'] = data_model_schema

    return entities


def get_heirarchy_tree(path, image):
    """
    save the hierarchy map as pdf
    :param path:
    :param image:
    """
    from graphviz import Digraph
    import json

    u = Digraph(filename=image,
                node_attr={'fixedsize': 'true',
                           'width': '6',
                           'height': '1', 'fontsize': '7', 'color': 'lightblue2', 'style': 'filled'})

    # read file
    with open(path, 'r') as myfile:
        data = myfile.read()

        # parse file
        obj = json.loads(data)

    for key in obj.keys():
        list_val = obj[key]
        for val in list_val:
            u.edge(key, val)

    u.render(image)

# def xml_reader(xmlfile):
#     import xml.etree.ElementTree as ET
#
#     """
#
#     :param xmlfile: full path of the xml file
#     :return: dictionary
#     """
#     # create element tree object
#     tree = ET.parse(xmlfile)
#
#     # get root element
#     root = tree.getroot()
#
#     items = []
#     dict = {}
#
#     for child in root:
#         if 'Page' in child.tag:
#             for child2 in child:
#                 if 'TextRegion' in child2.tag:
#                     for child3 in child2:
#                         if 'Property' in child3.tag:
#                             if dict is None or child3.attrib['value'] not in dict.keys():
#                                 dict[child3.attrib['value']] = []
#                         if 'TextLine' in child3.tag:
#                             for child4 in child3:
#                                 if 'Property' in child4.tag:
#                                     val = child4.attrib['value']
#                                     # dict2 = {"name" : val}
#                                     # dict3 = dict[list(dict.keys())[-1]]
#                                     # dict3.append(dict2)
#                                     # dict[list(dict.keys())[-1]] = dict3
#                                     # print(dict[list(dict.keys())[-1]])
#     print(dict)
#
#     return items


# def removal_of_conf_val(json_val):
#     conf_val = ['confidence', 'value']
#
#     def nested_json(json_val):
#         if type(json_val) is dict:
#             for key in json_val:
#                 nested_json(json_val[key])
#         elif type(json_val) is type([]):
#             for item in json_val:
#                 nested_json(item)
#         else:
#             print(json_val)
#
#     def check_for_conf_val(json_data):
#         if all(x in json_data for x in conf_val):
#             return True
#         else:
#             return False
#
#     nested_json(json_val)
#
#
# def removal_of_conf(list_val):
#     list_val2 = {}
#     for key in list_val:
#         if 'confidence' not in key and 'value' not in key:
#             lists = []
#             for value in list_val[key]:
#                 if 'confidence' not in value and 'value' not in value:
#                     lists.append(value)
#             if len(lists) > 0:
#                 list_val2[key] = lists
#
#     return list_val2
