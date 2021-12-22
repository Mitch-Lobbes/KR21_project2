import glob, os

from pgmpy.readwrite import BIFReader, XMLBIFWriter

PATH = "/Users/robinbux/Desktop/Vrije Universiteit/Period_2/KnowledgeRepresentation/Assignment/Assignment2/code/KR21_project2/Networks/**"

for filename in glob.iglob(PATH, recursive=True):
    print(filename)
    if os.path.isfile(filename): # filter dirs
        print(filename)
        with open(filename) as f:
            bn_file = f.read()
        bif_reader = BIFReader(string=bn_file)
        model = bif_reader.get_model()
        writer = XMLBIFWriter(model)
        writer.write_xmlbif(f"{filename}.BIFXML")