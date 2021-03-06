from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from cf.models import FeedEntry
from django.core.mail import EmailMessage

import feedparser, datetime, urllib2, socket



def index(request):

    socket.setdefaulttimeout(10) #if connection is dropped city will be ignored

    #all craigslist locations.
    locations = ['brunswick', 'caribbean', 'colombia', 'costarica', 'daytona', 'santodomingo','keys','fortmyers', 'fortlauderdale',
     'gainesville','cfl','jacksonville','lakecity','lakeland','managua','ocala','orlando','panama','puertorico','sarasota','miami',
     'spacecoast','staugustine','tampa','treasure','valdosta','caracas','virgin','westpalmbeach','yucatan',

     'boston', 'chicago', 'losangeles', 'miami','montreal','newyork','seattle','sfbay','toronto','vancouver','washingtondc',

     'amsterdam', 'berlin', 'brussels', 'budapest', 'copenhagen','cotedazur','dublin','edinburgh','florence','london','munich',
     'oslo','oxford','paris','prague','rome','stockholm','venice',

     'cairo',

     'auburn','bham','dotham','shoals','gadsden','huntsville','mobile','montgomery','tuscaloosa','anchorage','fairbanks','kenai',
     'juneau','flagstaff','mohave','phoenix','prescott','showlow','sierravista','tucson','yuma',

     'fayar','fortsmith','jonesboro','littlerock','texarkana',

     'bakersfield','chico','fresno','goldcountry','hanford','humboldt','imperial','inlandempire','mendocino','merced','modesto','monterey',
     'orangecounty','palmsprings','redding','sacramento','sandiego','slo','santabarbara','siskiyou','stockton','susanville','ventura',
     'visalia','yubasutter',

     'boulder','cosprings','denver','eastco','fortcollins','rockies','pueblo','westslope',

     'newlondon','hartford','newhaven','nwct',

     'delaware',

     'okaloosa','panamacity','pensacola','tallahassee',

     'albanyga','athensga','atlanta','augusta','columbusga','macon','nwga','savannah','statesboro',

     'honolulu','boise','eastidaho','lewiston','twinfalls','bn','chambana','decatur','lasalle','mattoon','peoria','rockford','carbondale',
     'springfieldil','quincy',

     'bloomington','evansville','fortwayne','indianapolis','kokomo','tippecanoe','muncie','richmondin','southbend','terrehaute',

     'ames','cedarrapids','desmoines','dubuque','fortdodge','iowacity','masoncity','quadcities','siouxcity','ottumwa','waterloo',

     'lawrence','ksu','nwks','salina','seks','swks','topeka','wichita',

     'bgky','eastky','lexington','louisville','owensboro','westky',

     'batonrouge','cenla','houma','lafayette','lakecharles','monroe','neworleans','shreveport','maine','annapolis','baltimore','easternshore',
     'frederik','smd','westmd','capecod','westernmass','worcester',

     'annarbor','battlecreek','centralmich','detroit','flint','grandrapids','holland','jxn','kalamazoo','lansing','monroe','muskegon','nmi',
     'porthuron','saginaw','swmi','thumb','up',

     'bemidji','brainerd','duluth','mankato','minneapolis','rmn','marshall','stcloud',

     'gulfport','hattiesburg','jackson','meridian','northmiss','natchez',

     'columbiamo','joplin','kansascity','kirksville','loz','semo','springfield','stjoseph','stlouis',

     'billings','bozeman','butte','greatfalls','helena','kalispell','missoula','montana',

     'grandisland','lincoln','northplatte','omaha','scottsbluff',

     'elko','lasvegas','reno',

     'nh', 'cnj', 'jerseyshore','newjersey','southjersey',

     'albuquerque','clovis','farmington','lascruces','roswell','santafe',

     'albany','binghamton','buffalo','catskills','chautauqua','elmira','fingerlakes','glensfalls','hudsonvalley','ithaca','longisland','oneonta','plattsburgh','potsdam',
     'rochester','syracuse','twintiers','utica','watertown',

     'asheville','boone','charlotte','eastnc','fayetteville','greensboro','hickory','jonslow','outerbanks','raleigh','wilmington','winstonsalem',

     'bismarck','fargo','grandforks','nd',

     'akroncanton', 'ashtabula', 'athensohio', 'chillicothe','cincinnati','cleveland', 'columbus','dayton','limaohio','mansfield','sandusky','toledo','tuscarawas','youngstown','zanesville',

     'lawton', 'enid','oklahomacity','stillwater','tulsa',

     'bend','corvallis','eastoregon','eugene','klamath','medford','oregoncoast','portland','roseburg','salem',

     'altoona','chambersburg','erie','harrisburg','lancaster','allentown','meadville','philadelphia','pittsburgh','poconos','reading','scranton','pennstate','williamsport','york',

     'providence',

     'charleston', 'columbia', 'florencesc', 'greenville', 'hiltonhead','myrtlebeach',

     'nesd', 'csd', 'rapidcity', 'siouxfalls', 'sd',

     'chattanooga', 'clarksville', 'cookeville', 'jacksontn', 'knoxville', 'memphis', 'nashville', 'tricities',

     'abilene', 'amarillo', 'austin', 'beaumont', 'brownsville', 'collegestation', 'corpuschristi', 'dallas', 'nacogdches', 'delrio', 'elpaso', 'galveston', 'houston', 'killeen',
     'laredo', 'lubock', 'mccallen', 'odessa', 'sanangelo', 'sanantonio', 'sanmarcos', 'bigbend', 'texoma', 'easttexas', 'victoriatx', 'waco','wichitafalls',

     'logan', 'ogden', 'provo', 'saltlakecity', 'stgeorge',

     'vermont',

     'charlottesville','danville','fredericksburg', 'norfolk', 'harrisonburg','lynchburg','blacksburg','richmond','roanoke','swva','winchester',

     'bellingham', 'kpr','moseslake','olympic','pullman','skagit','spokane','wenatchee','yakima',

     'charlestonwv','martinsburg','huntington','morgantown','wheeling','parkersburg','swv','wv',

     'appleton','eauclarie','greenbay','janesville','racine','lacrosse','madison','milwaukee','northernwi','sheboygan','wausau',

     'wyoming','micronesia', 

     'calgary', 'edmonton', 'ftmcmurray','lethbridge','hat','peace','reddeer','cariboo','comoxvalley','abbotsford','kamloops','kelowna','cranbrook','nanaimo','princegeorge','skeena',
     'sunshine','victoria','whistler', 'winnipeg', 'newbrunswick', 'newfoundland','territories','yellowknife', 'halifax','barrie','belleville','brantford','chatham','cornwall','guelph',
     'hamilton','kingston','kitchener','londonon','niagara','ottawa','owensound','peterborough','sarnia','soo','sudbury','thunderbay','toronto','windsor','pei','quebec','saguenay','sherbrooke',
     'troisrivieres','regina','saskatoon','whitehorse',

     'vienna', 'bulgaria','zagreb','prague','findland','bordeaux','rennes','grenoble','lille','loire','lyon','marseilles','montpellier','rouen','strasbourg','toulouse',

     'bremen','cologne','dresden','dusseldorf','essen','frankfurt','hamburg','hannover','heidelberg','kaiserslautern','leipzig','munich','nuremberg','stuttgart',

     'athens', 'reykjavik','dublin','bologna','genoa','milan','naples','perugia','sardinia','sicily','torino','luxembourg','warsaw','faro','lisbon','porto','bucharest','moscow','stpetersburg',

     'alicante','baleares', 'barcelona','bilbao', 'cadiz','canarias','granada','madrid','malaga','sevilla','valencia','basel','bern','geneva','lausanne','zurich','istambul','ukraine',

     'aberdeen', 'bath', 'belfast','birmingham','brighton','bristol','cambridge','cardiff','coventry','derby','devon','dundee','norwich','eastmids','essex','glasgow','hampshire','kent','leeds','liverpool',
     'manchester','newcastle','nottingham','sheffield',

     'bangladesh', 'beijing', 'chengdu', 'chongqing', 'dalian', 'guangzhou', 'hangzhou','nanjing','shangai','shenyang','shenzen','wuhan','xian','hongkong',

     'ahmedabad','bangalore','bhubaneswar', 'chandigarh','chennai','delhi','goa','hyderabad','indore','jaipur','kerala','kolkata','lucknow','mumbai','pune','surat', 'jakarta','tehran','baghdad',
     
     'haifa', 'jerusalem', 'telaviv', 'ramallah', 'fukuoka', 'hiroshima', 'nagoya', 'okinawa', 'osaka', 'sapporo', 'sendai','tokyo', 'seoul','kuwait','beirut','malaysia','pakistan',

     'bacolod', 'naga', 'cdo', 'cebu', 'davaocity', 'iloilo', 'manila', 'pampanga', 'zamboanga', 'singapore', 'taipei', 'bangkok', 'dubai','vietnam',

     'adelaide', 'brisbane', 'cairns', 'canberra', 'darwin', 'goldcoast', 'melbourne', 'ntl','perth', 'sydney','hobart','wollogong','auckland','christchurch','dunedin','wellington',     

     'lapaz', 'belohorizonte', 'brasilia', 'curitiba','fortaleza', 'portoalegre','recife','rio','salvador','saopaulo','santiago','quito','elsalvador','guatemala',

     'acapulco','bajasur','chihuahua','juarez','guadalajara','guanajuato','hermosillo','mazatlan','mexicocity','monterrey','oaxaca','puebla','pv','tijuana','veracruz',

     'lima', 'montevideo',

     'addisababa','accra','kenya','casablanca','capetown','durban','johannesburg','pretoria','tunis'


     ]
    jobs = []
    for location in locations :
	#loading the page can take considerable time as it's reading and parsing all rss feeds and verifying them at sqlite. 
	#the following print will display the city processed in the console.	
        print "Looking at "+location
	#modify url as needed. i.e can remove telecommuting flag        
	craiglist_url = 'http://' + location + '.craigslist.org/search/sof?addOne=telecommuting&srchType=B&format=rss'       
        feeds = feedparser.parse( craiglist_url )        
        for entry in feeds.entries:
            #f=FeedEntry.objects.get(url= entry.link)
            num_results = FeedEntry.objects.filter(url = entry.link).count()
            if (num_results == 0) :
                view = 'B'
                f = FeedEntry(url= entry.link, read_date=datetime.datetime.now(), status = 'R')
                f.save()
            else :
                f = FeedEntry.objects.get(url = entry.link)
                if (f.status == 'R') :
                    view = 'N'
                else :
                    view = 'X'

            
            if (view == 'B' or view == 'N') :
                jobs.append([entry.published.replace(' ', '')[:-6].upper(), location, entry.title, entry.summary_detail.value,entry.link,view])

    
    return render_to_response('index.html', {
         'jobs' : sorted(jobs ,key=lambda job: job[0], reverse=True)
         } , context_instance = RequestContext(request))


