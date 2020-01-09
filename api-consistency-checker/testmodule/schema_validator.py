def state_schema_validator(data_struct, state_struct):
    unmatched = []

    def validator(each_state_struct):
        unmatched_record = []
        visited = []

        def visited_node(each_value):
            if each_value not in visited:
                visited.append(each_value)
            if each_value in each_state_struct:
                list_val = each_state_struct[each_value]
                if len(list_val) > 0:
                    for each_list_value in list_val:
                        visited_node(each_list_value)

        for each_value in each_state_struct:
            if each_value not in visited:
                if each_value not in data_struct.keys():
                    unmatched_record.append({"key not found": each_value})
                    visited_node(each_value)
                else:
                    child_value = each_state_struct[each_value]
                    for each_child_value in child_value:
                        if each_child_value not in visited:
                            if each_child_value not in data_struct[each_value]:
                                unmatched_record.append(
                                    {"value not found for the key>> " + each_value: each_child_value})
                                visited_node(each_child_value)

        return unmatched_record

    for each_list in state_struct:
        for key, value in each_list.items():
            mismatch = validator(value)
            unmatched.append({key: mismatch})

    return unmatched
