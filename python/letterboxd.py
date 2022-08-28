import requests, json, zipfile, io, os, wget
from dotenv import load_dotenv
load_dotenv()
import pandas as pd

s = requests.Session()
s.get('https://letterboxd.com')
session_cookies = s.cookies
cookies_dictionary = session_cookies.get_dict()

for i in cookies_dictionary:
    csrf = cookies_dictionary[i]

login = os.environ['LETTERBOXD_LOGIN']
password = os.environ['LETTERBOXD_PASSWORD']
apikey = os.environ['TMDB_APIKEY']


auth_url = 'https://letterboxd.com/user/login.do'
data_url = 'https://letterboxd.com/data/export/'
data_test_url = 'https://letterboxd.com/cfn/list/test-list/'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

data = "__csrf=" + csrf + "&username=" + login + "&password=" + password + "&remember=true"
print(data)

auth = s.post(auth_url, headers=headers, data=data)

print('===AUTH===')
print (auth)

print('==COOKIES==')
for cookie in s.cookies:
    print (cookie.name, cookie.value)

download = s.get(data_url)

print('===DOWNLOAD==')
print(download)
print(len(download.content))

z = zipfile.ZipFile(io.BytesIO(download.content))
z.extractall("/Users/chris/Documents/GitHub/chrisfnicholson/python/")


# Read CSV file into DataFrame df
df = pd.read_csv('reviews.csv', index_col=0)

# Show dataframe
print(df)

movieName = str(df.iloc[0]['Name'])
movieYear = str(df.iloc[0]['Year'])
print(df.iloc[0]['Name'])

moviedb_config = "https://api.themoviedb.org/3/configuration?api_key=" + apikey

moviedb = "https://api.themoviedb.org/3/search/movie?api_key=" + apikey + "&language=en-US&query=" + movieName + "page=1&include_adult=false&year=" + movieYear
print(moviedb)

i = requests.Session()
#db_config_reply = i.get(moviedb_config)
#print(db_config_reply.content)
dbreply = i.get(moviedb)
dbjson = json.loads(dbreply.text)
poster_baseurl = "https://image.tmdb.org/t/p/w342"
poster_request = poster_baseurl + dbjson['results'][0]['poster_path']
print(poster_request)
wget.download(poster_request, 'shawshank.jpg')
