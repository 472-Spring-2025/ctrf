from typing import List, Optional
from abc import ABC, abstractmethod
import os
import shutil
from typing import List

baseRepoDir = "../code-example-dojo"

class YmlFile(ABC):
    def __init__(self, id: str, name: str, description: Optional[str] = None):
        if not id or not name or not id.strip() or not name.strip():
            raise ValueError("ID and name are required")
        
        self.id = id
        self.name = name
        self.description = description

    def __str__(self) -> str:
        result = f"id: {self.id}\nname: {self.name}\n"
        if self.description and self.description.strip():
            result += f"description: {self.description}\n"
        return result

class RepositoryLevelYmlFile(YmlFile):
    def __init__(self, id: str, name: str, description: str, type: str = "",
                 password: str = "", award: str = "", image: str = "", 
                 modules: List[str] = None):
        super().__init__(id, name, description)
        
        if not modules:
            raise ValueError("Modules cannot be empty")
        
        if any(not module or not module.strip() for module in modules):
            raise ValueError("Invalid module name")
            
        self.type = "more" if not type.strip() else type
        self.password = password
        self.award = award
        self.image = "pwncollege/challenge-simple" if not image.strip() else image
        self.modules = modules

    def __str__(self) -> str:
        result = super().__str__()
        result += f"type: {self.type}\n"
        
        if self.password.strip():
            result += f"password: {self.password}\n"
            
        if self.award.strip():
            result += f"award:\n emoji: {self.award}\n"
            
        result += f"image: {self.image}\n"
        result += "modules:\n"
        
        for module in self.modules:
            result += f" - id: {module}\n"
        return result

class Challenge:
    def __init__(self, id: str, name: str, files: List[str] = None, parent = None):
        self.id = id
        self.name = name
        self.files = files
        self.parent = parent

    def __str__(self) -> str:
        return f" - id: {self.id}\n name: {self.name}\n"

class ModuleLevelYml(YmlFile):
    def __init__(self, id: str, name: str, description: str, 
                 challenges: List[Challenge]):
        super().__init__(id, name, description)
        self.challenges = challenges

    def __str__(self) -> str:
        result = f"name: {self.name}\n"
        if self.description and not self.description.isspace():
            result += f"description: {self.description}\n"
        result += "challenges:\n"
        for challenge in self.challenges:
            result += str(challenge)
        return result



def build_repo_yml(input_source) -> RepositoryLevelYmlFile:
    #print("Hello! I'm here to help you build your command line CTF.\n")
    #print("What should its ID be? It must be unique (different from the other available CTFs).")
    id = input_source.readline().strip()
    
    #print("What would you like the name of your CTF to be?")
    name = input_source.readline().strip()
    
    #print("Would you like a description? If not, press enter")
    description = input_source.readline().strip()
    
    #print("What will the type be? [course/topic/hidden] or just press enter.")
    type = input_source.readline().strip()
    while type and type not in ["course", "topic", "hidden"]:
        #print("We couldn't determine your response. What will the type be? [course/topic/hidden] or just press enter.")
        type = input_source.readline().strip()
    
    #print("Would you like a password? If not, press enter.")
    password = input_source.readline().strip()
    
    #print("What would you like the award to be? Please enter an emoji")
    award = input_source.readline().strip()
    
    #print("What would you like the image path to be? Press enter for default.")
    image = input_source.readline().strip()
    
    #print("Please enter the names of your modules 1 at a time. Submit a blank name when done.")
    modules = []
    while True:
        module = input_source.readline().strip()
        if not module:
            break
        modules.append(module)
    
    return RepositoryLevelYmlFile(id, name, description, type, password, award, image, modules)

def get_code(input_source, modules: List[ModuleLevelYml]):
    for m in modules:
        for c in m.challenges:
            #print(f'For your module named "{m.name}", what files would you like to use? Input a blank when done.')
            while True:
                file_path = input_source.readline().strip()
                if not file_path:
                    break
                    
                source = os.path.abspath(file_path)
                dest_dir = os.path.join(baseRepoDir, m.name.lower(), c.id)
                dest = os.path.join(dest_dir, os.path.basename(source))
                
                try:
                    shutil.copy2(source, dest)
                except IOError as e:
                    print(f"Error copying file: {e}")

def get_module_level(input_source, rlyf: RepositoryLevelYmlFile) -> List[ModuleLevelYml]:
    module_level_ymls = []
    
    for module in rlyf.modules:
        #print(f'For your module named "{module}", what would you like its ID to be?')
        id = input_source.readline().strip()
        
        #print("Would you like a description? If not, press enter")
        description = input_source.readline().strip()
        
        #print("Please enter the names of your challenges 1 at a time. Submit a blank name when done.")
        challenges = []
        while True:
            challenge = input_source.readline().strip()
            if not challenge:
                break
            challenges.append(Challenge(challenge.lower(), challenge))
        
        module_level_ymls.append(ModuleLevelYml(id, module, description, challenges))
    
    return module_level_ymls

def write_to_files(rlyf: RepositoryLevelYmlFile, module_level_ymls: List[ModuleLevelYml]):
    try:
        # Create main directory
        os.makedirs(baseRepoDir, exist_ok=True)
        print(baseRepoDir)
        
        # Create module directories and their challenge subdirectories
        for mod in module_level_ymls:
            mod_path = os.path.join(baseRepoDir, mod.name.lower())
            os.makedirs(mod_path, exist_ok=True)
            for c in mod.challenges:
                os.makedirs(os.path.join(mod_path, c.id), exist_ok=True)
        
        # Write repository level YAML
        with open(f"{baseRepoDir}/dojo.yml", "w") as repo_out:
            repo_out.write(str(rlyf))
        
        # Write module level YAMLs
        for mod in module_level_ymls:
            with open(f"{baseRepoDir}/{mod.name}/{mod.id}.yml", "w") as mod_out:
                mod_out.write(str(mod))
                
    except Exception as e:
        print(f"Error: {e}")

def main(filename):
    import sys
    # Handle input source (file or stdin)
    if len(sys.argv) > 1:
        try:
            input_source = open(sys.argv[1], 'r')
        except Exception as e:
            if filename:
                input_source = open(filename, 'r')
            else:
                input_source = sys.stdin
    print(input_source)
    try:
        rlyf = build_repo_yml(input_source)
        module_level_ymls = get_module_level(input_source, rlyf)
        write_to_files(rlyf, module_level_ymls)
        get_code(input_source, module_level_ymls)
    finally:
        if input_source != sys.stdin:
            input_source.close()

if __name__ == "__main__":
    
    main(None)
