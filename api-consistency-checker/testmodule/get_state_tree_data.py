from testmodule import constant as cs
from testmodule.utils.utils import json_reader, get_key, get_entities


def get_state_schema_tree(state_json):
    """
    this function extract all the hierarchy mapping from state.json dict
    :param state_json: dict from state.json file
    :return:
    """
    parts = []
    data_model_schema = {}
    entities_val = {}
    json_prop = json_reader(cs.state_model_prop)
    for key in list(json_prop.keys()):
        result = get_key(state_json, json_prop[key])
        if result is not None and result[0] == True:
            data_model_schema[result[1]] = result[2]

    entities = get_key(state_json, cs.entities)
    if entities is not None and entities[0] == True:
        list_entitties = get_entities(entities[2], cs.entities_definition)
        data_model_schema[cs.entities_definitions] = list_entitties
        entities_val[cs.entities] = data_model_schema

        list_val = [cs.name, cs.type, cs.recurringListItemName, cs.required]

        part1_entities = entities_val

        part2_entities = get_entities_2_from_state_json(entities[2],list_val
                                                        )
        part3_entities = get_entities_3_from_state_json(entities[2], list_val)

        part4_entities = get_entities_4_from_state_json(entities[2], list_val)

        part5_entities = get_entities_5_from_state_json(entities[2], list_val)

        part6_entities = get_entities_6_from_state_json(entities[2], list_val)

        all_parts = [{cs.entityDefinition_body: part1_entities}, {cs.each_entity_outside_body: part2_entities},
                     {cs.each_entity_entityDefinition: part3_entities},
                     {cs.listItemPrototype_outside_body: part4_entities},
                     {cs.listItemPrototype_entity_entityDefinition: part5_entities},
                     {cs.listItemPrototype_entityDefintion: part6_entities}]

        parts = get_all_parts(all_parts)

    return parts


def get_all_parts(all_parts):
    """
    pass all the extracted entity, return
    if the entity is not empty

    :param all_parts:
    :return:
    """
    ret_val = []
    for dict_part in all_parts:
        for key, value in dict_part.items():
            if len(value) > 0:
                ret_val.append({key: value})
    return ret_val

