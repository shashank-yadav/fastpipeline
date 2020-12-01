import os
import pickle as pkl
import json
from os import path
from typing import List, Dict, Any, Tuple
from termcolor import colored

from fastpipeline.base_node import BaseNode
from fastpipeline.Utils import get_hash_of_text, get_code_text_from_object, colored_logging, get_result_file

class Pipeline:
    """
    A class to run operations of serveral nodes in series. Similar to pipeline from sklearn but with a different signature (Using Nodes and returning dictionaries).

    ...

    Attributes
    ----------
    experiment_name : str
        A unique name for the subfolder that'll contain data corresponding to all the nodes present in this pipeline, full path will be [experiments_dir]/[experiment_name]

    experiments_dir : str
        Folder containing all the experiments, full path will be [experiments_dir]/[experiment_name]

    savedir: str
        Full path of folder used for storing data from nodes: [experiments_dir]/[experiment_name]

    nodes : List[BaseNode]
        List of nodes (whose classes are inherited from BaseNode)

    Methods
    -------
    run(input: Dict[str, Any]):
        Run computations on all nodes in order (by calling their run functions) and reuse previously computed results
    
    """
    def __init__(self, experiment_name: str, nodes: List[BaseNode], experiments_dir: str = './experiments'):
        """
        Constructs all the necessary attributes for the Pipeline object.

        Parameters
        ----------
        experiment_name : str
        A unique name for the subfolder that'll contain data corresponding to all the nodes present in this pipeline, full path will be [experiments_dir]/[experiment_name]

        nodes : List[BaseNode]
            List of nodes (whose classes are inherited from BaseNode)

        experiments_dir : str, optional
            Folder containing all the experiments, full path will be [experiments_dir]/[experiment_name]

        """
        self.experiment_name = experiment_name
        self.experiments_dir = experiments_dir
        self.savedir = path.join(self.experiments_dir, experiment_name)
        self.nodes = nodes
        
    def run(self, input: Dict[str, Any]):
        """
        Run computations on all nodes in order (by calling their run functions) and reuse previously computed results.

        For each node we store the following:
        1) Source code of their class
        2) Config for the object
        3) The whole object (pickled)
        4) The pickled result corresponding to each of the inputs

        You'll find (1), (2) and (3) inside [experiments_dir]/[experiment_name]/[node_name]_[node_hash]
        And (4) inside [experiments_dir]/[experiment_name]/[node_name]_[node_hash]/input_[input_hash]/[output_hash].pkl

        Parameters
        ----------
        input : Dict[str, Any]
            All input data required to run the pipeline

        Returns
        -------
        out : Dict[str, Any]
            Output in the same format as the input
        """
        
        # Create a directory for this experiment if not already there
        os.makedirs(self.savedir, exist_ok=True)
        
        colored_logging('\n\n-----PIPELINE STARTED-----\n', '', color1='green')
        colored_logging('Find results of this experiment in: ', self.savedir)
        colored_logging('NOTE: To store the data in any other directory, you can pass different arguments for experiment_name and experiments_dir variables when creating the pipeline object','', color1='red')
        
        for node in self.nodes:
            node_name = node.name()
            node_hash = node.hash()
            # logging.info(colored('Node: %s'%node_name, 'red'))
            colored_logging('------------------------------------------------------------------------------------------','', color1='magenta')
            colored_logging('node: ', node_name+'_'+node_hash)

            # directory to store all the contents of the node
            node_dir = path.join(self.savedir, node_name+'_'+node_hash)
            os.makedirs(node_dir, exist_ok=True)
            colored_logging('storing node data at: ', node_dir)
            
            # store the code for the class corresponding to this node (if it doesn't already exists)
            if node.save_code:
                object_code_filepath = path.join(node_dir, '%s.py'%node_name)
                if not os.path.exists(object_code_filepath):
                    code_text = get_code_text_from_object(node)
                    with open( object_code_filepath, 'w') as f:
                        f.write(code_text)
                    colored_logging('creating source code file: ', object_code_filepath, color2='green')
                else:
                    colored_logging('existing source code file: ', object_code_filepath)
            else:
                colored_logging('not saving the source code for object', '', color1='red')

            # store the object so that it can be analyzed later if needed
            if node.save_object:
                object_pickle_filepath = path.join(node_dir, '%s.pkl'%node_name)
                if not os.path.exists(object_pickle_filepath):
                    try:
                        with open(object_pickle_filepath, 'wb') as f:
                            pkl.dump(node, f)
                    except:
                        raise AttributeError('Object is not picklable')
                    colored_logging('creating pickled object: ', object_pickle_filepath, color2='green')
                else:
                    colored_logging('existing pickled object: ', object_pickle_filepath)
            else:
                colored_logging('not saving the object', '', color1='red')

            # store the config separately in a directly readable format (json)
            if node.save_config:
                config_json_filepath = path.join(node_dir, 'config.json')
                if not os.path.exists(config_json_filepath):
                    try:
                        with open(config_json_filepath, 'w') as f:
                            json.dump(node.config, f)
                    except:
                        raise AttributeError('Unable to convert config to json')
                    colored_logging('saving config as json: ', config_json_filepath, color2='green')
                else:
                    colored_logging('config stored as: ', config_json_filepath)
            else:
                colored_logging('not saving the config passed to the object', '', color1='red')

            input_hash = get_hash_of_text(str(input))
            result_dir = path.join(node_dir, 'input_%s'%input_hash)

            # check if result already exists, if not then generate it
            existing_result_filepath = get_result_file(result_dir)
            
            if existing_result_filepath is not None:
                # load existing result from previous run
                colored_logging('loading previously calculated result from: ', existing_result_filepath)
                with open(existing_result_filepath, 'rb') as f:
                    out = pkl.load(f)
            else:
                # run and save
                colored_logging('no previous results for this input, running again ...', '', color1='red')
                out = node.run(input)
                if node.save_result:
                    result_hash = get_hash_of_text(str(out))
                    result_filepath = path.join(result_dir, 'result_%s.pkl'%result_hash)
                    os.makedirs(result_dir, exist_ok=True)
                    colored_logging('storing pickled result: ', result_filepath, color2='green')
                    try:
                        with open(result_filepath, 'wb') as f:
                            pkl.dump(out, f)
                    except:
                        raise AttributeError('Result is not picklable')
                else:
                    colored_logging('not saving the generated result', '', color1='red')
                    
            input = out
        colored_logging('------------------------------------------------------------------------------------------','', color1='magenta')
        return out