def debug(request):

    locations = ['caribbean','buenosaires']
    jobs = []
    for location in locations :
        craiglist_url = 'http://' + location + '.craigslist.org/search/sof?addOne=telecommuting&srchType=B&format=rss'       
        feeds = feedparser.parse( craiglist_url )        
            
    return render_to_response('index.html', {
         'jobs' : feeds.entries ,
         })


def action(request):
    #these are implemented as ajax calls in the view. Page will not be resubmitted. Email or record will be marked as read or deleted in the db
    #or email will be sent, but page won't be reloaded
    c = {}
    c.update(csrf(request))

    if request.method == 'POST': # If the form has been submitted...
        link = request.POST['targetLink']
        action = request.POST['targetAction']

        if (action == 'delete') :
            #delete code 
            f = FeedEntry.objects.get(url = link)
            f.status='X'
            f.save()

        if (action == 'mail') :
            # mail action
            html = urllib2.urlopen(link).read()
            mail = find_between(html, 'var displayEmail = "','";')
       
            #harcode mail to test  
           
            email = EmailMessage('Craigslist post '+link, 'Hello,\nWrite down plain text email\n\n\n\n\nRegards,\nYourName' , to=[mail])
            email.send()

            f = FeedEntry.objects.get(url = link)
            f.status='S'
            f.save()



    # ... view code here
    return render_to_response('output.html', {
         'result' : link ,
         })




def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""
