import argparse
import logging
import logging.config
import os

import yaml

from encryptpy import SOEncryptPy
from encryptpy.conf.logconf import logconfig
from encryptpy.conf.setting import EncryptType
from encryptpy.conf.setting import Setting as setting


def init_args():
    """
    initialization args
    """
    ignored_default = setting.default_filter_config.get('filter', {}).get('ignored')
    ignore_pf_default = setting.default_filter_config.get('filter', {}).get('ignore_pf')

    parser = argparse.ArgumentParser(description="Python encryption program")
    
    # config 配置将替换掉所有命令
    parser.add_argument('-c', '--config', type=str, required=False, help="yaml config file")

    parser.add_argument('-i', '--input', type=str, required=False, help='path of the project')
    parser.add_argument('-o', '--output', default='./build', type=str, required=False, help='Absolute path of output')
    parser.add_argument('-t', '--type', default=EncryptType.so, type=str, required=False, help="Encryption type")
    parser.add_argument('-k', '--keep_step', default=False, type=bool, required=False, help="Keep intermediate files")
    parser.add_argument('-d', '--ignored', default=ignored_default, nargs='+', required=False, help="Excluded folders")
    parser.add_argument('-f', '--ignore_pf', default=ignore_pf_default,  nargs='+', required=False, help="Excluded Python files")
    parser.add_argument('-l', '--logfile', default='./build.log',  type=str, required=False, help="Log file path")

    return parser.parse_args()


def args_filter(args):

    input = args.input
    output = args.output
    config = args.config
    type = args.type
    keep_step = args.keep_step
    ignored = args.ignored
    ignore_pf = args.ignore_pf
    logfile = args.logfile

    if config:
        if not os.path.isabs(config):
            config = os.path.abspath(config)
        with open(config) as fi:
            config_ = yaml.load(fi, Loader=yaml.FullLoader)
        
        input = config_.get('input')
        output = config_.get('output', './build')
        type = config_.get('type', EncryptType.so)
        keep_step = config_.get('keep_step', False)
        ignored = config_.get('filter', {}).get('ignored')
        ignore_pf = config_.get('filter', {}).get('ignore_pf')
        logfile = config_.get('logfile', './build.log')
     
    if not os.path.isabs(input):
        input = os.path.abspath(input)
    
    if not os.path.isabs(output):
        output = os.path.abspath(output)
    
    if not os.path.isabs(logfile):
        logfile = os.path.abspath(logfile)
    

    return {
        'input': input,
        'output': output,
        'type': type,
        'keep_step': keep_step,
        'ignored': ignored,
        'ignore_pf': ignore_pf,
        'logfile': logfile
    }


def execute():

    args = init_args()
    args = args_filter(args)

    logfile = args.get('logfile')
    log_conf = logconfig(logfile)
    logging.config.dictConfig(log_conf)
    logger = logging.getLogger(__name__)

    logger.info(f'input parameter: {args}')

    args.pop('logfile')
    
    type = args.get('type')
    if type == EncryptType.so:
        exec_cls = SOEncryptPy
    else:
        raise Exception(f'This encryption type does not exist: {type}')

    encrypt_program = exec_cls(**args)
    encrypt_program.execute()

if __name__ == "__main__":
    execute()