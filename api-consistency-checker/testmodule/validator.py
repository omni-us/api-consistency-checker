import json
from testmodule import constant as cs
from .schema_validator import state_schema_validator
from .get_state_tree_data import get_state_schema_tree
from testmodule.utils.utils import flatten_json, json_reader, get_data_struct, get_heirarchy_tree


def validator(data_model, data, state, xml_validator):
    """
    :param data_model: path of data_model.json
    :param data: path of data.json
    :param state: path of state.json
    :param xml_validator: path of xml_validator.xml
    """

    # read the data model json file
    model_json = json_reader(data_model)

    # read the data.json file
    data_json = json_reader(data)

    # read the state.json file
    state_json = json_reader(state)

    # xml_data = xml_reader(xml_validator)

    # get tree structure of the data_model json object
    data_struct = get_data_struct(model_json, cs.data_model_prop)

    # save state.json as tree
    save_file(cs.data_model_tree, data_struct)

    # get tree structure of state.json object
    state_struct = get_state_schema_tree(state_json)

    # save state.json as tree
    save_file(cs.state_tree, state_struct)

    # flatten list for state tree
    state_struct_flattened_data = get_flatten_json_for_state_schema(state_struct)

    # save the flattened state tree
    save_file(cs.state_flattened_tree, state_struct_flattened_data)

    # flatten list for data model tree
    data_model_flattened_data = flatten_json(data_struct)

    # save the flattened data model tree
    save_file(cs.data_model_flattened_tree, data_model_flattened_data)

    # save the hierarchy image of data_model.json
    get_heirarchy_tree(cs.data_model_flattened_tree, cs.data_model_hierarchy_image)

    # save_file("data_struct1.json",data_model_flattened_data)
    # save_file("state_struct1.json",state_struct_flattened_data)

    # get the unmatched result for state and model
    unmatched_state_schema = state_schema_validator(data_model_flattened_data, state_struct_flattened_data)

    print(unmatched_state_schema)


def get_flatten_json_for_state_schema(state_struct):
    """

    :param state_struct: all the hierarchy tree from state json
    :return: all list of flattened json
    """
    flat_state_json_data = []
    val1 = cs.entity_outside_body
    val2 = cs.each_entity_definition

    for value in state_struct:
        for key in value:
            if key not in [val1, val2]:
                flat_state_json_data.append({key: flatten_json(value[key])})
            else:
                key_value = value[key]
                entities = key_value[cs.entities]
                entities_definition = entities[cs.entities_definitions]

                for each_dict in entities_definition:
                    for each_dict_key, each_dict_value in each_dict.items():
                        entities_definition_new = {cs.entities_definitions: each_dict_value}
                        list_entities = {cs.entities: entities_definition_new}

                        flat_state_json_data.append(
                            {key + cs.double_underscore + str(each_dict_key): flatten_json(list_entities)})

    return flat_state_json_data


def save_file(path, data):
    """
    :param path: path where json data need to be save
    :param data: dict or json object
    """
    with open(path, 'w') as fout:
        json.dump(data, fout)
