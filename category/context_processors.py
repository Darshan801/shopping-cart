from .models import Category

def menu_links(request):
    # fetching all the categories form the database
    links = Category.objects.all()
    return dict(links=links)#brings all the category list and store it in link variable 
