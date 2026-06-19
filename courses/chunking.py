def chunk(lst, n):
    """Разбивает список на группы по n элементов."""
    if not lst:
        return []
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])
    return result

def flatten(lst_of_lsts):
    """Объединяет список списков в один плоский список."""
    result = []
    for sublist in lst_of_lsts:
        result.extend(sublist)
    return result