def get_entities_2_from_state_json(schema_entity, key_name):
    # total list of children

    def recurring_list(state_schema_entity, key_name, no_of_entry, list_of_children):

        for val in state_schema_entity:
            main_dict = {}
            if type(val) is dict:
                # extract name,type,required,recurringListItemName
                for attr in key_name:
                    if attr in val.keys():
                        main_dict[attr] = val[attr]
                list_of_children.append({no_of_entry: main_dict})
                no_of_entry = no_of_entry + 1

                if cs.recurringListItemName in main_dict.keys():
                    recurringListItemName = main_dict[cs.recurringListItemName]
                    if not ((recurringListItemName is None) or (str(recurringListItemName).strip() == cs.empty_string)):
                        # check if 'children' in each entities
                        if cs.children in val.keys():
                            child_val = val[cs.children]
                            recurring_list(child_val, key_name, no_of_entry, list_of_children)
                    else:
                        last_child = []
                        child_val = val[cs.children]
                        for each_ent in child_val:
                            main_dict1 = {}
                            for each_val in each_ent.keys():
                                for attr_child in key_name:
                                    if attr_child == each_val:
                                        main_dict1[attr_child] = each_ent[attr_child]
                                main_dict1[cs.children] = each_ent[cs.children]
                            last_child.append(main_dict1)
                        list_of_children.append({no_of_entry: last_child})

    entity_definition = {}
    list_val = []
    number = 0
    list_val2 = []
    ret_val = {}

    for val1 in schema_entity:

        main_dict1 = {}
        if type(val1) is dict:
            # extract name,type,required,recurringListItemName
            for attr in key_name:
                if attr in val1.keys():
                    main_dict1[attr] = val1[attr]
            if cs.recurringListItemName in main_dict1.keys():
                recurringListItemName1 = main_dict1[cs.recurringListItemName]
                if not ((recurringListItemName1 is None) or (str(recurringListItemName1).strip() == cs.empty_string)):
                    # check if 'children' in each entities
                    if cs.children in val1.keys():
                        child_val = val1[cs.children]
                        if type(child_val) == type([]):
                            for each_children in child_val:
                                main_dict1[cs.children] = []
                                list_of_children = [{0: main_dict1}]
                                if type(each_children) is not type([]):
                                    each_children = [each_children]
                                recurring_list(each_children, key_name, 1, list_of_children)
                                length_of_child = len(list_of_children)
                                second_value = []
                                if length_of_child > 0:
                                    second_value = list_of_children[0][0]
                                if length_of_child > 1:
                                    while length_of_child > 1:
                                        second_value = list_of_children[length_of_child - 2][length_of_child - 2]
                                        temp_value = list_of_children[length_of_child - 1][length_of_child - 1]
                                        if type(temp_value) is dict:
                                            temp_value = [temp_value]
                                        second_value[cs.children] = temp_value
                                        length_of_child = length_of_child - 1
                                list_val.append({number: second_value})
                                list_val2.append(second_value)
                                number = number + 1
                else:
                    main_dict1_child = []
                    if cs.children in val1.keys():
                        child_val = val1[cs.children]
                        for each_child in child_val:
                            main_dict2 = {}
                            for attribute in key_name:
                                if attribute in each_child:
                                    main_dict2[attribute] = each_child[attribute]
                            if cs.children in each_child:
                                main_dict2[cs.children] = each_child[cs.children]

                            main_dict1_child.append(main_dict2)

                    main_dict1[cs.children] = main_dict1_child
                    list_val2.append(main_dict1)

            list_val.append({number: list_val2})
    max_num = 1
    list_names = {}
    for each_entity in list_val2:
        name = each_entity[cs.name]
        if name in list_names.keys():
            num = list_names[name]
            num = num + 1
            if max_num < num:
                max_num = num
            list_names[name] = num
        else:
            list_names[name] = 1

    dict_entity = []

    if len(list_names) > 0:
        for i in range(0, max_num):
            list_entities = []
            added_list = []
            for each_dict in list_val2:
                name = each_dict[cs.name]
                if name not in added_list:
                    if name in list_names.keys():
                        val = list_names[name]
                        if val > 0:
                            list_entities.append(each_dict)
                            val = val - 1
                            list_names[name] = val
                            added_list.append(name)

            dict_entity.append({i: list_entities})

    if len(dict_entity) > 0:
        entity_definition[cs.entities_definitions] = dict_entity
        ret_val[cs.entities] = entity_definition
    return ret_val


