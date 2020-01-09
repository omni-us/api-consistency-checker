def data_validator(datamodel, data):
    all_keys = []

    for key in datamodel:
        # print(key, datamodel[key])
        all_keys.append(key)
        get_all_pair(datamodel[key])

        # print(innerkey,"\n")

    print(all_keys)


def get_all_pair(value):
    if type(value) is dict:
        for key in value:
            get_all_pair(value[key])
    elif type(value) is list:
        for listval in value:
            get_all_pair(listval)
    else:
        print('\n\n',value)
