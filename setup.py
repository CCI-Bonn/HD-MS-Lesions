from setuptools import setup


setup(name='ms_lesions',
      version='1.0',
      packages=["ms_lesions"],
      description='Tool for multiple sclerosis segmentation. This is the result of a joint project between the Department of '
                  'Neuroradiology at the Heidelberg University Hospital and the Division of Medical Image Computing at '
                  'the German Cancer Research Center (DKFZ). See readme.md for more information',
      # TODO: Here the URL and the Description need to change
      url='https://github.com/NeuroAI-HD/ToBeDefined',
      python_requires='>=3.6',
      author='Tassilo Wald',
      author_email='tassilo.wald@dkfz-heidelberg.de',
      license='Apache 2.0',
      zip_safe=False,
      install_requires=[
          'torch',
          'nnunet>1.0',
          'batchgenerators'
      ],
      entry_points={
          'console_scripts': [
                'ms_lesions_predict = ms_lesions.ms_lesions_predict:main',
                'ms_lesions_predict_folder = ms_lesions.ms_lesions_predict_folder:main',
                'ms_lesions_noT1ce_predict =  ms_lesions.ms_lesions_noT1ce_predict:main',
                'ms_lesions_noT1ce_predict_folder = ms_lesions.ms_lesions_noT1ce_predict_folder:main'
        ],
      },
      classifiers=[
          'Intended Audience :: Science/Research',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
          'Operating System :: Unix'
      ]
      )

