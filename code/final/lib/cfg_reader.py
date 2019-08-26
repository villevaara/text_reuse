import yaml
import getopt
import sys


def print_params(params):
    for key, value in params.items():
        print(key + ": " + str(value))
    print("\n")


def get_config_file_params(config_file, verbose=True):
    config = yaml.safe_load(open("cfg/" + config_file))
    if verbose:
        print_params(config)
    return config


def get_start_params(argv, verbose=True):
    # docid = "0145100105"
    cfg = ""
    # filter_out_author = "Hume, David (1711-1776)"  # ->cfg
    # author_ignore_id = ""  # ->cfg
    # require_first_author = None  # ->cfg
    # filter_out_year_below = -1  # ->cfg
    # filter_out_year_above = -1  # ->cfg
    limit = -1
    try:
        opts, args = getopt.getopt(argv, "",
                                   [
                                    # "docid=",
                                    "cfg=",
                                    "limit="]
                                   )
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        # if opt == "--docid":
        #     docid = arg
        if opt == "--cfg":
            cfg = arg
        elif opt == "--limit":
            limit = arg
    outpath_prefix = (cfg[:-4]
                      # + "-" + docid
                      )
    start_params = {
        # 'document_id': docid,
        'config_file': cfg,
        'api_limit': limit,
        'output_path_prefix': outpath_prefix}
    if verbose:
        print_params(start_params)
    return start_params
