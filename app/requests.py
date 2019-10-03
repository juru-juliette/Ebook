# import urllib.request ,json
# from .models import Book_Api

# base_url=None

# def configure_request(app):
#     global base_url
    
#     base_url = app.config['BOOK_API_BASE_URL']

# def get_book():
#    with urllib.request.urlopen(base_url) as url:
#      get_book_data=url.read()
#      get_book_response=json.loads(get_book_data)
#      book_object=None
#      if get_book_response:
#        id=get_book_response.get('id')
#        author=get_book_response.get('author')
#        content=get_book_response.get('quote')
#        book_object=Book_Api(id,author,content)

#    return quote_object