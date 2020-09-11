  <h1>templeKB</h1>

  This package contains the corpus and the corpus creation and curation platform explained in the paper 'A Seed Corpus of Hindu Temples In India.' LREC2020.
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
  <h3> Cite </h3>
  
  @inproceedings{radhakrishnan-2020-seed,
    title = "A Seed Corpus of {H}indu Temples in {I}ndia",
    author = "Radhakrishnan, Priya",
    booktitle = "Proceedings of The 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.32",
    pages = "254--258",
    abstract = "Temples are an integral part of culture and heritage of India and are centers of religious practice for practicing Hindus. A scientific study of temples can reveal valuable insights into Indian culture and heritage. However to the best of our knowledge, learning resources that aid such a study are either not publicly available or non-existent. In this endeavour we present our initial efforts to create a corpus of Hindu temples in India. In this paper, we present a simple, re-usable platform that creates temple corpus from web text on temples. Curation is improved using classifiers trained on textual data in Wikipedia articles on Hindu temples. The training data is verified by human volunteers. The temple corpus consists of 4933 high accuracy facts about 573 temples. We make the corpus and the platform freely available. We also test the re-usability of the platform by creating a corpus of museums in India. We believe the temple corpus will aid scientific study of temples and the platform will aid in construction of similar corpuses. We believe both these will significantly contribute in promoting research on culture and heritage of a region.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
