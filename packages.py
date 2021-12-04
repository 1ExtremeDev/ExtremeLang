def println(text):
    if text is None:
        print('\n')
    elif isinstance(text, list) or isinstance(text, tuple):
        print("".join(str(each) for each in text), end='')
    elif isinstance(text, str):
        print(text, end='') 

def request(*args):
    t = args[0][0]
    url = args[0][1]
    import requests
    if t == 'POST':
        print(
            requests.post(url).status_code, end=''
        )
    else:
        print(
            requests.get(url).status_code, end=''
        )
