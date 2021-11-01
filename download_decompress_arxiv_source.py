import arxiv
import gzip
import json
import os
import pandas as pd
from tqdm import tqdm

from utils import mkdir_p

# ______________________________________________________________________________________________________ ||
def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--id',action='store',type=str,default='')
    parser.add_argument('--json',action='store',type=str,default='')
    parser.add_argument('--out_dir',action='store',type=str)
    parser.add_argument('--df_path',action='store',type=str)
    return parser.parse_args()

# ______________________________________________________________________________________________________ ||
def gunzip(infile,tofile):
    os.system('gunzip -f {:s}'.format(infile))

# ______________________________________________________________________________________________________ ||
def untar(infile,out_dir):
    os.system('tar -xf {:s} -C {:s}'.format(infile,out_dir))

# ______________________________________________________________________________________________________ ||
def download_uncompress_source_files(arxiv_id,out_dir='./',verbose=True):
    if verbose:
        print("Download and decompress ",arxiv_id," to ",out_dir)
    paper = next(arxiv.Search(id_list=[arxiv_id]).results())
    targz_filename = arxiv_id+".tar.gz"
    paper.download_source(dirpath=out_dir,filename=targz_filename)

    tar_filename = arxiv_id+".tar"
    tar_path = os.path.join(out_dir,tar_filename)
    targz_path = os.path.join(out_dir,targz_filename)
    gunzip(targz_path,tar_path)
    untar(tar_path,out_dir)

def get_metadata(json_path):
    with open(json_path) as f:
        for line in f:
            yield line

def read_meta_json(json_path,out_dir):
    metadata = get_metadata(json_path)
    for ind, paper in tqdm(enumerate(metadata)):
        paper = json.loads(paper)
        id_str = str(paper['id'])
        id_out_dir = os.path.join(out_dir,id_str)
        mkdir_p(id_out_dir)
        download_uncompress_source_files(id_str,id_out_dir)

def read_df(df_path,out_dir,):
    df = pd.read_csv(df_path,index_col=None)
    for index,row in df.iterrows():
        id_str = row['id']
        id_out_dir = os.path.join(out_dir,id_str)
        mkdir_p(id_out_dir)
        download_uncompress_source_files(id_str,id_out_dir)
    
if __name__ == "__main__":
    args = parse_arguments()
    if args.df_path:
        read_df(args.df_path,args.out_dir)    
    elif args.id:
        download_uncompress_source_files(args.id,args.out_dir)
    elif args.json:
        read_meta_json(args.json,args.out_dir)
        
