from strings_transformers import String_to_list_transformer


def test_list():
    assert isinstance(String_to_list_transformer.transform(['smth', 'smth']), list)
    
