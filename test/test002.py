import sys
sys.path.append("../")
import logging
from encryptpy import SOEncryptPy

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    ignored = ['.git', '__pycache__', '.vscode', 'build']
    ignore_pf = ['main.py']

    so_ep = SOEncryptPy('/home/sk/project/test/encrypted_python', 
                        '/home/sk/project/test/build', 
                        ignored, ignore_pf)
                        
    so_ep.execute()