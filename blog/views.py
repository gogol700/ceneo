import urllib.request
import math
from bs4 import BeautifulSoup
from datetime import datetime
from django.shortcuts import render
from blog.models import Post
from django.views.generic import ListView

prefix = "https://www.ceneo.pl/"
postfix = "/opinie-"

class Ceneo:
    id = ""
    author = ""
    recomendation = ""
    stars = ""
    content = ""
    advantages = ""
    disadvantages = ""
    useful = ""
    unuseful = ""
    add_date = ""
    purchase_date = ""

    
class UserListView(ListView):    
    model = Post
    template_name = 'blog/load_list.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'blog'  # Default: object_list
    paginate_by = 10
    queryset = Post.objects.all()
    
    def get_queryset(self):
        product_id = self.request.GET.get('product_id','')
        if product_id != "":
                return Post.objects.filter(product_id=self.request.GET.get('product_id'))
        else:
                return Post.objects.all()
    
 
def post_list(request):
    
    result = []
    
    product_id = request.GET.get('product_id','')
    
    page_from = request.GET.get('page_from','')
    
    page_to = request.GET.get('page_to','')
    
    if product_id != "": # The variable
        url = prefix+product_id
        posts = loadCountOfPage(url)
        
        #url = "https://www.ceneo.pl/45498942/opinie-1"
    
       # result.append(loadPage(url))
        if(page_from != "" and page_to != ""):
            for x in range(int(page_from), int (page_to)):
                url = prefix+product_id+postfix+str(x)
                result+=loadPage(url)
               
        if(len(result) != 0):
            for value in result:
                p = Post(id=value.id, author=value.author, recomendation=value.recomendation,stars=value.stars,content=value.content,
                product_id=product_id, unuseful=value.unuseful, useful=value.useful,purchase_date=value.purchase_date)
                p.save()            
    else:
        posts = 0
        
    return render(request, 'blog/post_list.html', {'posts': posts, 'product_id': product_id, 'page_from': page_from, 'page_to': page_to, 'results': result})


def loadPage(url):
    
    result = []
    
    site = urllib.request.urlopen(url)
    page = site.read()

    page_tree = BeautifulSoup(page, 'html.parser')

    opinions_num = int(page_tree.find("span",attrs={"itemprop": "reviewCount"}).string)

    #parsowanie kodu strony

    opinions = page_tree.select("li.review-box")
    
    for opinion in opinions:
    # print(opinion)
        ceneo = Ceneo() 
        
        id = int(opinion["data-entry-id"])

        author = (opinion.select("div.reviewer-name-line")).pop().string

        try:
            recomendation = (opinion.select("div.product-review-summary > em")).pop().string
        except IndexError:
                recomendation = None

        stars = (opinion.select("span.review-score-count")).pop().string

        content = (opinion.select("p.product-review-body")).pop().get_text()

        useful = (opinion.select("[id^=votes-yes]")).pop().string

        unuseful = (opinion.select("[id^=votes-no]")).pop().string

        time = opinion.select("div > span.review-time > time")


        add_date = datetime.strptime(time.pop()["datetime"], "%Y-%m-%d %H:%M:%S")
        # od Python 3.7
        # add_date = datetime.fromisoformat(time.pop()["datetime"])

        if time:
            purchase_date = datetime.strptime(time.pop()["datetime"], "%Y-%m-%d %H:%M:%S")
        else:
            purchase_date = None

        try:
            advantages = (opinion.select("div.pros-cell > ul")).pop().get_text()
        except IndexError:
            advantages = None

        try:
            disadvantages = (opinion.select("div.cons-cell > ul")).pop().get_text()
        except IndexError:
            disadvantages = None
            
        ceneo.id = id
        ceneo.author = author
        ceneo.recomendation = recomendation
        ceneo.stars = stars
        ceneo.content = content
        ceneo.advantages = advantages
        ceneo.useful = useful
        ceneo.unuseful = unuseful
        ceneo.add_date = add_date
        ceneo.purchase_date = purchase_date
        
       
        result.append(ceneo)
            

    return result

def loadCountOfPage(url):
    #pobranie zawartoЬci strony
    site = urllib.request.urlopen(url)
    page = site.read()

    page_tree = BeautifulSoup(page, 'html.parser')

    opinions_num = int(page_tree.find("span",attrs={"itemprop": "reviewCount"}).string)
    return math.ceil(opinions_num/10)