import json 


def load_vocab(path : str) :
    with open(path , 'r') as f:
        tokens_to_ids : dict[str , int] = json.load(f)
    return { token_id : token_str for token_str , token_id in tokens_to_ids.items()}
