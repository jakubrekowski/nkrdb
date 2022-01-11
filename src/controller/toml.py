import toml as toml_old


class toml:
    def __init__(self, path):
        with open(path, "r") as toml_string:
            self.toml = toml_old.load(toml_string)

    def get(self, query):
        q = query.split('.')
        return self.__recursive_get(self.toml, q)

    def __recursive_get(self, _dict, keys):
        value = _dict.get(keys.pop(0))
        if value and keys: value = self.__recursive_get(value, keys)
        return value
