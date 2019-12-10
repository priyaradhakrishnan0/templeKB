  <h1>templeKB</h1>

  This package contains the corpus and the corpus creation and curation platform explained in the paper 'A Seed Corpus of Hindu Temples In India.'
  Please cite the paper if you are using this software.

  <h2>Folder structure </h2>
  . : Platform  <br>
  corpus : temple corpus  <br>
  data : Wikipedia pages and scrapped web pages <br>
  models : CQ and QA pretrained model files <br>
  output : preprocessing and other intermediate outputs <br>

  <h2>Requirements: </h2>
  Python 3.7 <br>
  Transformer model 'bert-large-uncased-whole-word-masking-finetuned-squad-pytorch_model.bin'  from https://huggingface.co/transformers/pretrained_models.html <br>
  BERT pretrained model 'wwm_uncased_L-24_H-1024_A-16' <br>
  SQuAD dataset <br>

  <h2>Paths in KGconfig.py : </h2>
  wiki_corpus_path <br>
  web_scraped_temple_text_path <br>
  bert_path <br>
  bert_for_qa <br>
  squad_path

  <h2> Create Corpus </h2>
  <h3> Web Scrape </h3>
  '''
  python Scrapper.py --url <web-page-url>
  '''
  <h3> Create corpus</h3>
  '''
  python templeQA_1.py
  '''
  <h3> Curate corpus </h3>
