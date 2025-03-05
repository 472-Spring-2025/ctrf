# content of test_sample.py
import os
import sys
from main_method import build_repo_yml, get_module_level, RepositoryLevelYmlFile # type: ignore
import pytest

def check_module(filename):
    input = open(filename, "r")
    expected_input = open(filename, "r")
    build_repo_yml(expected_input)
    
    rlyf = build_repo_yml(input)
    modules = get_module_level(input, rlyf)
    count = 0
    
    for module in modules:

        assert module.name == rlyf.modules[count]
        assert module.id == expected_input.readline().strip()
        assert module.description == expected_input.readline().strip()
        for challenge in module.challenges:
            assert challenge.name == expected_input.readline().strip()
        count += 1
        expected_input.readline().strip()
        

def test_module():
    check_module("input/input-2.txt")
