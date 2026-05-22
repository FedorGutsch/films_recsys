from strings_transformers import String_to_list_transformer
import pytest

@pytest.mark.parametrize(
   'value',
   [
       ['smth', 'smth', 'smth'],
       'Actor 1, actor 2, actor 3',
       ['smth', 'smth', 3]
] 
    
)
def test_positive(value):
    assert isinstance(String_to_list_transformer.transform(value), list)


@pytest.mark.parametrize(
   'value',
   [
       5,
       ('actor2', 'actor1'),
       {"num": 1}
])  
def test_negative(value):
    assert not isinstance(String_to_list_transformer.transform(value), list)

    

