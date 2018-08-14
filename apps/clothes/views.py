from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max,Min
from django.db.models import Q


from clothes.models import Clothes,Season
from users.models import UserProfile

# Create your views here.
def more(request,sortby='time'):
    seasons = None
    user_info = None
    clothes = None
    search_keywords = request.POST.get('keywords','')
    try:
        user_info = UserProfile.objects.filter(username=request.user.username)[0]
    except:
        pass
    try:
        seasons = Season.objects.order_by('index')
    except:
        pass
    cson = request.GET.get('season','all')
    if cson=='all':
        if sortby=='sold':
            clothes = Clothes.objects.order_by('sold')
        else:
            clothes = Clothes.objects.order_by('update_time')
    else:
        try:
            clothes = Clothes.objects.filter(seasons__name=cson)
        except:
            pass
        if sortby=='sold':
            clothes = clothes.order_by('sold')
        else:
            clothes = clothes.order_by('update_time')
    if search_keywords:
        clothes = clothes.filter(Q(name__icontains=search_keywords)|Q(brand__name__icontains=search_keywords)|Q(sleeve__icontains=search_keywords))
    paginator = Paginator(clothes, 4)
    page = request.GET.get('page','1')
    clothes_paginator = paginator.get_page(page)
    clothes = list(map(lambda x: {'firstImg': x.colors.all()[0].colorImg,
                                  'firstColor':x.colors.all()[0].id,
                                  'c_id':x.id,
                                  'c_name':x.name,
                                  'price': x.price,
                                  'colors': x.colors.all(),
                                  'brand':x.brand,
                                  'fabric':x.fabric,
                                  'size_min':x.size_to_styles.aggregate(Min('name'))['name__min'],
                                  'size_max':x.size_to_styles.aggregate(Max('name'))['name__max'],
                                  'flower': x.colors.all()[0].flower},clothes_paginator))
    context = {'user_info': user_info, 'seasons': seasons, 'clothes': clothes,'clothes_paginator':clothes_paginator,'cson':cson,'sortby':sortby}
    return render(request, 'more.html', context=context)



def detail(request,c_id=1,color_id=1):
    user_info = None
    clothes = None
    colors = None
    sizes = None
    seasons = None
    all_seasons = None
    flowers = None
    ez = False
    try:
        user_info = UserProfile.objects.filter(username=request.user.username)[0]
    except:
        pass

    try:
        clothes = Clothes.objects.filter(id=c_id)[0]
        colors = clothes.colors.all()
        first_color = colors.filter(id=color_id)[0]
        sizes = clothes.size_to_styles.order_by('name')
        seasons = clothes.seasons.all()
        all_seasons = Season.objects.order_by('index').values('name')
        flowers = set(map(lambda x:x.flower,colors))
        ez = user_info.fav.filter(id=c_id).exists()
    except:
        pass
    context={'user_info':user_info,'clothing':clothes,'cur_color':first_color,'colors':colors,'colorsName':set(map(lambda x:x.name,colors)),'seasons':seasons,'all_seasons':all_seasons,'sizes':sizes,'flowers':flowers,'ez':ez}
    return render(request,'clothing.html',context=context)