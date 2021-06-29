#    Copyright 2021 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from batchgenerators.utilities.file_and_folder_operations import subfiles

from ms_lesions.utils import blockPrint, enablePrint

blockPrint()
from nnunet.inference.predict import predict_cases

enablePrint()
import argparse
from ms_lesions.paths import folder_with_t1ce_parameter_files
from ms_lesions.setup_ms_lesions import maybe_download_weights
from ms_lesions.prepare_input_args import prepare_input_args_t1ce


def main():
    parser = argparse.ArgumentParser(description="This script will allow you to predict MS lesions of all cases in a folder"
                                                 " that come with the following modalities (with index):\n"
                                                 "T1 (0000), T1ce (0001), T2 (0002), FLAIR (0003)"
                                                 "Should you not have T1CE imaging modality use the `ms_lesions_noT1ce_predict` or `ms_lesions_noT1ce_predict_folder` function."
                                                 "The different modalities should follow nnUNet naming convention `{SOME_ID}_{ModalityID}.nii.gz`"
                                                 "Given the identifier and the folder containing it, a prediction of contrast enhancing and edema lesions are provided."
                                                 "To predict a single case, please use `ms_lesions_predict`")
    parser.add_argument("-i", "--input_folder", type=str, required=True,
                        help="Folder containing input files (no nested folder structure supported). All .nii.gz files in this folder are attempted to be processed.")
    parser.add_argument("-o", "--output_folder", type=str, required=True,
                        help="output folder. This is there the resulting segmentations will be saved. Cannot be the "
                             "same folder as the input folder. If output_folder does not exist "
                             "it will be created")
    parser.add_argument("-p", "--processes", default=4, type=str, required=False,
                        help="number of processes for data preprocessing and nifti export. You should not have to "
                             "touch this. So don't unless there is a clear indication that it is required. Default: 4")
    parser.add_argument('--keep_existing', default=True, required=False, action='store_false',
                        help="Set to False to overwrite segmentations in output_folder. If true continue where you left off "
                             "(useful if something crashes). If this flag is not set, all segmentations that may "
                             "already be present in output_folder will be kept.")
    parser.add_argument("-mod", "--skip_modality_check", type=bool, required=False, default=0,
                        help="Optional: Skips asking if the modalities are provided as expected", nargs='?')

    args = parser.parse_args()
    input_folder = args.input_folder
    output_folder = args.output_folder
    processes = args.processes
    keep_existing = args.keep_existing
    skip_modality = args.skip_modality_check

    maybe_download_weights()

    # we must generate a list of input filenames
    nii_files = subfiles(input_folder, suffix='.nii.gz', join=False)
    unique_ids = list(set([file[:-12] for file in nii_files]))

    input_image_names = []
    output_names = []
    for unique_id in unique_ids:
        input_image_mod_names, output_name = prepare_input_args_t1ce(input_dir=input_folder,
                                                                     input_id=unique_id,
                                                                     output_dir=output_folder,
                                                                     output_id=None,
                                                                     skip_modality_confirmation=skip_modality)
        input_image_names.append(input_image_mod_names)
        output_names.append(output_name)

    predict_cases(model=folder_with_t1ce_parameter_files,
                  list_of_lists=input_image_names,
                  output_filenames=output_names,
                  folds=(0, 1, 2, 3, 4),
                  save_npz=False,
                  num_threads_preprocessing=processes,
                  num_threads_nifti_save=processes,
                  segs_from_prev_stage=None,
                  do_tta=True,
                  mixed_precision=None,
                  overwrite_existing=not keep_existing,
                  all_in_gpu=False)


if __name__ == "__main__":
    main()
