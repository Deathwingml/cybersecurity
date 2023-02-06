from setuptools import find_packages, setup
from typing import List

REQUIREMENT_FILE_NAME = "requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements()->List[str]:
    with open(REQUIREMENT_FILE_NAME) as requirements.txt:
        requirement_list = requirement_file.readlines()
    requirement_list = [requirement_name.replace("\n","") for requirement_name in requirement_list]
    
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list



    setup(
        name = "CyberSecurity",
        version = "0.0.1",
        author = "Santosh Singh",
        author_email = "pardesisantoshsingh@gmail.com",
        packages = find_packages(),
        install_requires = get_requirements(),
    )