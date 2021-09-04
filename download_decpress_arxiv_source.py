import arxiv
import gzip
import json
import os

# ______________________________________________________________________________________________________ ||
def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--id',action='store',type=str,default='')
    parser.add_argument('--json',action='store',type=str,default='')
    parser.add_argument('--out_dir',action='store',type=str)
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

def read_meta_json(json_path):
    f = open(json_path,)
    data = json.load(f)
    print(len(data))

if __name__ == "__main__":
    args = parse_arguments()
    if args.id:
        download_uncompress_source_files(args.id,args.out_dir)
    elif args.json:
        read_meta_json(args.json)
        
