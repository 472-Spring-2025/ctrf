import sys
import os

# Get the absolute path of the directory containing the module
from main_method import main # type: ignore
import pytest

def test_file_out():
    main("input/input-2.txt")
    actualfile = open("../code-example-dojo/dojo.yml" , "r")
    expectedfile = open("input/input-2.txt" , "r")
    
    id_actual = actualfile.readline().strip().split(":")[1].strip()
    name_actual = actualfile.readline().strip().split(":")[1].strip()
    description_actual = actualfile.readline().strip().split(":")[1].strip()
    type_actual = actualfile.readline().strip().split(":")[1].strip()
    password_actual = actualfile.readline().strip().split(":")[1].strip()
    actualfile.readline()
    award_actual = actualfile.readline().strip().split(":")[1].strip()
    image_actual = actualfile.readline().strip().split(":")[1].strip()
    actualfile.readline() 
    modules_actual = []
    condition = True
    while condition:
        module = actualfile.readline()
        if module == "":
            condition = False
        else:
            module = module.split(":")[1].strip()
            modules_actual.append(module)

    assert id_actual == expectedfile.readline().strip()
    assert name_actual == expectedfile.readline().strip()
    assert description_actual == expectedfile.readline().strip()
    assert type_actual == expectedfile.readline().strip()
    assert password_actual == expectedfile.readline().strip()
    assert award_actual == expectedfile.readline().strip() 
    image = expectedfile.readline().strip()
    assert image_actual == image or image_actual == "pwncollege/challenge-simple"
    modules = []
    condition = True
    while condition:
        module = expectedfile.readline().strip() 
        if module == "":
            condition = False
        else:
            modules.append(module)
    assert modules_actual == modules
    
    