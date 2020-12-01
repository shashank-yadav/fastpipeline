import inspect
import hashlib
import logging
import glob
from termcolor import colored
from os import path
import logging

logging.basicConfig(level=logging.NOTSET, format='%(levelname)s - %(message)s')

def get_code_text_from_object(obj: object):
    '''Extract code text of a class from its object that can be used to identify changes made to that class'''
    
    # Try extracting class of the object
    try:
        class_of_obj = obj.__class__
    except Exception as e:
        raise(TypeError('Unable to get the class of object %s'.format(obj)))

    source_text = inspect.getsource(class_of_obj)
    return source_text


def get_hash_of_text(text):
    '''Take hash that can be used to compare the two pieces of text'''
    
    hashval = hashlib.md5(text.encode())
    return hashval.hexdigest()


def colored_logging(first_statement, second_statement, color1='yellow',  color2='cyan'):
    '''Normal logging is hard to read, we're printing with colors'''
    logging.info( colored(first_statement, color1) + colored(second_statement, color2) )


def get_result_file(folderpath):
    '''A helper function to find the file that contains the result of computations done on a node'''
    possible_result_files = glob.glob(path.join(folderpath, 'result_*.pkl'))
    if len(possible_result_files) != 1:
        return None
    else:
        return possible_result_files[0]
