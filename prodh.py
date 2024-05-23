import requests

import pandas as pd

from tqdm import tqdm

from datetime import date

import streamlit as st

from io import BytesIO

from base64 import b64decode



tqdm.pandas()



def get_ranking_products(day, month, year=2024):

    hasNextPage = True

    cursor = None

    products = []

    while hasNextPage:

        url = "https://www.producthunt.com:443/frontend/graphql"

        cookies = {"_delighted_web": "{%2271AaKmxD4TpPsjYW%22:{%22_delighted_fst%22:{%22t%22:%221667281385155%22}}}", "visitor_id": "9bd1a4c5-5a04-44b3-a9fe-de20d515fdef", "track_code": "1c76d5831e", "_ga": "GA1.1.58851014.1716289611", "first_visit": "1716289611", "first_referer": "", "ajs_anonymous_id": "069a72db-5b19-491b-a9e1-10b8d810f9fe", "_hjSessionUser_3508551": "eyJpZCI6IjUyY2E5NWYwLWVkZTgtNTQzYy05YzY2LTYyMDhjMTg4MmQ3NyIsImNyZWF0ZWQiOjE3MTYyODk2MTE1MjQsImV4aXN0aW5nIjp0cnVlfQ==", "intercom-id-fe4ce68d4a8352909f553b276994db414d33a55c": "1ff538a1-e63f-4eaf-8849-697b3c2929cd", "intercom-session-fe4ce68d4a8352909f553b276994db414d33a55c": "", "intercom-device-id-fe4ce68d4a8352909f553b276994db414d33a55c": "0b8a9170-01d0-470b-8267-25eb6e8fa951", "ajs_user_id": "4517972", "_hjHasCachedUserAttributes": "true", "_hjSession_3508551": "eyJpZCI6ImU3OGUzOWM3LWY0NmYtNGNiYi05YWRjLTkwMjAwNTNlNjZiYiIsImMiOjE3MTYyOTkzMjQ4NjIsInMiOjEsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=", "_ga_WZ46833KH9": "GS1.1.1716299325.2.0.1716299325.60.0.0", "csrf_token": "jl_hsPc41N6gmbd67kXvYDcJRSyGxOsJvVf2-UUXhCvR-N9In-tm1ibOQ75vD7jkOTUK_7TEMW-pkmlNDwrO1Q"}

        headers = {"Sec-Ch-Ua": "\"Not:A-Brand\";v=\"99\", \"Chromium\";v=\"112\"", "Accept": "*/*", "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36", "Sec-Ch-Ua-Platform": "\"macOS\"", "Origin": "https://www.producthunt.com", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.producthunt.com/leaderboard/daily/2024/5/19", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}

        json={"extensions": {

                  "persistedQuery": {

                      "sha256Hash": "c00ccd1f7f4d9c21abeb9afa1f70cd4a45e9d374a6efd0ef0eb2689b9b869380", "version": 1

                  }},

              "operationName": "LeaderboardDailyPage", "variables": {

                  "cursor": cursor,

                  "day": day,

                  "featured": True,

                  "month": month,

                  "order": "DAILY_RANK",

                  "year": year}

             }

        out = requests.post(url, headers=headers, cookies=cookies, json=json)

        edges = out.json()['data']['homefeedItems']['edges']

        for i in edges:

            product = {"Date": f"{year}/{month}/{day}"}

            product['slug'] = i['node']['slug']

            product['url'] = "https://www.producthunt.com/posts/" + i['node']['slug']

            product['tagline'] = i['node']['tagline']

            product['votes'] = i['node']['votesCount']

            product['topics'] = ", ".join([j['node']['name'] for j in i['node']['topics']['edges']])

            products.append(product)

        hasNextPage = out.json()['data']['homefeedItems']['pageInfo']['hasNextPage']

        if hasNextPage:

            cursor = out.json()['data']['homefeedItems']['pageInfo']['endCursor']

    return products



def get_makers(slug):    

    url = "https://www.producthunt.com:443/frontend/graphql"

    headers = {"Sec-Ch-Ua": "\"Not:A-Brand\";v=\"99\", \"Chromium\";v=\"112\"", "Accept": "*/*", "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36", "Sec-Ch-Ua-Platform": "\"macOS\"", "Origin": "https://www.producthunt.com", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.producthunt.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}

    json={"extensions": {"persistedQuery": {"sha256Hash": "510d16fbf629902a34866e235fd3a8e710cd1f6e39f94a80e061d307600ec83f", "version": 1}}, "operationName": "PostPage", "variables": {"slug": slug}}

    out = requests.post(url, headers=headers,  json=json)

    makers = [{"Name": i['name'], "username": i['username']} for i in out.json()['data']['post']['makers']]

    return makers



def get_links(username):

    url = "https://www.producthunt.com:443/frontend/graphql"

    headers = {"Sec-Ch-Ua": "\"Not:A-Brand\";v=\"99\", \"Chromium\";v=\"112\"", "Accept": "*/*", "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36", "Sec-Ch-Ua-Platform": "\"macOS\"", "Origin": "https://www.producthunt.com", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.producthunt.com/posts/octoverse", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"}

    json={"extensions": {"persistedQuery": {"sha256Hash": "568ab27efbe48ab0e61095eca22570e2d28c38d5c3e29bd8322d70c0852ec9df", "version": 1}}, "operationName": "ProfileAboutPage", "variables": {"newProductsCursor": None, "username": username}}

    try:

        out = requests.post(url, headers=headers, json=json)

        links = [{i['kind']: i['encodedUrl']} for i in out.json()['data']['profile']['links']]

        return links

    except Exception as e:

        print(username)

        return []



# Streamlit App

st.title("Product Hunt Daily Rankings")

st.write("Select a date to fetch the Product Hunt daily rankings:")



input_date = st.date_input("Select Date", value=date(2024, 5, 1), min_value=date(2023, 1, 1))



if st.button("Fetch Data"):

    day = input_date.day

    month = input_date.month

    year = input_date.year



    with st.spinner("Fetching data..."):

        products = get_ranking_products(day, month, year)

        df = pd.DataFrame(products)



        df['makers'] = df['slug'].apply(get_makers)

        df = df.explode('makers')
        df.dropna(inplace=True)

        df['Name'] = df['makers'].apply(lambda x: x['Name'])

        df['username'] = df['makers'].apply(lambda x: x['username'])

        df.drop("makers", axis=1, inplace=True)

        df['links'] = df["username"].apply(get_links)

        

        df['links'] = df['links'].apply(lambda x: {j: k for i in x for j, k in i.items()})

        for i in ['facebook', 'instagram', 'linkedin', 'twitter', 'website']:

            df[i] = df['links'].apply(lambda x: x.get(i, ""))

        for i in ['facebook', 'instagram', 'linkedin', 'twitter', 'website']:

            df[i] = df[i].apply(lambda x: b64decode(x.strip()).decode() if x else x)

        df.drop(["links"], axis=1, inplace=True)

        st.write(df)