import sys
import testmodule.validator as validator


def main():
    """

    :rtype: object
    """
    assert (len(sys.argv) == 5), 'Please pass 4 files path'
    data_model_json_path = sys.argv[1]
    data_json_path = sys.argv[2]
    state_json_path = sys.argv[3]
    validate_xml_path = sys.argv[4]
    validator.validator(data_model_json_path,data_json_path,state_json_path,validate_xml_path)


if __name__ == '__main__':
    main()
