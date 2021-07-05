# HD-MS-Lesions

## Introduction

This repository provides easy to use access to our HD-MS-Lesions brain segmentation tool.
HD-MS-Lesions is the result of a joint project between the Department of Neuroradiology at the Heidelberg University Hospital, Germany and the Division of Medical Image Computing at the German Cancer Research Center (DKFZ) Heidelberg, Germany.
If you are using HD-MS-Lesions, please cite the following publications:

1. Brugnara, G., Isensee, F., Neuberger, U. et al. Automated volumetric assessment with artificial neural networks might enable a more accurate assessment of disease burden in patients with multiple sclerosis.
   Eur Radiol 30, 2356–2364 (2020). https://doi.org/10.1007/s00330-019-06593-y
   
2. Isensee, F., Jaeger, P. F., Kohl, S. A., Petersen, J., & Maier-Hein, K. H. (2020). nnU-Net: a self-configuring method 
for deep learning-based biomedical image segmentation. Nature Methods, 1-9.


HD-MS-Lesions was developed with 416 patients with clinically diagnosed MS at any disease stage,
treated at the Heidelberg University Hospital (Heidelberg, Germany) and who underwent standardized
MRI at the Department of Neuroradiology in the period from January 2010 to December 2016. The patients were assigned to either training or test set with a 4:1 ratio.
Specifically, the training set consisted of n = 334 patients (with n = 334 MRI exams, i.e.,one exam per patient) at any point in the disease course,
whereas the longitudinal test set consisted of n = 88 patients (with n = 266 MRI exams, i.e., acquired at multiple time points for each patient (mean of 3 scans per patient (range 2–8)).

MRI exams were acquired with a 3-T MR imaging system (Magnetom Verio, Skyra or Trio TIM; Siemens Healthcare) and a 12-channel head matrix coil,
and included 3D MPRAGE T1-weighted images before (T1-w) and after (cT1-w) the contrast agent administration as well as 2D axial fluid-attenuated inversion recovery (FLAIR)
and 2D axial T2-weighted (T2-w) images. For acquisition parameters checkout the first paper ([Brugnara et al. 2020](https://doi.org/10.1007/s00330-019-06593-y)).

Given these modalities we provide two models that are capable to predict MS Lesions for patients:
1. For patients imaged with T1-weighted, contrast enhanced T1-weighted, T2-weighted and FLAIR sequence we predict ce and T2/FLAIR lesions,  
2. for patients imaged with T1-weighted, T2-weighted and FLAIR sequence we predict only T2/FLAIR lesions.


## Installation Instructions

### Installation Requirements
HD-MS-lesions only runs on Linux with python3.
Supported python3 versions are python3.6. Python 3.9 doesn't work as downloading of weights breaks. (Might work after downloading the [weights](https://zenodo.org/record/4915908) manually and extracting them in the directory specified by `paths.py`).
In order to run a pc with a GPU with at least 4 GB of VRAM and cuda/pytorch support is required. Running the prediction on CPU is not supported.

### Installation with Pip
Installation with pip is currently not supported but will be added soon.

### Manual installation
We generally recommend to create a new virtualenv for every project that is installed so package dependencies don't get mixed.
To test if virtualenv is installed call `virtualenv --version`. This will return something like this: `virtualenv 20.0.17 from <SOME_PATH>` should it be installed.
([Should it not be installed follow this how-to to install it (Optional).](https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/))

#### Installing with a virtualenv
```shell
# With virtualenv
virtualenv HD-MS-Lesions-env --python=python3.6  # Creates a new Virtual environment 
source HD-MS-Lesions-env/bin/activate  # Activates the environment

git clone git@github.com:NeuroAI-HD/HD-MS-Lesions.git  # Clones the Repository
pip install HD-MS-Lesions/  # Install the repository for the current virtualenv
```
#### Installing without virtualenv
```shell
# Without virtualenv
git clone git@github.com:NeuroAI-HD/HD-MS-Lesions.git  # Clones the repository
pip3 install HD-MS-Lesions/  # Installs the repository for the python3 interpreter
```

This will install `HD-MS-Lesions` commands directly onto your system (or the virtualenv). You can use them from anywhere (when the virtualenv is active).

## How to use it
Using HD-MS-Lesions is straight forward. After installing you can call `ms_lesions_predict` or `ms_lesions_predict_folder` to predict cases imaged with all four MRI modalities or
call `ms_lesions_noT1ce_predict` or `ms_lesions_noT1ce_predict_folder` to predict cases that are imaged with T1-weighted, T2-weighted and FLAIR MRI sequence.

When predicting cases with all modalities the model will predict CE and Edema lesions, whereas only Edema lesions are predicted for the model without cT1 modality.


As these commands are called for the first time the weights for the nnUNet model will be downloaded automatically and saved to your home directory.
Should you want to change the location where weights are to be stored edit the file located in `/<YOUR_PATH>/HD-MS-Lesions/ms_lesions/paths.py`.

## Prerequisites
HD-MS-Lesions was trained with three/four MRI modalities: T1, (optional) constrast-enhanced T1, T2 and FLAIR.

All input files must be provided as nifti (.nii.gz) files containing 2D or 3D MRI image data.
Sequences with multiple temporal volumes (i.e. 4D sequences) are not supported (however can be split upfront into the individual temporal volumes using fslsplit1).
- T1 inputs must be a T1-weighted sequence before contrast-agent administration (T1-w) acquired as 2D with axial orientation (e.g. TSE) or as 3D (e.g. MPRAGE)
- cT1 inputs must be a T1-weighted sequence after contrast-agent administration (cT1-w) acquired as 2D with axial orientation (e.g. TSE) or as 3D (e.g. MPRAGE)
- T2 inputs must be a T2-weighted sequence (T2-w) acquired as 2D
- FLAIR inputs must be a fluid attenuated inversion recovery (FLAIR) sequence acquired as 2D with axial orientation (e.g. TSE). A 3D acquisition (e.g. 3D TSE/FSE) may work as well.

(These specifications are in line with the consensus recommendations for a standardized brain tumor imaging protocol in clinical trials - see Ellingson et al. Neuro Oncol. 2015 Sep;17(9):1188-98 - www.ncbi.nlm.nih.gov/pubmed/26250565)

Input files must contain 3D images; Sequences with multiple temporal volumes (i.e. 4D sequences) are not supported (however can be splitted upfront into the individual temporal volumes using fslsplit1).

All input files must match the orientation of standard MNI152 template and must be brain extracted and co-registered. All non-brain voxels must be 0. To ensure that these pre-processing steps are performed correctly you may adhere to the following example:

#### Reorient MRI sequences to standard space
```shell
fslreorient2std T1.nii.gz T1_reorient.nii.gz
fslreorient2std CT1.nii.gz CT1_reorient.nii.gz
fslreorient2std T2.nii.gz T2_reorient.nii.gz
fslreorient2std FLAIR.nii.gz FLAIR_reorient.nii.gz
```

#### The following is the recommended workflow for FSL5. There is a better way to do this but this requires FSL6 (see below)

```shell
# perform brain extraction using HD-BET (https://github.com/MIC-DKFZ/HD-BET)
hd-bet -i T1_reorient.nii.gz
hd-bet -i CT1_reorient.nii.gz
hd-bet -i T2_reorient.nii.gz
hd-bet -i FLAIR_reorient.nii.gz 

# register all sequences to T1
fsl5.0-flirt -in CT1_reorient_bet.nii.gz -ref T1_reorient_bet.nii.gz -out CT1_reorient_bet_reg.nii.gz -dof 6 -interp spline
fsl5.0-flirt -in T2_reorient_bet.nii.gz -ref T1_reorient.nii.gz -out T2_reorient_bet_reg.nii.gz -dof 6 -interp spline
fsl5.0-flirt -in FLAIR_reorient_bet.nii.gz -ref T1_reorient.nii.gz -out FLAIR_reorient_bet_reg.nii.gz -dof 6 -interp spline

# reapply T1 brain mask (this is important because HD-MS-Lesions expects non-brain voxels to be 0 and the registration process can introduce nonzero values
# T1_BRAIN_MASK.nii.gz is the mask (not the brain extracted image!) as obtained from HD-Bet
fsl5.0-fslmaths CT1_reorient_bet_reg.nii.gz -mas T1_BRAIN_MASK.nii.gz CT1_reorient_bet_reg.nii.gz
fsl5.0-fslmaths T2_reorient_bet_reg.nii.gz -mas T1_BRAIN_MASK.nii.gz T2_reorient_bet_reg.nii.gz
fsl5.0-fslmaths FLAIR_reorient_bet_reg.nii.gz -mas T1_BRAIN_MASK.nii.gz FLAIR_reorient_bet_reg.nii.gz
```

#### This is how to do it with FSL6:
```shell
# run hd bet
hd-bet -i T1_reorient.nii.gz -o t1_bet.nii.gz -s 1
hd-bet -i CT1_reorient.nii.gz -o ct1_bet.nii.gz
hd-bet -i T2_reorient.nii.gz -o t2_bet.nii.gz
hd-bet -i FLAIR_reorient.nii.gz -o flair_bet.nii.gz

# register brain extracted images to t1, save matrix
flirt -in ct1_bet.nii.gz -out ct1_bet_reg.nii.gz -ref t1_bet.nii.gz -omat ct1_to_t1.mat -interp spline -dof 6 &
flirt -in t2_bet.nii.gz -out t2_bet_reg.nii.gz -ref t1_bet.nii.gz -omat t2_to_t1.mat -interp spline -dof 6 &
flirt -in flair_bet.nii.gz -out flair_bet_reg.nii.gz -ref t1_bet.nii.gz -omat flair_to_t1.mat -interp spline -dof 6 &
wait

# we are only interested in the matrices, delete the other output images
rm ct1_bet.nii.gz t2_bet.nii.gz flair_bet.nii.gz
rm ct1_bet_reg.nii.gz t2_bet_reg.nii.gz flair_bet_reg.nii.gz

# now apply the transformation matrices to the original images (pre hd-bet)
flirt -in CT1_reorient.nii.gz -out ct1_reg.nii.gz -ref t1_bet.nii.gz -applyxfm -init ct1_to_t1.mat -interp spline &
flirt -in T2_reorient.nii.gz -out t2_reg.nii.gz -ref t1_bet.nii.gz -applyxfm -init t2_to_t1.mat -interp spline &
flirt -in FLAIR_reorient.nii.gz -out flair_reg.nii.gz -ref t1_bet.nii.gz -applyxfm -init flair_to_t1.mat -interp spline &
wait

# now apply t1 brain mask to all registered images
fslmaths ct1_reg.nii.gz -mas t1_bet_mask.nii.gz CT1_reorient_reg_bet.nii.gz & # t1_bet_mask.nii.gz was generated by hd-bet (see above)
fslmaths t2_reg.nii.gz -mas t1_bet_mask.nii.gz T2_reorient_reg_bet.nii.gz & # t1_bet_mask.nii.gz was generated by hd-bet (see above)
fslmaths flair_reg.nii.gz -mas t1_bet_mask.nii.gz FLAIR_reorient_reg_bet.nii.gz & # t1_bet_mask.nii.gz was generated by hd-bet (see above)
wait

# done
```
After applying this example you would use T1_reorient.nii.gz, CT1_reorient_reg_bet.nii.gz, T2_reorient_reg_bet.nii.gz and FLAIR_reorient_reg_bet.nii.gz to proceed.

## Run HD-MS-Lesions
HD-MS-Lesions provides four main scripts: `ms_lesions_predict` and `ms_lesions_predict_folder` for cases where contrast T1, cT1, T2 and FLAIR modalities were imaged.\
For these cases automatic segmentations for CE and Edema lesions are predicted.

Cases that were imaged with T1, T2 and FLAIR can be automatically segmented using `ms_lesions_noT1ce_predict` and `ms_lesions_noT1ce_predict_folder`.\
For these cases only Edema lesions are predicted.

### Predicting cases
The models take multiple modalities as input, which have to be formatted in a nnUNet style fashion (i.e. `{ARBITRARY_IMAGE_ID}_{MODALITY_ID}.nii.gz`).
See [original nnUNet docu](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/dataset_conversion.md) for more information about that.

For cases that are imaged with T1, cT1, T2 and FLAIR the `MODALITY_ID` has to be: `{T1: 0000, cT1: 0001, T2: 0002, FLAIR: 0003}`, for the corresponding modality.
For cases imaged __without__ cT1 modality the `MODALITY_ID` has to be: `{T1: 0000, T2: 0001, FLAIR: 0002}`, for the corresponding modalities.
The user has to confirm this when running or skip the check by using the `--skip_modality_check 1` option. 

### Predicting a single case
`ms_lesions_predict` and `ms_lesions_noT1ce_predict` can be used to predict a single case. 
This can be useful for exploration or if the number of cases to be procesed is low. Exemplary use of it:

`ms_lesions_predict -i INPUT_DIR -id ARBITRARY_IMAGE_ID -o OUTPUT_DIR -oid OUTPUT_ID`

`INPUT_DIR` is the path to the directory that contains the images of the patient.
`ARBITRARY_IMAGE_ID` can be either only the identifier or any image with/without the `MODALITY_ID`.
`OUTPUT_DIR` is the path to the output directory to save the image to, if it does not exist all directories that are missing will be created.
`OUTPUT_ID` is an _optional_ name for the output, if not given the input image ID will be used instead.

For further information use the help option that comes with each command, providing a detailed explanation. (e.g. `ms_lesions_predict --help`).

### Predicting multiple cases
`ms_lesions_predict_folder` / `ms_lesions_noT1ce_predict_folder` is useful for batch processing, especially if the number of cases to be processed is large.
By interleaving preprocessing, inference and segmentation export we can speed up the prediction significantly. Furthermore, the pipeline is initialized only once for all cases,
again saving a lot of computation and I/O time.  Here is how to use it:

`ms_lesions_predict_folder -i INPUT_DIR -o OUTPUT_DIR`

`INPUT_DIR` must contain nifti images (.nii.gz). The results will be written to the `OUTPUT_DIR` (with the same file names).
 If the output folder does not exist it will be created.
