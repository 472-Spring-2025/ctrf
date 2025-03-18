# 
import sys
import os
import yaml
from main_method import build_repo_yml, RepositoryLevelYmlFile # type: ignore
import pytest

def check_input(filepath):
    inputfile = open(filepath, "r")
    input_source_actual = yaml.safe_load(inputfile)
    expectedfile = open(filepath , "r")
    input_source_expected = yaml.safe_load(expectedfile)
    
    
    id = input_source_expected["id"]
    name = input_source_expected["name"]
    description = input_source_expected["description"]
    type = input_source_expected["type"]
    password = input_source_expected["password"]
    award = input_source_expected["award"] 
    image = input_source_expected["image"]
    modules = input_source_expected["modules"]
    
    if(id == None or name == None or modules == None):
        with pytest.raises(ValueError):
            build_repo_yml(input_source_actual)
        return
    else:
        my_file = build_repo_yml(input_source_actual)
    assert my_file.id == id
    assert my_file.name == name
    assert my_file.description == description
    assert my_file.type == type or my_file.type == "more"
    assert my_file.password == password
    assert my_file.award == award
    assert (my_file.image == image or my_file.image == "pwncollege/challenge-simple")
    iterator = 0
    for module in my_file.modules:
        assert module == modules[iterator][0]
        iterator += 1

def test_files():
    check_input("input/repo-only/repo-input-1.yml")
    check_input("input/repo-only/repo-input-2.yml")
    check_input("input/repo-only/repo-input-3.yml")
    check_input("input/repo-only/repo-input-4.yml")
    check_input("input/repo-only/repo-input-5.yml")





