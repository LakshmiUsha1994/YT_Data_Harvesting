#!/usr/bin/env python
# coding: utf-8

# In[97]:


pip install requests


# In[2]:





# In[23]:


pip install seaborn


# In[98]:


Api_Key="AIzaSyBdorMTSa_edWObhC9ftmRsEa4nJUrGQlM"


# In[99]:


pip install --upgrade google-api-python-client


# In[100]:


import pandas as pd
from googleapiclient.discovery import build
import seaborn as sns


# In[101]:


Api_Key="AIzaSyBdorMTSa_edWObhC9ftmRsEa4nJUrGQlM"
#api_service_name="youtube"
#api_version="v3"
youtube=build('youtube','v3',developerKey=Api_Key)

channel_ids=['UCnjX8fylNvSKVSMuyTqshsQ',
             'UCnz-ZXXER4jOvuED5trXfEA',
             'UCLhLpPmymIUy0JfF3Nkcf_w' ] # dharsha]


# # Function to get channel statistics

# In[102]:


def channel_videos(youtube,channel_ids):
    #Api_Key="AIzaSyBdorMTSa_edWObhC9ftmRsEa4nJUrGQlM"
    #api_service_name="youtube"
    #api_version="v3"
    #youtube=build('youtube','v3',developerKey=Api_Key)
    all_data=[]
    
    request=youtube.channels().list(
               part="snippet,contentDetails,statistics", 
               id=','.join(channel_ids))
    response=request.execute()
    
    for i in range(len(response["items"])):
        data=dict(Channel_name=response['items'][i]['snippet']['title'],
             Subscriber=response['items'][i]['statistics']['subscriberCount'],
             views=response['items'][i]['statistics']['viewCount'],
             total_videos=response['items'][i]['statistics']['videoCount'],
             playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
                 )
        all_data.append(data)
    
    return(pd.DataFrame(all_data))
    
channel_videos(youtube,channel_ids)

    

    


# In[103]:


Channel_data=channel_videos(youtube,channel_ids)
Channel_data['Subscriber']=pd.to_numeric(Channel_data['Subscriber'])
Channel_data['views']=pd.to_numeric(Channel_data['views'])
Channel_data['total_videos']=pd.to_numeric(Channel_data['total_videos'])
Channel_data


# In[104]:


playlist_id=Channel_data.loc[Channel_data['Channel_name']=='Cosmo Coding','playlist_id'].iloc[0]
playlist_id


# In[105]:


def get_video_ids(youtube,playlist_id):
    video_ids=[]
    request=youtube.playlistItems().list(
        part="snippet,contentDetails", 
        playlistId=playlist_id,
        maxResults=50
    )
    
    response=request.execute()
    
    for i in range(len(response["items"])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
    next_page_token=response.get('nextPageToken')
    more_pages=True
    
    while more_pages:
        if next_page_token is None:
            more_pages=False
        else:
            request=youtube.playlistItems().list(
                      part="contentDetails", 
                      playlistId=playlist_id,
                      maxResults=50,
                      pageToken=next_page_token)
            response=request.execute()
            
            for i in range(len(response["items"])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
            next_page_token=response.get('nextPageToken')
    
    return video_ids


# In[108]:


print(type(video_ids))


# In[110]:


videoID=get_video_ids(youtube,playlist_id)
videoID


# ## function to get video details

# In[113]:


def get_video_details(youtube, video_ids):
    request=youtube.videos().list(
                part="snippet,statistics", 
                id=','.join(video_ids[:50]))
    response=request.execute()
                    
            
    return response
get_video_details(youtube, video_ids)


# In[123]:


def get_video_details(youtube,video_ids):
    all_video_info=[]
    
    for i in range(0,len(videoID),50):
        requests=youtube.videos().list(
                   part="snippet,statistics", 
                   id=video_ids)
        response=requests.execute()
        
        for video in response['items']:
            video_stats=dict(Title= video['snippet']['title'],
                             Published_Date=video['snippet']['publishedAt'],
                             Views=video['statistics']['viewCount'],
                             Likes=video['statistics']['likeCount'],
                             Dislikes=video['statistics']['dislikeCount'],
                             Favorites=video['statistics']['favouriteCount'],
                             CommentsCount=video['statistics']['commentCount']
                             )
            
            #stats_to_keep={'snippet':['channelTitle','title','description','tags','publishedAt'],
                          #'statistics':['viewCount','likeCount','favouriteCount','commentCount'],
                          #'contentDetails':['duration','definition','caption']}
            #video_info={}
            #video_info['video_id']=video['id']
            
            #for k in stats_to_keep.keys():
                #for v in stats_to_keep[k]:
                   # try:
                        #video_info[v]=video[k][v]
                    #except:
                        #video_info[v]=None
                        
            all_video_info.append(video_stats)
            
    return all_video_info
        
        
        


# In[124]:


get_video_details(youtube,video_ids)

