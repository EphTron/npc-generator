import pandas as pd


def merge_json_files(file_path_list, output_json_file):
    """
    Merge one or more name jsons into one json file. Write the json file.
    :param file_path_list: list of strings
    :param output_json_file: string
    :return: -
    """
    name_file_list = []
    for path in file_path_list:
        name_file_list.append(list(pd.read_json(path).names))

    merged_names_file = []
    for nf in name_file_list:
        merged_names_file += nf

    written = 0
    skipped = 0

    # open output file
    out = open(output_json_file, "w")

    # open json brackets
    out.write('{"year": "2018", "names": [')

    merged_names_file = list(set(merged_names_file))
    # write names to file
    for idx, name in enumerate():

        # break line after 5000 names
        if (idx % 5000 == 0):
            out.write('\n')

        # check that names don't contain @ or (
        if '@' in name or '(' not in name:
            written += 1

            # write name to file
            if name == set(merged_names_file)[-1]:
                out.write('"' + name + '"')
            else:
                out.write('"' + name + '", ')

        # skip name because it contains wrong symbol
        else:
            skipped += 1

    # close json brackets
    out.write(']}')

    print('Wrote ' + str(written) + ' names.')
    print('Skipped ' + str(skipped) + ' names.')

    out.close()


def name_txt_to_json(file_name, output_json_file):
    """
    Read a txt file which contains a name in every row and create a json object out of it.
    Write the json object to a output file.
    :param file_name: string
    :param output_json_file: string
    :return: -
    """
    # open txt file
    with open(file_name) as f:
        content = f.readlines()
        content = [x.strip() for x in content]

    f.close()

    skipped = len(content) - len(set(content))
    written = 0

    # open output file
    out = open(output_json_file, "w")

    # open json brackets
    out.write('{"year": "2018", "names": [')

    content = list(set(content))
    for idx, name in enumerate(content):
        if (idx % 5000 == 0):
            out.write('\n')
        if '@' in name or '(' in name:
            written += 1

            # write name to file
            if name == content[-1]:
                out.write('"' + name + '"')
            else:
                out.write('"' + name + '", ')

        else:
            skipped += 1

    # close json brackets
    out.write(']}')

    print('Wrote ' + str(written) + ' names.')
    print('Skipped ' + str(skipped) + ' doubles and bad formed names.')

    out.close()


def main():
    merge_json_files(['name-lists/........json',
                      'name-lists/........json',
                      'name-lists/........json',
                      'name-lists/........json',
                      'name-lists/........json'],
                     'female_names.json')


if __name__ == '__main__':
    main()
