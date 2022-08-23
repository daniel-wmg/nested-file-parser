from collections import defaultdict
from glob import glob
from pathlib import Path
import pandas as pd
import csv
import argparse

def get_uuid(filename):
    return filename.split("_")[0]



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process kraken reports with nested phylogenetic-like info")
    
    parser.add_argument('input', metavar="INPUT_DIRECTORY", type=str, help="The input directory where the files are stored")
    parser.add_argument('out', metavar="OUT_FILE", type=str, help="Path to the output file. Output is saved as .csv")
    parser.add_argument('valcol', metavar="VALUE_COLUMN", type=int, help="The column in the raw files that contain the value of interest")
    parser.add_argument('sppcol', metavar="SPECIES_COLUMN", type=int, help="The column in the raw file that has the species name. Use -1 for the last column")
    parser.add_argument("spp", metavar="SPECIES", type=str, help="The species that we want data for. Enter as comma-separated list in quotations")
    parser.add_argument("-g", metavar="GLOB", type=str, help="The glob search string, within the directory.", default="*.kraken_report.txt")

    
    args = parser.parse_args()
    
    ## Setting args
    value_col = args.valcol
    species_col = args.sppcol
    wanted_species = [spp.strip() for spp in args.spp.split(",")]
    out_path = args.out
    input_dir = Path(args.input)

    out_dict = defaultdict(dict)

    for file in input_dir.glob(args.g):
        path = Path(file)
        uuid = get_uuid(path.name)
        
        with open(file, "r") as f:
            current_row = defaultdict(str)
            reader = csv.reader(f, delimiter="\t", quotechar='"')

            for row in reader:
                
                species = row[species_col].strip()

                if species in wanted_species:
                    value = row[value_col].strip()
                    current_row[species] = value

            out_dict[uuid] = current_row

    df = pd.DataFrame.from_dict(out_dict, orient="index")
    
    df.to_csv(out_path)
                
