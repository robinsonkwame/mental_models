import os
import json
from mental_model.auto_map import AutoMap
from mental_model.similarity import sinreich_relationship_similarity_measure

dialog_example_path =\
    "./tests/fixture"
dialog_example_file =\
    "sample_dialog.json"


def test_sinreich_same_groups():
    group_one =\
        {1: [('I', 'desire.v.01'),
             ('desire.v.01', 'to'),
             ('to', 'travel.v.01'),
             ('travel.v.01', 'the'),
             ('the', 'canine.n.02')],
         2: [('I', 'to'),
             ('desire.v.01', 'travel.v.01'),
             ('to', 'the'),
             ('travel.v.01', 'canine.n.02')],
         3: [('I', 'travel.v.01'),
             ('desire.v.01', 'the'),
             ('to', 'canine.n.02')],
         4: [('I', 'the'),
             ('desire.v.01', 'canine.n.02')],
         5: [('I', 'canine.n.02')]}

    relationship_similarity =\
        sinreich_relationship_similarity_measure(group_one, group_one)

    assert all((1.0 == score for window_size, score 
        in relationship_similarity.items())),\
            ("Same groups failed to be 1.0 at all window sizes for "
             "Sinreich similarity measure!")


def test_sinreich_window_size_1():
    group_one =\
        {1: [('I', 'desire.v.01'),
             ('desire.v.01', 'to'),
             ('to', 'travel.v.01'),
             ('travel.v.01', 'the'),
             ('the', 'canine.n.02')]}

    group_two =\
        {1: [('I', 'desire.v.01'),
             ('desire.v.01', 'to'),
             ('to', 'travel.v.01'),
             ('travel.v.01', 'the'),
             ('XXX', 'XXXX')]}

    #  here group two differs on the last entry.
    # this should make,
    # 
    # common arcs:  4
    # uncommon arcs: 2
    # similarity --> 4/6 = 0.67

    relationship_similarity =\
        sinreich_relationship_similarity_measure(group_one, group_two)

    assert relationship_similarity[1] == 4/6, "Window size 1 test doesn't match!"


def test_sinreich_window_size_2():
    group_one =\
        {1: [('I', 'desire.v.01'),
             ('desire.v.01', 'to'),
             ('to', 'travel.v.01'),
             ('travel.v.01', 'the')],
         2: [('the', 'canine.n.02')]}

    group_two =\
        {1: [('I', 'desire.v.01'),
             ('desire.v.01', 'to'),
             ('to', 'travel.v.01'),
             ('travel.v.01', 'the')],
         2: [('XXX', 'XXXX')]}

    #  here both groups differ at the last window
    # this should make,
    # 
    # for window_size 2
    #
    # common arcs:  4
    # uncommon arcs: 2
    # similarity --> 4/6 = 0.67
    # 
    # for window size 1
    # should be 1.0
    relationship_similarity =\
        sinreich_relationship_similarity_measure(group_one, group_two)

    assert relationship_similarity[2] == 4/6, "Window size 2 of 2 test doesn't match!"

    assert relationship_similarity[1] == 1.0, "Window size 1 of 2 test doesn't match!"


def test_sinreich_window_size_2_reverse():
    group_one =\
        {2: [('I', 'desire.v.01'),
             ('desire.v.01', 'to'),
             ('to', 'travel.v.01'),
             ('travel.v.01', 'the')],
         1: [('the', 'canine.n.02')]}

    group_two =\
        {2: [('I', 'desire.v.01'),
             ('desire.v.01', 'to'),
             ('to', 'travel.v.01'),
             ('travel.v.01', 'the')],
         1: [('XXX', 'XXXX')]}

    #  here both groups differ at the last window
    # this should make,
    # 
    # for window_size 2
    #
    # common arcs:  4
    # uncommon arcs: 2
    # similarity --> 4/6 = 0.67
    # 
    # for window size 1
    # should be 0
    relationship_similarity =\
        sinreich_relationship_similarity_measure(group_one, group_two)

    assert relationship_similarity[2] == 4/6, "Window size 2 of 2 test doesn't match!"

    assert relationship_similarity[1] == 0, "Window size 1 of 2 test doesn't match!"


def test_sinreich_window_size_3_with_gap():
    group_one =\
        {3: [('A', 'B')],
         1: [('I', 'desire.v.01'),
             ('desire.v.01', 'to'),
             ('to', 'travel.v.01'),
             ('travel.v.01', 'the')],
         2: []}

    group_two =\
        {3: [('A', 'C')],
         1: [('I', 'desire.v.01'),
             ('desire.v.01', 'to'),
             ('to', 'travel.v.01'),
             ('travel.v.01', 'the')],
         2: []}

    #  here both groups differ at the last window
    # this should make,
    # 
    # for window_size 2
    #
    # common arcs:  4
    # uncommon arcs: 2
    # similarity --> 4/6 = 0.67
    # 
    # for window size 1
    # should be 0
    relationship_similarity =\
        sinreich_relationship_similarity_measure(group_one, group_two)

    assert relationship_similarity[3] == 4/6, "Window size 3 of 3 test doesn't match!"

    assert relationship_similarity[2] == 1.0, "Window size 2 of 3 test doesn't match!"

    assert relationship_similarity[1] == 1.0, "Window size 1 of 3 test doesn't match!"


def test_dialog_example():
    #  A more realistic similiarty example over dialog pairs
    # Note: this is an integration test, not a unit test
    with open(os.path.join(dialog_example_path, dialog_example_file), "r") as file_object:
        dialogs = json.load(file_object)

        number_of_utterances =\
            len(dialogs["utterances"])
        utterances = dialogs["utterances"]  # to save typing

        turns =\
            [(utterances[index-1]["text"], utterances[index]["text"])
                for index in range(1, number_of_utterances)]

        turn_concepts =\
            [(AutoMap(text=turn[0] ).get_statements()["rhetorical"],
              AutoMap(text=turn[1]).get_statements()["rhetorical"]) for turn in turns]

        turn_similarity =\
            [sinreich_relationship_similarity_measure(*turn) for turn in turn_concepts]
        1/0

        assert 33 == len(turn_similarity), "Unexpected number of turns!"
