class String_to_list_transformer:
    def transform(value: str) -> list[str]:
        if isinstance(value, list):
            return value
        else:
            try:
                list_val = value.split(',')
                list_val = [i.strip() for i in list_val]
            
                return list_val
            except:
                raise TypeError(f'Ожидалась строка, получено {type(value)}')
            
print(String_to_list_transformer.transform('Actor 1, actor 2, actor 3'))


