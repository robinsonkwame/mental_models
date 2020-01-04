import utils
from mental_model.auto_map import AutoMap

# technically should be fixtures but these files have so little content
USA_TEXT =\
    "The New York City Police Department said a number of people were trapped in elevators for awhile. Thousands of people left buildings and walked into the streets."

DENMARK_TEXT =\
    """
    Reporters said hundreds of people emerged from shops in Copenhagen city centre to see what was happening, and used their mobile phones to contact their families.
    Railway and underground train services ground to a halt. Hospitals switched to be using emergency generators.
    The (nuclear) security systems worked just as they should.
    """

DELETED_DENMARK_TEXT =\
    """
    Reporters said hundreds people emerged shops Copenhagen city centre see happening, used mobile phones contact families.
    Railway underground train services ground halt. Hospitals switched using emergency generators.
    (nuclear) security systems worked should.
    """

my_delete_list = [
    "a",
    "and",
    "as",
    "be",
    "from",
    "in",
    "just",
    "of",
    "the",
    "their",
    "they",
    "to",
    "was",
    "what"]


def test_delete_list():
    # Verify against page 5, Table 1
    text = DENMARK_TEXT

    #  we create a custom nlp object so we can use our custom stopword list
    automap = AutoMap(text=text, delete_list=my_delete_list)
    response =\
        automap.get_concepts(want_text_concepts=True)
    text_concepts = response['text_concepts']

    deleted_denmark_text_concepts =\
        DELETED_DENMARK_TEXT.strip()\
                            .replace('\n', '')\
                            .replace('.', '')\
                            .replace(',', '')\
                            .replace('(', '')\
                            .replace(')', '')\
                            .split()  # spaCy removes (, ) even w custom stopwords :(

    assert [token.text for token in text_concepts] ==\
        deleted_denmark_text_concepts, "Failed to to remove unwanted words!"


def test_table2_generalization():
    #  Verify against page 7, Table 2 but use WordNet as the thesaurus
    text = DENMARK_TEXT.split('.')[0]  # we only want the first sentence

    #  delete_list=[None] is hack to prevent the default spaCy delete list
    # from taking precendence; here we want no delete list per Table 2
    automap = AutoMap(text=text, delete_list=[None])
    response =\
        automap.get_concepts(want_higher_concepts=True, include_text_concepts=True)

    expected =\
        ['communicator.n.01', 'express.v.02', 'large_integer.n.01',
         'of', 'group.n.01', 'appear.v.02',
         'from', 'mercantile_establishment.n.01', 'in',
         'entity.n.01', 'municipality.n.01', 'entity.n.01',
         'to', 'see', 'what',
         'was', 'happen.v.01', 'and',
         'used', 'their', 'mobile.s.01',
         'electronic_equipment.n.01', 'to', 'communicate.v.02',
         'their', 'unit.n.03']

    assert response["higher_concepts"] == expected, "Higher concepts test for include text concepts failed!"

    response =\
        automap.get_concepts(want_higher_concepts=True, include_text_concepts=False)
    expected =\
        ['communicator.n.01', 'express.v.02', 'large_integer.n.01',
         'group.n.01', 'appear.v.02', 'mercantile_establishment.n.01',
         'entity.n.01', 'municipality.n.01', 'entity.n.01',
         'happen.v.01', 'mobile.s.01', 'electronic_equipment.n.01',
         'communicate.v.02', 'unit.n.03']

    assert response["higher_concepts"] == expected, "Higher concepts test without text concepts failed!"


def test_direct_with_and_without_text_statement_all_windows():
    # This test covers all of page 9, Table 3
    # in that it generates all window sizes, had both adjacency
    # defn. (via rhetorical option) 
    raw_text = "I want to walk the dog"
    automap = AutoMap(text=raw_text, delete_list=[None])

    response =\
        automap.get_statements()
    expected_direct =\
        {1: [('I', 'desire.v.01'), ('desire.v.01', 'to'), ('to', 'travel.v.01'),
             ('travel.v.01', 'the'), ('the', 'canine.n.02')],
         2: [('I', 'to'), ('desire.v.01', 'travel.v.01'),
             ('to', 'the'), ('travel.v.01', 'canine.n.02')],
         3: [('I', 'travel.v.01'), ('desire.v.01', 'the'),
             ('to', 'canine.n.02')],
         4: [('I', 'the'), ('desire.v.01', 'canine.n.02')],
         5: [('I', 'canine.n.02')]}
    expected_rhetorical =\
        {1: [],
         2: [('desire.v.01', 'travel.v.01'), ('travel.v.01', 'canine.n.02')],
         3: [],
         4: [('desire.v.01', 'canine.n.02')],
         5: []}

    assert response['direct'] == expected_direct, "Direct statement constuction is off!"
    assert response['rhetorical'] == expected_rhetorical, "Rhetorical statement constuction is off!"
