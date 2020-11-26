from typing import Dict, Any
from mlpipeline.Utils import get_code_text_from_object, get_hash_of_text
import inspect

class BaseNode:
    """
    A class to represent a single block of operation on data: data generation, transformation or even prediction

    ...

    Attributes
    ----------
    config : Dict[str, Any], optional
        hyperparameters for this node

    Methods
    -------
    run(input: Dict[str, Any]):
        Run relevant computations on this node

    hash():
        Gets the hash value calculated from config and the code of this class
    
    name():
        Gets the name of class for whom this object is instantiated
    
    """
    def __init__(self, config: Dict[str, Any] = {}):
        """
        Constructs all the necessary attributes for the BaseNode object.

        Parameters
        ----------
            config : Dict[str, Any], optional
                hyperparameters for this node
        """
        self.config = config

    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run relevant computations on this node

        Parameters
        ----------
        input : Dict[str, Any]
            All input data required to run the computation

        Returns
        -------
        out : Dict[str, Any]
            Output in the same format as the input
        """
        raise NotImplementedError

    def hash(self):
        """
        Gets the hash value calculated from config and the code of this class.

        This is required to uniquely identify a node and save the results for the same. This value will change if either the config or the code correspoding to the class changes

        Parameters
        ----------
        None

        Returns
        -------
        hashvalue : str
            Hash value calculated from config and the code of this class.
        """
        
        try:
            str_config = str(self.config)
        except:
            raise(TypeError('Unable to convert your config to string! This is necessary to calculate the hash for comparing duplicate calls.'))
        
        str_class_code = get_code_text_from_object(self)
        
        # Calculate hash for config as well as the code of the class
        hash_config = get_hash_of_text(str_config)
        hash_class_code = get_hash_of_text(str_class_code)

        # Calculate the combined hash
        return get_hash_of_text(hash_config + hash_class_code)

    def name(self):
        """
        Gets the name of class for whom this object is instantiated.

        We use it to create suitable directory for storing the content of this node. The name of the folder is {Node class name}_{hash value of the class's code}

        Parameters
        ----------
        None

        Returns
        -------
        classname : str
            Name of class for whom this object is instantiated.
        """
        
        return type(self).__name__