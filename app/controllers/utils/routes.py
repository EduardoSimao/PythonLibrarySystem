from PIL import Image

def cropImge(name):

    img = Image.open('app/static/img/leitor_livro/{}'.format(name))
    img = img.resize((800, 600), Image.ANTIALIAS)
    img.save('app/static/img/leitor_livro/{}'.format(name))