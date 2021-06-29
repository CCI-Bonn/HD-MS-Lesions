# Installation instructions
## Installation requirements
ms-lesions only runs on Linux with python3.6 [^1].
You need a pytorch capable GPU with 4GB of GPU memory to run ms-lesions.

[^1]: (other versions might work after downloading the [weights](https://zenodo.org/record/4915908) manually and extracting them in the directory specified by `paths.py`

1) We strongly recommend you install ms-lesions in a separate python virtual environment. [Here is a quick how-to for Ubuntu.](https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/)
2) Once you set up the environment (and activated it)
3) Change the directory to the directory containing `ms-lesions`
4) Install ms-lesions with pip: `pip install ms-lesions` (or change directory into ms-lesions `cd ms-lesions` and call `pip install .`)
5) Done

```
# With virtualenv
virtualenv ms-lesions-env --python=python3.6
source ms-lesions-env/bin/activate

git clone {ms-lesions-repo}
pip install ms-lesions/
```
```
# Without virtualenv
git clone {ms-lesions-repo}
pip3 install ms-lesions/
```

This will install ms_lesions commands directly onto your system (or the virtualenv). You can use them from anywhere (when the virtualenv is active).

# Usage
When running ms_lesions for the first time the weights for the nnUNet model will be downloaded automatically and saved to the home directory.\
Should you want to change the location where weights are to be stored edit the file located in `/<YOUR_PATH>/ms-lesions/ms_lesions/paths.py`

## Run ms-lesions
ms-lesions provides four main scripts: `ms_lesions_predict` and `ms_lesions_predict_folder` for cases where contrast enhanced imaging was taken.<br>
Automatic segmentations for CE and Edema lesions are predicted for the respective cases.

Cases that were imaged without contrast enhancing use `ms_lesions_noT1ce_predict` and `ms_lesions_noT1ce_predict_folder`. <br>
For these cases only edema lesions are predicted.

### Preparing data to predict
The models take multiple modalities as input, which have to be formatted in a nnUNet style fashion (i.e. `{IMAGE_ID}_{MODALITY_ID}.nii.gz`).
See [original nnUNet docu](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/dataset_conversion.md) for more information about that.
The models trained with contrast enhancing modality expect the IDS to be: `{T1: 0000, T1CE: 0001, T2: 0002, FLAIR: 0003}`.
The model trained __without__ the contrast enhancing modality expects the IDS to be: `{T1: 0000, T2: 0001, FLAIR: 0002}`. <br>
When running inference we ask the user once to verify this (can be skipped by using `--skip_modality_check 1`).

### Predicting a single case
`ms_lesions_predict` and `ms_lesions_noT1ce_predict` can be used to predict a single image. <br> 
This can be useful for exploration or if the number of cases to be procesed is low. Examplary use of it:

`ms_lesions_predict -i INPUT_DIRECTORY -id IMAGE_ID -o OUTPUT_DIR -oid OUTPUT_ID`

`IMAGE_ID` can be either the identifier before the `MODALITY_ID` or one image of the modalities.
`OUTPUT_DIR` is the output directory to save the image to, if it does not exist it will be created.
`OUTPUT_ID` is an _optional_ name for the output, if not given the input image ID will be used instead.

For further information use the help option that comes with each command, providing a detailed explanation. (e.g. `ms_lesions_predict --help`).

### Predicting multiple cases
`ms_lesions_predict_folder` / `ms_lesions_noT1ce_predict_folder` is useful for batch processing, especially if the number of cases to be processed is large. By 
interleaving preprocessing, inference and segmentation export we can speed up the prediction significantly. Furthermore, 
the pipeline is initialized only once for all cases, again saving a lot of computation and I/O time.  Here is how to use it:

`ms_lesions_predict_folder -i INPUT_FOLDER -o OUTPUT_FOLDER`

INPUT_FOLDER must contain nifti images (.nii.gz). The results will be written to the OUTPUT_FOLDER (with the same file names).
 If the output folder does not exist it will be created.