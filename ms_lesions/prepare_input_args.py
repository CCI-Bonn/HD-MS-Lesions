import os
from batchgenerators.utilities import file_and_folder_operations as file_io
from ms_lesions.paths import folder_with_t1ce_parameter_files, folder_with_not1ce_parameter_files

modality_flag = False
flag = False


def _user_confirm_modalities():
    global flag
    val = input("Do the input images contain the correct modalities? '(y/n)'")
    if val == "y":
        flag = True
        pass
    else:
        print("Please change the order accordingly!")
        exit(0)
    return


def _prepare_input_args(input_dir, input_id, output_dir, output_id, modalities: dict, skip_modality_confirmation: bool):
    """ Loads the input files from input_dir with input_id and the modality after.

    :param input_dir: Input directory containing the input images of all modalities
    :param input_id: Identifier of the modality to load
    :param output_dir: Output path to write the modality to
    :param output_id: Output Name (can be omitted to use the input_identifier instead)
    :param modalities: Dictionary containing the modalities integer key.
    :param skip_modality_confirmation: Skips the input asking if modalities align.
    :return:
    """
    input_paths = []

    modality_values = list(modalities.keys())

    for key, val in modalities.items():
        input_paths.append(os.path.join(input_dir, input_id + "_{:04}.nii.gz".format(key)))

    # Assert all modality files exist!
    input_paths.sort()
    for file_path in input_paths:
        assert os.path.exists(file_path), "Could not find {} in {}. Expect all modalities of the input!".format(os.path.basename(file_path), os.path.dirname(file_path))

    contents_in_dir = os.listdir(input_dir)
    modalities_of_contents = list(set([content.split("_")[-1][:-7] for content in contents_in_dir]))

    global flag

    if flag == False:
        print("Found modalities:")
        for entry in sorted(modalities_of_contents):
            print(entry)

    if flag == False:
        if skip_modality_confirmation:
            pass
        else:
            try:
                assert len(modalities_of_contents) == len(modality_values), f"{len(modality_values)} modalities should exist! Found only {len(modalities_of_contents)}"
                _user_confirm_modalities()
            except AssertionError:
                if len(modalities_of_contents) < len(modality_values):
                    print(f"Not all modalities expected found! Be sure to provide: {modalities}")
                    exit(1)
                else:
                    if flag == False:
                        print("Warning: Found more than the specified modalities!")
                        _user_confirm_modalities()
    else:
        pass

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=False)  # If not exists, creates path to that directory.

    if output_id is not None:
        output_file = os.path.join(output_dir, output_id)
    else:
        output_file = os.path.join(output_dir, input_id)
    if not output_file.endswith(".nii.gz"):
        output_file = output_file + ".nii.gz"

    return input_paths, output_file


def print_expected_modalities(modalities: dict):
    global modality_flag
    if modality_flag == False:
        print("Expecting the 'input modalities' to be in image with 'index':")
        for key, val in modalities.items():
            print(f"{val:7s} \t{key:04}")
        modality_flag = True
    return


def prepare_input_args_t1ce(input_dir, input_id, output_dir, output_id, skip_modality_confirmation):
    plans_file = file_io.load_pickle(os.path.join(folder_with_t1ce_parameter_files, "plans.pkl"))
    modalities = plans_file["modalities"]
    print_expected_modalities(modalities)

    input_paths, output_file = _prepare_input_args(input_dir, input_id, output_dir, output_id, modalities, skip_modality_confirmation)

    return input_paths, output_file


def prepare_input_args_not1ce(input_dir, input_id, output_dir, output_id, skip_modality_confirmation):
    plans_file = file_io.load_pickle(os.path.join(folder_with_not1ce_parameter_files, "plans.pkl"))
    modalities = plans_file["modalities"]
    print_expected_modalities(modalities)

    input_paths, output_file = _prepare_input_args(input_dir, input_id, output_dir, output_id, modalities, skip_modality_confirmation)

    return input_paths, output_file
