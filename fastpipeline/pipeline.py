import os
import pickle as pkl
import json
from os import path
from typing import List, Dict, Any, Tuple
from termcolor import colored
from datetime import datetime

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

    pipeline_logpath: str
        Full path of the json file containing details of a particular run of pipeline: [experiments_dir]/[experiment_name]/runs/yyy-mm-dd--hh-mm-ss.json

    log: dict[str, Any]
        Dictionary containing detailed log of a particular run

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
        now = datetime.now()
        
        dt_string = now.strftime("%Y-%m-%d--%H-%M-%S")
        self.experiment_name = experiment_name
        self.experiments_dir = experiments_dir
        self.savedir = path.join(self.experiments_dir, experiment_name)
        self.pipeline_logpath = path.join(self.savedir, 'runs', '%s.json'%dt_string)
        os.makedirs(path.join(self.savedir, 'runs'), exist_ok=True)
        self.log = {
            'id': dt_string,
            'nodes': {}
        }
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
        # colored_logging('-------------------------------', color1='magenta')
        colored_logging('Startig Pipeline: %s'%self.log['id'], color1='magenta')
        colored_logging('Experiment: %s'%self.experiment_name, color1='magenta')
        colored_logging('You can find the complete logs in: ', self.pipeline_logpath)

        for i, node in enumerate(self.nodes):
            out, node_log = self.run_for_node(node, i+1, input)
            if 'error' in node_log.keys():
                raise Exception(node_log['error'])
            self.log['nodes'][i+1] = node_log
            input = out
        
        # Save log to file
        colored_logging('', color1='magenta')
        colored_logging('Saving pipeline logs to file: %s'%self.pipeline_logpath, color1='magenta')
        colored_logging('Pipeline Run finished successfully', color1='green')
        colored_logging('--------------------', color1='magenta')
        with open(self.pipeline_logpath, "w") as f:
            json.dump(self.log, f, indent=4, sort_keys=True)

        
        return out

    def run_for_node(self, node: BaseNode, node_id: int, input: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        '''
        Helper function for run() called for each node
        '''
        node_log = {}
        try:
            node_name = node.name()
            node_hash = node.hash()
            colored_logging('')
            colored_logging('Started running node #%s: '%node_id, node_name)

            node_log['node_name'] = node_name
            node_log['node_hash'] = node_hash

            # directory to store all the contents of the node
            node_dir = path.join(self.savedir, node_name+'_'+node_hash)
            os.makedirs(node_dir, exist_ok=True)
            node_log['node_dir'] = node_dir

            # store the code for the class corresponding to this node (if it doesn't already exists)
            if node.save_code:
                object_code_filepath = path.join(node_dir, '%s.py'%node_name)
                if not os.path.exists(object_code_filepath):
                    code_text = get_code_text_from_object(node)
                    with open( object_code_filepath, 'w') as f:
                        f.write(code_text)
                node_log['object_code_filepath'] = object_code_filepath
            else:
                node_log['object_code_filepath'] = None

            # store the object so that it can be analyzed later if needed
            if node.save_object:
                object_pickle_filepath = path.join(node_dir, '%s.pkl'%node_name)
                if not os.path.exists(object_pickle_filepath):
                    try:
                        with open(object_pickle_filepath, 'wb') as f:
                            pkl.dump(node, f)
                    except:
                        raise AttributeError('Object is not picklable')
                node_log['object_pickle_filepath'] = object_pickle_filepath
            else:
                node_log['object_pickle_filepath'] = object_pickle_filepath

            # store the config separately in a directly readable format (json)
            if node.save_config:
                config_json_filepath = path.join(node_dir, 'config.json')
                if not os.path.exists(config_json_filepath):
                    try:
                        with open(config_json_filepath, 'w') as f:
                            json.dump(node.config, f)
                    except:
                        raise AttributeError('Unable to convert config to json')
                node_log['config_json_filepath'] = config_json_filepath
            else:
                node_log['config_json_filepath'] = config_json_filepath

            input_hash = get_hash_of_text(str(input))
            result_dir = path.join(node_dir, 'input_%s'%input_hash)
            
            colored_logging('Trying to load existing results from: ', result_dir)
            # check if result already exists, if not then generate it
            existing_result_filepath = get_result_file(result_dir)
            
            if existing_result_filepath is not None:
                colored_logging('Found existing results... Loading...', color1='green')
                # load existing result from previous run
                with open(existing_result_filepath, 'rb') as f:
                    out = pkl.load(f)
                
                node_log['result_filepath'] = existing_result_filepath
                node_log['reused_result'] = True
            else:
                # run and save
                colored_logging('Existing results not found... Running...', color1='red')
                node_log['reused_result'] = False
                out = node.run(input)
                if node.save_result:
                    result_hash = get_hash_of_text(str(out))
                    result_filepath = path.join(result_dir, 'result_%s.pkl'%result_hash)
                    os.makedirs(result_dir, exist_ok=True)
                    try:
                        with open(result_filepath, 'wb') as f:
                            pkl.dump(out, f)
                    except:
                        raise AttributeError('Result is not picklable')
                    node_log['result_filepath'] = result_filepath
                else:
                    node_log['result_filepath'] = None
        
        except Exception as e:
            out = None
            node_log['error'] = repr(e)

        return out, node_log

    