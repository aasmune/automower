
def config_section(config, section):
    dict_ = {}
    options = config.options(section)
    for option in options:
        try:
            dict_[option] = config.get(section, option)
        except Exception as e:
            print(str(e))
            dict_[option] = None
    return dict_