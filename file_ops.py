from news import AllNews

def write_selected(title):
    with open(AllNews.text_file, 'a') as f:
        f.write(title)
        print('stored title')
        
def check_posted():
    with open(AllNews.text_file, 'r') as f:
        posted_titles = f.readlines()
        return posted_titles

