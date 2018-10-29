from pathlib import Path
import os

class PathToImages:
    
    path_to_folder = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(os.path.join(path_to_folder, 'static'), 'images')
