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

from ms_lesions.utils import blockPrint, enablePrint
blockPrint()
from nnunet.inference.predict import predict_cases
enablePrint()
import argparse
from ms_lesions.paths import folder_with_not1ce_parameter_files
from ms_lesions.prepare_input_args import prepare_input_args_not1ce
from ms_lesions.setup_ms_lesions import maybe_download_weights


def main():
    parser = argparse.ArgumentParser(description="This script will allow you to predict MS lesions of a single case coming with modalities (with index):\n"
                                                 "T1 (0000), T2 (0001), FLAIR (0002)"
                                                 "The different modalities should follow nnUNet naming convention `{SOME_ID}_{ModalityID}.nii.gz`"
                                                 "Given the identifier and the folder containing it a prediction of edema lesions are provided."
                                                 "To predict all cases in a directory, please use ms_lesions_noT1ce_predict_folder (this one "
                                                 "will be substantially faster for multiple cases because we can "
                                                 "interleave preprocessing, GPU prediction and nifti export."
                                                 "Should you have access to T1CE modality please use the `ms_lesions_predict` or `ms_lesions_predict_folder` function.")

    parser.add_argument("-i", "--input_folder", type=str, required=True,
                        help="Directory the input file is in")
    parser.add_argument("-id", type=str, required=True,
                        help="Identifier of the input file (if the file ends with .nii.gz id is extracted automatically."
                             " All expected modalities of the id must exist.")
    parser.add_argument("-o", "--output_folder", type=str, required=True,
                        help="Directory to save the output files to.")
    parser.add_argument("-oid", "--output_id", type=str, required=False,
                        help="Optional: Output file name (If omitted uses identifier)", nargs='?')
    parser.add_argument("-mod", "--skip_modality_check", type=bool, required=False, default=0,
                        help="Optional: Skips asking if the modalities are provided as expected", nargs='?')

    args = parser.parse_args()
    inp_dir = args.input_folder
    inp_id: str = args.id
    output_dir = args.output_folder
    output_id = args.output_id
    skip_modality = args.skip_modality_check

    if inp_id.endswith(".nii.gz"):
        inp_id = inp_id[:-12]  # -8 for concatenating .nii.gz

    maybe_download_weights()
    input_paths, output_file = prepare_input_args_not1ce(inp_dir, inp_id, output_dir, output_id, skip_modality)

    predict_cases(folder_with_not1ce_parameter_files, [input_paths], [output_file], (0, 1, 2, 3, 4), False, 1,
                  1, None, True, None, True)


if __name__ == "__main__":
    main()

