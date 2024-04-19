from pytube import YouTube

clases_ap = { "clase01":"https://www.youtube.com/watch?v=NVWymUzSMOc",
              "clase02":"https://www.youtube.com/watch?v=ghmj2M3lylE",
              "clase03":"https://www.youtube.com/watch?v=eFnc72z31k8",
              "clase04":"https://www.youtube.com/watch?v=k4nQY0126Ug",
              "clase05":"https://www.youtube.com/watch?v=fDdfwa3iZK0",
              "clase06":"https://www.youtube.com/watch?v=7SsqzZZh-iQ",
              "clase07":"https://www.youtube.com/watch?v=gG51jozGygY",
              "clase08":"https://www.youtube.com/watch?v=3JPOhwGmDPM",
              "clase09":"https://www.youtube.com/watch?v=RDJVL10Qzzg",
              "clase10":"https://www.youtube.com/watch?v=JCSyky0RcAk",
              "clase11":"https://www.youtube.com/watch?v=JZfT4RoSeZA",
              "clase12":"https://www.youtube.com/watch?v=J-uxWWA1Zmk",
              "clase13":"https://www.youtube.com/watch?v=30e3MfFMXxI",
              "clase14":"https://www.youtube.com/watch?v=kFDUKZJ8pZY",
              "clase15":"https://www.youtube.com/watch?v=5uCf0dgQ3sc",
              "clase16":"https://www.youtube.com/watch?v=l7fi1xDh41A",
              "clase17":"https://www.youtube.com/watch?v=6LdZci2fhWw",
              "clase18":"https://www.youtube.com/watch?v=WXLQM6yTxjM",
              "clase19":"https://www.youtube.com/watch?v=ORoxiEWgwQc",
              "clase20":"https://www.youtube.com/watch?v=JJH8CUm58Js",
              "clase21":"https://www.youtube.com/watch?v=SsGZBXq39pc",
              "clase22":"https://www.youtube.com/watch?v=c_GRoCnZCdY",
              "clase23":"https://www.youtube.com/watch?v=YXPX9PjYXW8",
              "clase24":"https://www.youtube.com/watch?v=kDoJ7t1E4o8",
              "clase25":"https://www.youtube.com/watch?v=fUD4ojx7CSQ"}

for k,v in clases_ap.items():
    print("Descargando video de la {}".format(k))
    url = v
    yt = YouTube(url)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
