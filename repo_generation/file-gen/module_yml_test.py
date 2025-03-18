# content of test_sample.py
import os
import sys
from main_method import build_repo_yml, get_module_level, RepositoryLevelYmlFile # type: ignore
import pytest
import yaml

def check_module(filename):
    input = open(filename, "r")
    input_source = yaml.safe_load(input)
    expected_input = open(filename, "r")
    expected_source = yaml.safe_load(expected_input)
    if input_source["modules"] == None:
        with pytest.raises(ValueError):
            build_repo_yml(input_source)
            return
    for module in input_source["modules"]:
        if module == None or len(module) != 4 or module[0] == None or module[1] == None or module[2] == None or module[3] == None or len(module[3]) == 0:
            with pytest.raises(ValueError):
                rl = build_repo_yml(input_source)
                get_module_level(input_source, rl)
            return
        for challenge in module[3]:
            if challenge[0] == None or challenge[1] == None or len(challenge[1]) == 0:
                with pytest.raises(ValueError):
                    rl = build_repo_yml(input_source)
                    get_module_level(input_source, rl)
                    
                return
            for filepath in challenge[1]:
                try:
                    open(filepath, "r")
                except:
                    with pytest.raises(ValueError):
                        rl = build_repo_yml(input_source)
                        get_module_level(input_source, rl)
                    return

    
    build_repo_yml(expected_source)
    
    rlyf = build_repo_yml(input_source)
    modules = get_module_level(input_source, rlyf)
    modCount = 0
    
    for module in modules:

        assert module.name == rlyf.modules[modCount]
        assert module.id == expected_source["modules"][modCount][1]
        assert module.description == expected_source["modules"][modCount][2]
        chalCount = 0
        for challenge in module.challenges:
            assert challenge.name == expected_source["modules"][modCount][3][chalCount][0]
            assert challenge.files == expected_source["modules"][modCount][3][chalCount][1]
            chalCount += 1
        modCount += 1
        

def test_module():
    check_module("input/module-only/module-input-1.yml")
    check_module("input/module-only/module-input-2.yml")
    check_module("input/module-only/module-input-3.yml")
    check_module("input/module-only/module-input-4.yml")
    check_module("input/module-only/module-input-5.yml")
    check_module("input/module-only/module-input-6.yml")
    check_module("input/module-only/module-input-7.yml")
    check_module("input/module-only/module-input-8.yml")
