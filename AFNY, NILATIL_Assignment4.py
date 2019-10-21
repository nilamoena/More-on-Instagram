#AFNY (1313618001)
#NILATIL MOENA (1313618002)
#Assignment4

import instaloader
import pandas as pd
import time

#Target profile
#Silahkan isi 'username'
username = "...."
L = instaloader.Instaloader(max_connection_attempts=0)
#Login akun dengan ("username", "password")
L.login("....", "....")

profile = instaloader.Profile.from_username(L.context, username)

#Menemukan daftar Ghost Followers dari target akun pertama
print('Ghost Followers')
print('Untuk mendapatkan daftar followers yang tidak aktif')
print('mis. Followers yang tidak pernah menyukai post an Anda\n')
likes = set()
print('Mengambil data likes dari semua post akun milik {}.'.format(profile.username))
for post in profile.get_posts():
    print(post)
    likes = likes | set(post.get_likes())

print('')
print('Mengambil data followers akun milik {}.'.format(profile.username))
followers = set(profile.get_followers())

ghosts = followers - likes

print('')
print('Ghost Followers :')

for ghost in ghosts:
        print(ghost.username)

print('====================================')
print('')

usernamelist = []
captionlist = []
hashtaglist = []
likeslist = []
commentlist = []
followerlist = []
        
#Target akun pertama
count = 1
for post in profile.get_posts():
        print("Mengumpulkan data dari akun " + username + " postingan ke " + str(count) + " dari " + str(profile.mediacount))
        caption = post.caption
        if caption is None:
            caption = ""
        if caption is not None:
            caption = caption.encode('ascii', 'ignore').decode('ascii')
        hashtag = post.caption_hashtags
        likes = post.likes
        
        comments = []
        for comment in post.get_comments() :
            comments.append(comment.text.encode('ascii', 'ignore').decode('ascii'))

        usernamelist.append(username)
        captionlist.append(caption)
        hashtaglist.append(hashtag)
        likeslist.append(likes)
        commentlist.append(comments)
        count = count+1

#Followers akun pertama (level 1)
followers = []
count_account = 1
for follower in profile.get_followers():
    username_follower = follower.username
    profile_follower = instaloader.Profile.from_username(L.context, username_follower)
    if profile_follower.is_private == True:
        print("Profile Instagram dengan username " + username_follower + " tidak dapat diakses")
    count = 1
    for post in profile_follower.get_posts():
        print("Mengumpulkan data dari akun " + username_follower + " postingan ke " + str(count) + " dari " + str(profile_follower.mediacount) + ", follower ke " + str(count_account) + " dari " + str(profile.followers))
        caption = post.caption
        if caption is None:
            caption = ""
        if caption is not None:
            caption = caption.encode('ascii', 'ignore').decode('ascii')
            caption = caption.split()
        
        hashtag = post.caption_hashtags
        likes = post.likes
        
        comments = []
        for comment in post.get_comments() :
            comments.append(comment.text.encode('ascii', 'ignore').decode('ascii'))

        usernamelist.append(username_follower)
        captionlist.append(caption)
        hashtaglist.append(hashtag)
        likeslist.append(likes)
        commentlist.append(comments)
        count = count+1
    count_account = count_account + 1
     
#Followers dari followers akun pertama (level 2)
    for follower2 in follower.get_followers():
        username_follower2 = follower2.username
        follower_follower2 = instaloader.Profile.from_username(L.context, username_follower2)
        if follower_follower2.is_private == True:
            print("Profile Instagram dengan username " + username_follower2 + " tidak dapat diakses")
        count = 1
        for post in follower_follower2.get_posts():
            print("Mengumpulkan data dari akun " + username_follower2 + " postingan ke " + str(count) + " dari " + str(follower_follower2.mediacount) + ", follower ke " + str(count_account) + " dari " + str(follower.followers))
            caption = post.caption
            if caption is None:
                caption = ""
            if caption is not None:
                caption = caption.encode('ascii', 'ignore').decode('ascii')
                caption = caption.split()
        
            hashtag = post.caption_hashtags
            likes = post.likes
        
            comments = []
            for comment in post.get_comments() :
                comments.append(comment.text.encode('ascii', 'ignore').decode('ascii'))

            usernamelist.append(username_follower2)
            captionlist.append(caption)
            hashtaglist.append(hashtag)
            likeslist.append(likes)
            commentlist.append(comments)
            count = count+1
        count_account = count_account + 1

data = pd.DataFrame({"account":usernamelist, "post":captionlist, "tag":hashtaglist, "likes":likeslist, "comments":commentlist})
timestring = time.strftime("%Y%m%d_%H%M%S")
nama_file = "data_instagram_" + username + "_" + timestring + ".csv"
data.to_csv(nama_file)
