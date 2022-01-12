def transliterate_for_dag_id(name):
    from transliterate import translit
    name_translit = translit(name, 'ru', reversed=True)
    return clear_symbols(name_translit)


def clear_symbols(name):
    return "".join([c for c in name.replace(" ", "_") if (c.isalnum() or c in ["_", ".", "-"]) and c not in "әғқңөұүі"]).strip().lower()