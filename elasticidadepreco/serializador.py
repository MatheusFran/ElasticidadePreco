from joblib import load, dump

def inSerializer(archive,path):
    return dump(archive,f'{path}.joblib')

def outSerializer(path):
    return load(f'{path}.joblib')