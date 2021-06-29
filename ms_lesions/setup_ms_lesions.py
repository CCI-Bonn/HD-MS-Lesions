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

from urllib.request import urlopen
from batchgenerators.utilities.file_and_folder_operations import *
from ms_lesions.paths import folder_with_t1ce_parameter_files, folder_with_not1ce_parameter_files, base_path
import shutil
import zipfile


def maybe_download_weights():
    # check if models are available
    all_good = True
    for f in range(5):
        if not isfile(join(folder_with_t1ce_parameter_files, 'fold_%d' % f, "model_final_checkpoint.model")) or not \
                isfile(join(folder_with_t1ce_parameter_files, 'fold_%d' % f, "model_final_checkpoint.model.pkl")) or not \
                isfile(join(folder_with_not1ce_parameter_files, 'fold_%d' % f, "model_final_checkpoint.model")) or not \
                isfile(join(folder_with_not1ce_parameter_files, 'fold_%d' % f, "model_final_checkpoint.model.pkl")):
            all_good = False
            break
    if all_good:
        return

    import http.client
    http.client.HTTPConnection._http_vsn = 10
    http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

    if isdir(base_path):
        shutil.rmtree(base_path)
    maybe_mkdir_p(base_path)

    out_filename = join(base_path, "parameters.zip")

    url = "https://zenodo.org/record/4915908/files/ms_lesions_weights.zip?download=1"
    print("Downloading", url, "...")
    data = urlopen(url).read()
    with open(out_filename, 'wb') as f:
        f.write(data)

    zipfile.ZipFile(out_filename).extractall(path=base_path)
    os.remove(out_filename)
