import os
import numpy as np
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError
import pandas as pd
import json
import socket

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_961831598513-urdgliumr9j4ab4g68jtocc30dimqb9g.apps.googleusercontent.com.json"
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    videoId = '5YGc4zOqozo'
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=videoId,
        maxResults = 100
    )
    response = request.execute()

    totalResults = 0
    totalResults = int(response['pageInfo']['totalResults'])

    count = 0
    nextPageToken = ''
    comments = []
    first = True
    further = True
    while further:
        halt = False
        if first == False:
            print('..')
            try:
                response = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=videoId,
                    maxResults = 100,
                    textFormat='plainText',
                    pageToken=nextPageToken
                            ).execute()
                totalResults = int(response['pageInfo']['totalResults'])
            except HttpError as e:
                print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
                halt = True

        if halt == False:
            count += totalResults
            for item in response["items"]:
                # 这只是一部分数据，你需要啥自己选就行，可以先打印下你能拿到那些数据信息，按需爬取。
                comment = item["snippet"]["topLevelComment"]
                author = comment["snippet"]["authorDisplayName"]
                text = comment["snippet"]["textDisplay"]
                likeCount = comment["snippet"]['likeCount']
                publishtime = comment['snippet']['publishedAt']
                comments.append([author, publishtime, likeCount, text])
            if totalResults < 100:
                further = False
                first = False
            else:
                further = True
                first = False
                try:
                    nextPageToken = response["nextPageToken"]
                except KeyError as e:
                    print("An KeyError error occurred: %s" % (e))
                    further = False
    print('get data count: ', str(count))
    data = np.array(comments)
    df = pd.DataFrame(data, columns=['author', 'publishtime', 'likeCount', 'comment'])
    df.to_csv('google_comments.csv', index=0, encoding='utf-8')

    result = []
    for time,comment in comments:
        temp = {}
        temp['date'] = time
        temp['comment'] = comment
        result.append(temp)
    json_str = json.dumps(result, indent=4)
    with open('youtube评论数据.csv', 'w', encoding='utf-8') as f:
        f.write(json_str)

    f.close()
if __name__ == "__main__":
    main()
