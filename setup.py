from setuptools import setup, find_packages

setup(
    name="question-generator",
    version="0.1",
    packages=find_packages(),
    package_dir={'': '.'},
    install_requires=[
        'PyPDF2>=3.0.0',
        # other dependencies here
    ],
) 