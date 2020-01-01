from mental_map.auto_map import AutoMap

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


def test_delete_list():
    # Verify against page 5, Table 1
    text = DENMARK_TEXT
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
    automap = AutoMap(text=text, delete_list=my_delete_list)

    response =\
        automap.get(text_concepts=True)
    text_concepts = response['text_concepts']

    deleted_denmark_text_concepts =\
        DELETED_DENMARK_TEXT.strip().strip('\n').lower().split()

    assert text_concepts == deleted_denmark_text_concepts,\
        "Failed to to remove unwanted words!"


def test_table3_generalization():
    #  Verify against page 9, Table 3
    pass


def test_statement_with_adjacency():
    #  Verify against page 11, Table 6
    pass