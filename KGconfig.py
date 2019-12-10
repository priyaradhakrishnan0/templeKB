import argparse

parser = argparse.ArgumentParser(description='KG')

parser.add_argument('--wiki_corpus_path', help='annotated_wiki_extraction', required=False, default="/wiki_text_corpus/annotated_wiki_extraction/")
parser.add_argument('--web_scraped_temple_text_path', help='templeKB', required=False, default="/web_corpus/web_text_corpus/")
parser.add_argument('--url', help='website url', required=False, default="http://www.vaikhari.org/mulakkulam.html")

args = vars(parser.parse_args())
if args["wiki_corpus_path"]:
    #args["wiki_corpus_path"] = xxx
    print("[Info] Using annotated_wiki_extraction in /Users/pradh4/Desktop/research/wiki_text_corpus/")

print(str(args))
