import rdkit.Chem as Chem
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
import numpy as np
import torch
import pandas as pd

def drug_similarity(smiles):
    softmax_fun = torch.nn.Softmax(dim=1)
    N = len(smiles)
    simi = np.zeros((N,N))
    for i in range(N):
        col = []
        for j in range(N):
            ms = [Chem.MolFromSmiles(smiles[i]),Chem.MolFromSmiles(smiles[j])]
            fps = [FingerprintMols.FingerprintMol(x) for x in ms]
            similarity = DataStructs.FingerprintSimilarity(fps[0], fps[1])
            col.append(similarity)
        simi[i] = col

    input = torch.from_numpy(simi.astype(np.float32))
    similarity_softmax = softmax_fun(input)

    return similarity_softmax


def prepare_similarity_data(data_path, data_type, args):

# if __name__ == "__main__":

    if args["cross_study"]:
        GDSC_smiles_path = data_path+f'/{data_type}/{data_type}_Data/all_smiles.csv' # changing this for comatibility with all the data sources, have to find a better fix
    else:
        GDSC_smiles_path = data_path+f'/{data_type}/{data_type}_Data/{data_type}_smiles.csv' # changing this for comatibility with all the data sources, have to find a better fix
    GDSC_smiles = pd.read_csv(GDSC_smiles_path, index_col=0)
    GDSC_smiles_vals = GDSC_smiles["smiles"].values

    similarity_softmax = drug_similarity(GDSC_smiles_vals)
    GDSC_softmax_similarity = pd.DataFrame(similarity_softmax.numpy(), columns=None, index=None)
    GDSC_softmax_similarity.to_csv(data_path+f"/{data_type}/drug_similarity/{data_type}_drug_similarity.csv",header=None,index=None)

    print(f"{data_type} drug similarity has finished!")
