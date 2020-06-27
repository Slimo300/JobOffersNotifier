from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.core.mail import send_mail
from bs4 import BeautifulSoup
import requests

from django.template.loader import render_to_string
from django.utils.html import strip_tags


def pracuj(request):
    lista = [{"key": 5001, "value": "Administracja biurowa"},
             {"key": 5002, "value": "Badania i rozwój"}, {"key": 5003, "value": "Bankowość"},
             {"key": 5004, "value": "BHP / Ochrona środowiska"},
             {"key": 5005, "value": "Budownictwo"},
             {"key": 5006, "value": "Call Center"}, {"key": 5007, "value": "Edukacja / Szkolenia"},
             {"key": 5008, "value": "Finanse / Ekonomia"},
             {"key": 5009, "value": "Franczyza / Własny biznes"},
             {"key": 5010, "value": "Hotelarstwo / Gastronomia / Turystyka"},
             {"key": 5011, "value": "Human Resources / Zasoby ludzkie"},
             {"key": 5013, "value": "Internet / e-Commerce / Nowe media"},
             {"key": 5014, "value": "Inżynieria"},
             {"key": 5015, "value": "IT - Administracja"},
             {"key": 5016, "value": "IT - Rozwój oprogramowania"},
             {"key": 5017, "value": "Łańcuch dostaw"},{"key": 5018, "value": "Marketing"},
             {"key": 5019, "value": "Media / Sztuka / Rozrywka"},
             {"key": 5020, "value": "Nieruchomości"},
             {"key": 5021, "value": "Obsługa klienta"},
             {"key": 5022, "value": "Praca fizyczna"},
             {"key": 5023, "value": "Prawo"},
             {"key": 5024, "value": "Produkcja"},
             {"key": 5025, "value": "Public Relations"},
             {"key": 5026, "value": "Reklama / Grafika / Kreacja / Fotografia"},
             {"key": 5027, "value": "Sektor publiczny"},
             {"key": 5028, "value": "Sprzedaż"},
             {"key": 5031, "value": "Transport / Spedycja"},
             {"key": 5032, "value": "Ubezpieczenia"},
             {"key": 5033, "value": "Zakupy"},
             {"key": 5034, "value": "Kontrola jakości"}, {"key": 5035, "value": "Zdrowie / Uroda / Rekreacja"},
             {"key": 5036, "value": "Energetyka"}, {"key": 5012, "value": "Inne"},]
    template = loader.get_template('index.html')
    context = {
        'lista': lista,
    }
    return HttpResponse(template.render(context, request))


def sendmail(request):
    link = "https://www.pracuj.pl/praca?rd=30"
    to_email = request.POST['email']
    from_email = 'sebastian.slimak707@gmail.com'
    categories = request.POST.getlist('categories')
    if len(categories) == 0:
        return pracuj(request)
    #TODO error?

    link += "&cc="+categories[0]

    for i in range(1, len(categories)):
        link += "%2c"+categories[i]

    source = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml')

    the_head = soup.find('head')
    the_message = soup.find_all('li', class_="results__list-container-item")

    formatted_message = ""
    for i in range(10):
        offer_logo = str(the_message[i].find('div', class_='offer-logo'))
        offer_details = str(the_message[i].find('div', class_='offer-details__text'))
        offer_desc = str(the_message[i].find('span', class_='offer-description__content'))
        offer_date = str(the_message[i].find('span', class_='offer-actions__date'))
        formatted_message += offer_logo + offer_details + offer_desc + offer_date + '<hr />'

    the_new_message = str(the_head) + formatted_message

    send_mail('Oferty', strip_tags(the_new_message), from_email, [to_email, ], html_message=the_new_message)

    return pracuj(request)
