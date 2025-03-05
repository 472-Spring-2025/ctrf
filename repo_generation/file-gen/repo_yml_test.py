# 
import sys
import os
from main_method import build_repo_yml, RepositoryLevelYmlFile # type: ignore
import pytest

def check_input(filepath):
    inputfile = open(filepath, "r")
    expectedfile = open(filepath , "r")
    
    id = expectedfile.readline().strip()
    name = expectedfile.readline().strip()
    description = expectedfile.readline().strip()
    type = expectedfile.readline().strip()
    password = expectedfile.readline().strip()
    award = expectedfile.readline().strip() 
    image = expectedfile.readline().strip() 
    modules = []
    condition = True
    while condition:
        module = expectedfile.readline().strip() 
        if module == "":
            condition = False
        else:
            modules.append(module)
    if(id == "" or name == "" or len(modules) == 0):
        with pytest.raises(ValueError):
            build_repo_yml(inputfile)
        return
    else:
        my_file = build_repo_yml(inputfile)
    assert my_file.id == id
    assert my_file.name == name
    assert my_file.description == description
    assert my_file.type == type or my_file.type == "more"
    assert my_file.password == password
    assert my_file.award == award
    assert (my_file.image == image or my_file.image == "pwncollege/challenge-simple")
    iterator = 0
    for module in my_file.modules:
        assert module == modules[iterator]
        iterator += 1

def test_files():
    check_input("input/repo-only/repo-input-1.txt")
    check_input("input/repo-only/repo-input-2.txt")
    check_input("input/repo-only/repo-input-3.txt")
    check_input("input/repo-only/repo-input-4.txt")
    check_input("input/repo-only/repo-input-5.txt")





