def proceed_dict(data, context):
    """Return sorted-filtered data or message that something's wrong"""
    if context.get('filter', None):
        for field, value in context['filter'].items():
            if not all(field in item.keys() for item in data):
                return {field: 'there is not such field in one or in all strings of file'}
            data = [i for i in filter(lambda x: x[field] == value, data)]

    if context.get('sort', None):
        if context.get('sort', None):
            for field, reverse in context['sort'].items():
                if not all(field in item.keys() for item in data):
                    return {field: 'there is not such field in one or in all strings of file'}
                if type(reverse) is not bool:
                    return {field: 'value of this field can be only false or true'}
                data = sorted(data, key=lambda x: x[field], reverse=reverse)
    return data