def get_entities_3_from_state_json(schema_entity, key_name):
    # total list of children

    def recurring_list(state_schema_entity, key_name, no_of_entry, list_of_children):

        for val in state_schema_entity:
            main_dict = {}
            if type(val) is dict:
                # extract name,type,required,recurringListItemName
                for attr in key_name:
                    if attr in val.keys():
                        main_dict[attr] = val[attr]
                list_of_children.append({no_of_entry: main_dict})
                no_of_entry = no_of_entry + 1

                if cs.recurringListItemName in main_dict.keys():
                    recurringListItemName = main_dict[cs.recurringListItemName]
                    if not ((recurringListItemName is None) or (str(recurringListItemName).strip() == cs.empty_string)):
                        # check if 'children' in each entities
                        if cs.children in val.keys():
                            child_val = val[cs.children]
                            recurring_list(child_val, key_name, no_of_entry, list_of_children)
                    else:
                        last_child = []
                        child_val = val[cs.children]
                        for each_ent in child_val:
                            main_dict1 = {}
                            if cs.entities_definition in each_ent.keys():
                                main_dict1 = each_ent[cs.entities_definition]

                            last_child.append(main_dict1)
                        list_of_children.append({no_of_entry: last_child})

    entity_definition = {}
    list_val = []
    number = 0
    list_val2 = []
    ret_val = {}

    for val1 in schema_entity:

        main_dict1 = {}
        if type(val1) is dict:
            # extract name,type,required,recurringListItemName
            for attr in key_name:
                if attr in val1.keys():
                    main_dict1[attr] = val1[attr]
            if cs.recurringListItemName in main_dict1.keys():
                recurringListItemName1 = main_dict1[cs.recurringListItemName]
                if not ((recurringListItemName1 is None) or (str(recurringListItemName1).strip() == cs.empty_string)):
                    # check if 'children' in each entities
                    if cs.children in val1.keys():
                        child_val = val1[cs.children]
                        if type(child_val) == type([]):
                            for each_children in child_val:
                                main_dict1[cs.children] = []
                                list_of_children = [{0: main_dict1}]
                                if type(each_children) is not type([]):
                                    each_children = [each_children]
                                recurring_list(each_children, key_name, 1, list_of_children)
                                length_of_child = len(list_of_children)
                                second_value = []
                                if length_of_child > 0:
                                    second_value = list_of_children[0][0]
                                if length_of_child > 1:
                                    while length_of_child > 1:
                                        second_value = list_of_children[length_of_child - 2][length_of_child - 2]
                                        temp_value = list_of_children[length_of_child - 1][length_of_child - 1]
                                        if type(temp_value) is dict:
                                            temp_value = [temp_value]
                                        second_value[cs.children] = temp_value
                                        length_of_child = length_of_child - 1
                                list_val.append({number: second_value})
                                list_val2.append(second_value)
                                number = number + 1
                else:
                    main_dict1_child = []
                    if cs.children in val1.keys():
                        child_val = val1[cs.children]
                        for each_child in child_val:
                            main_dict2 = {}
                            for attribute in key_name:
                                if attribute in each_child:
                                    main_dict2[attribute] = each_child[attribute]
                            if cs.children in each_child:
                                main_dict2[cs.children] = each_child[cs.children]

                            main_dict1_child.append(main_dict2)

                    main_dict1[cs.children] = main_dict1_child
                    list_val2.append(main_dict1)

            list_val.append({number: list_val2})
    max_num = 1
    list_names = {}
    for each_entity in list_val2:
        name = each_entity[cs.name]
        if name in list_names.keys():
            num = list_names[name]
            num = num + 1
            if max_num < num:
                max_num = num
            list_names[name] = num
        else:
            list_names[name] = 1

    dict_entity = []

    if len(list_names) > 0:
        for i in range(0, max_num):
            list_entities = []
            added_list = []
            for each_dict in list_val2:
                name = each_dict[cs.name]
                if name not in added_list:
                    if name in list_names.keys():
                        val = list_names[name]
                        if val > 0:
                            list_entities.append(each_dict)
                            val = val - 1
                            list_names[name] = val
                            added_list.append(name)

            dict_entity.append({i: list_entities})

    if len(dict_entity) > 0:
        entity_definition[cs.entities_definitions] = dict_entity
        ret_val[cs.entities] = entity_definition
    return ret_val


def get_entities_4_from_state_json(schema_entity, key_name):
    # total list of children

    def recurring_list(state_schema_entity, key_name, no_of_entry, list_of_children):
        if type(state_schema_entity) is dict:
            main_dict = {}
            # extract name,type,required,recurringListItemName
            for attr in key_name:
                if attr in state_schema_entity.keys():
                    main_dict[attr] = state_schema_entity[attr]
            list_of_children.append({no_of_entry: main_dict})
            no_of_entry = no_of_entry + 1

            if cs.children in state_schema_entity.keys():
                child_val = state_schema_entity[cs.children]
                last_child = []
                main_dict1 = {}
                for child_value in child_val:
                    if cs.entities_definition in child_value.keys():
                        main_dict1 = child_value[cs.entities_definition]
                    last_child.append(main_dict1)
                list_of_children.append({no_of_entry: last_child})

    list_entities = {}
    entity_definition = {}
    list_val = []

    for val1 in schema_entity:

        main_dict1 = {}
        if type(val1) is dict:
            # extract name,type,required,recurringListItemName
            for attr in key_name:
                if attr in val1.keys():
                    main_dict1[attr] = val1[attr]
            if cs.listItemPrototype in val1.keys():
                list_item_proto = val1[cs.listItemPrototype]
                if list_item_proto is not None:
                    main_dict1[cs.children] = []
                    list_of_children = [{0: main_dict1}]
                    recurring_list(list_item_proto, key_name, 1, list_of_children)

                    length_of_child = len(list_of_children)
                    second_value = []
                    if length_of_child > 0:
                        second_value = list_of_children[0][0]
                    if length_of_child > 1:
                        while length_of_child > 1:
                            second_value = list_of_children[length_of_child - 2][length_of_child - 2]
                            temp_value = list_of_children[length_of_child - 1][length_of_child - 1]
                            if type(temp_value) is dict:
                                temp_value = [temp_value]
                            second_value[cs.children] = temp_value
                            length_of_child = length_of_child - 1
                    list_val.append(second_value)

    if len(list_val) > 0:
        entity_definition[cs.entities_definitions] = list_val
        list_entities[cs.entities] = entity_definition
    return list_entities


