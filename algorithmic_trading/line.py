import requests
       
def lineNotify(msg, token):
    url_line_noti = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer ' + token}
    r = requests.post(url_line_noti, headers=headers, data = {'message': msg})
    # print(r.text)