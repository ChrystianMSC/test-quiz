import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

@pytest.fixture
def question_with_choices():
    """Fixture that creates a question with multiple choices for testing."""
    question = Question(title="Sample Question", points=10, max_selections=3)

    choice1 = question.add_choice(text="First choice", is_correct=True)
    choice2 = question.add_choice(text="Second choice", is_correct=False)
    choice3 = question.add_choice(text="Third choice", is_correct=True)
    choice4 = question.add_choice(text="Fourth choice", is_correct=False)

    return question


@pytest.fixture
def empty_question():
    """Fixture that creates a question with no choices."""
    return Question(title="Empty Question", points=5)


def test_set_correct_choices_with_fixture(question_with_choices):
    correct_choice_ids = [1, 3]

    question_with_choices.set_correct_choices(correct_choice_ids)

    for choice in question_with_choices.choices:
        if choice.id in correct_choice_ids:
            assert choice.is_correct is True
        else:
            assert choice.is_correct is False


def test_correct_selected_choices_with_fixture(question_with_choices):
    selected_ids = [1, 2, 3]

    result = question_with_choices.correct_selected_choices(selected_ids)

    assert result == [1, 3]
    assert len(result) == 2

def test_create_question_with_valid_points_succeeds():
    title = "Valid Title"
    points = 50

    question = Question(title=title, points=points)

    assert question.points == points
    assert question.title == title


def test_create_question_with_points_below_minimum_raises_exception():
    title = "Valid Title"
    invalid_points = [0, -1, -5]

    for points in invalid_points:
        with pytest.raises(Exception, match="Points must be between 1 and 100"):
            Question(title=title, points=points)


def test_create_question_with_points_above_maximum_raises_exception():
    title = "Valid Title"
    invalid_points = [101, 150, 1000]

    for points in invalid_points:
        with pytest.raises(Exception, match="Points must be between 1 and 100"):
            Question(title=title, points=points)


def test_add_choice_with_empty_text_raises_exception():
    question = Question(title="Valid Title")

    with pytest.raises(Exception, match="Text cannot be empty"):
        question.add_choice(text="", is_correct=False)


def test_add_choice_with_text_exceeding_max_length_raises_exception():
    question = Question(title="Valid Title")
    long_text = "a" * 101

    with pytest.raises(Exception, match="Text cannot be longer than 100 characters"):
        question.add_choice(text=long_text, is_correct=False)


def test_add_choice_returns_choice_with_incremented_ids():
    question = Question(title="Valid Title")

    first_choice = question.add_choice(text="First choice", is_correct=False)
    second_choice = question.add_choice(text="Second choice", is_correct=False)
    third_choice = question.add_choice(text="Third choice", is_correct=False)

    assert first_choice.id == 1
    assert second_choice.id == 2
    assert third_choice.id == 3


def test_remove_choice_by_id_removes_choice_from_choices_list():
    question = Question(title="Valid Title")
    choice_to_remove = question.add_choice(text="To be removed", is_correct=False)
    kept_choice = question.add_choice(text="Keep this one", is_correct=False)

    question.remove_choice_by_id(choice_to_remove.id)

    assert choice_to_remove not in question.choices
    assert kept_choice in question.choices
    assert len(question.choices) == 1


def test_remove_choice_by_id_with_invalid_id_raises_exception():
    question = Question(title="Valid Title")
    question.add_choice(text="First choice", is_correct=False)
    invalid_id = 999

    with pytest.raises(Exception, match="Invalid choice id 999"):
        question.remove_choice_by_id(invalid_id)


def test_set_correct_choices_marks_specified_choices_as_correct():
    question = Question(title="Valid Title")
    first_choice = question.add_choice(text="First", is_correct=False)
    second_choice = question.add_choice(text="Second", is_correct=False)
    third_choice = question.add_choice(text="Third", is_correct=False)
    correct_choice_ids = [first_choice.id, third_choice.id]

    question.set_correct_choices(correct_choice_ids)

    assert first_choice.is_correct is True
    assert third_choice.is_correct is True
    assert second_choice.is_correct is False


def test_correct_selected_choices_returns_only_correct_choice_ids():
    question = Question(title="Valid Title", max_selections=3)
    correct_choice = question.add_choice(text="Correct", is_correct=True)
    another_correct = question.add_choice(text="Also Correct", is_correct=True)
    incorrect_choice = question.add_choice(text="Incorrect", is_correct=False)
    selected_ids = [correct_choice.id, incorrect_choice.id, another_correct.id]

    result = question.correct_selected_choices(selected_ids)

    assert result == [correct_choice.id, another_correct.id]
    assert len(result) == 2