def get_entities_5_from_state_json(schema_entity, key_name):
    # total list of children

    def recurring_list(state_schema_entity, key_name, no_of_entry, list_of_children):
        if type(state_schema_entity) is dict:
            main_dict = {}
            # extract name,type,required,recurringListItemName
            for attr in key_name:
                if attr in state_schema_entity.keys():
                    main_dict[attr] = state_schema_entity[attr]
            list_of_children.append({no_of_entry: main_dict})
            no_of_entry = no_of_entry + 1

            if cs.children in state_schema_entity.keys():
                child_val = state_schema_entity[cs.children]
                last_child = []
                for child_value in child_val:
                    main_dict1 = {}
                    for attr_child in key_name:
                        if attr_child in child_value:
                            main_dict1[attr_child] = child_value[attr_child]
                    if cs.children in child_value:
                        main_dict1[cs.children] = child_value[cs.children]
                    last_child.append(main_dict1)
                list_of_children.append({no_of_entry: last_child})

    list_entities = {}
    entity_definition = {}
    list_val = []

    for val1 in schema_entity:

        main_dict1 = {}
        if type(val1) is dict:
            # extract name,type,required,recurringListItemName
            for attr in key_name:
                if attr in val1.keys():
                    main_dict1[attr] = val1[attr]
            if cs.listItemPrototype in val1.keys():
                list_item_proto = val1[cs.listItemPrototype]
                if list_item_proto is not None:
                    main_dict1[cs.children] = []
                    list_of_children = [{0: main_dict1}]
                    recurring_list(list_item_proto, key_name, 1, list_of_children)
                    length_of_child = len(list_of_children)
                    second_value = []
                    if length_of_child > 0:
                        second_value = list_of_children[0][0]
                    if length_of_child > 1:
                        while length_of_child > 1:
                            second_value = list_of_children[length_of_child - 2][length_of_child - 2]
                            temp_value = list_of_children[length_of_child - 1][length_of_child - 1]
                            if type(temp_value) is dict:
                                temp_value = [temp_value]
                            second_value[cs.children] = temp_value
                            length_of_child = length_of_child - 1
                    list_val.append(second_value)

    if len(list_val) > 0:
        entity_definition[cs.entities_definitions] = list_val
        list_entities[cs.entities] = entity_definition
    return list_entities


def get_entities_6_from_state_json(schema_entity, key_name):
    list_entities = {}
    entity_definition = {}
    list_val = []

    for val1 in schema_entity:
        main_dict1 = {}
        if type(val1) is dict:
            # extract name,type,required,recurringListItemName
            for attr in key_name:
                if attr in val1.keys():
                    main_dict1[attr] = val1[attr]
            if cs.listItemPrototype in val1.keys():
                list_item_proto = val1[cs.listItemPrototype]
                if list_item_proto is not None:
                    main_dict1[cs.children] = []
                    if cs.entities_definition in list_item_proto.keys():
                        main_dict1[cs.children] = [list_item_proto[cs.entities_definition]]
                        list_val.append(main_dict1)

    if len(list_val) > 0:
        entity_definition[cs.entities_definitions] = list_val
        list_entities[cs.entities] = entity_definition
    return list_entities