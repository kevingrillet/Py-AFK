# https://deepnote.com/@rmi-ppin/Faie-un-singleton-en-python-DRh6cy8kTEmyqru_SkWs5g
# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class MetaSingleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in MetaSingleton.__instances:
            # print(f'Creation d\'une nouvelle instance de {cls}')
            MetaSingleton.__instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        # print(MetaSingleton.__instances)
        return MetaSingleton.__instances[cls]
