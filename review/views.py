from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader, Template, Context
import time
from .models import News, Content
from menu.models import Button

def review_page(request):
    '''
    the page to show news review
    '''
    template = loader.get_template("review/review.html")
    inner_template = Template('''
        {% load staticfiles %}
        <div class="multi">
          <a href="{{ news.url }}" class="item">
            <time>{{ date }}</time>
            <div class="wrap">
              <img src="{% static news.cover_pic_path %}" onerror="_imgError(this)">
                <h4>{{ news.title }}</h4>
                </div>
          </a>
          {% autoescape off %}
          {{ other_news_document }}
          {% endautoescape %}
        </div>
        ''')
    other_news_template = Template('''
        {% load staticfiles %}
        {% for news in news_list %}
        <a href="{{ news.url }}" class="item">
          <img src="{% static news.cover_pic_path %}" onerror="_imgError(this)">
            <h5>{{ news.title }}</h5>
        </a>
        {% endfor %}
        ''')

    try:
        all_news = Button.objects.get(url=request.get_raw_uri())
    except Button.DoesNotExist:
        raise Http404()

    all_news = all_news.content_set.all()
    date_list = []
    first_news_dict = {} # use date as the key, below the same
    other_news_dict = {}

    # order the contents by date

    for news in all_news:
        date = time.ctime(news.news_from.update_time)

        if date in date_list:
            try:
                other_news_dict[date]
            except KeyError:
                # the first piece of other news
                other_news_dict[date] = [ {
                    'url': news.url,
                    'cover_pic_path': "review/cover_pic/"+news.thumb_media_id,
                    'title': news.title
                    } ]
            else:
                other_news_dict[date].append( {
                    'url': news.url,
                    'cover_pic_path': "review/cover_pic/"+news.thumb_media_id,
                    'title': news.title
                    } )
        else:
            # the first piece
            date_list.append(date)
            first_news_dict[date] = {
                'url': news.url,
                'cover_pic_path': "review/cover_pic/"+news.thumb_media_id,
                'title': news.title
                }
            
    # render the document
    inner_document = ''

    for date in date_list:
        other_news_context = Context({'news_list': other_news_dict[date]})
        other_news_document = other_news_template.render(other_news_context)

        inner_context = Context({
            'news': first_news_dict[date],
            'date': date,
            'other_news_document': other_news_document
            })
        inner_document += inner_template.render(inner_context)
    
    context = RequestContext(request, {'document': inner_document})

    return HttpResponse(template.render(context))
