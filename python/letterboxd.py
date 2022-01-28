import requests, json, zipfile, io
import pandas as pd

s = requests.Session()
s.get('https://letterboxd.com')
session_cookies = s.cookies
cookies_dictionary = session_cookies.get_dict()

for i in cookies_dictionary:
    csrf = cookies_dictionary[i]

login = os.environ['LETTERBOXD_LOGIN']
password = os.environ['LETTERBOXD_PASSWORD']
apikey = os.environ['TMBD_APIKEY']


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

moviedb = "https://api.themoviedb.org/3/search/movie?api_key=" + apikey + "&language=en-US&query=" + movieName + "page=1&include_adult=false&year=" + movieYear
print(moviedb)

i = requests.Session()
dbreply = i.get(moviedb)
print(dbreply.content)
