import requests
import json
coder_api_url = "https://ottsquci4g2ok.pit-1.try.coder.app/api/v2"
# coder_api_url = "http://localhost:3000/api/v2"
# coder_session_token="ylTwRqG6NP-41Q4xDAUs2UO8aZ4vV76Gb"  # session for admin@gmail.com on debcoder
coder_session_token = "<coder_session_token>"
coder_organization_id = "<coder_organization_id"
class coder_api:
    def get_coder_user(email):
        r= requests.Session()
        r.headers.update({"Coder-Session-Token":coder_session_token})
        result = r.get(coder_api_url+f"/users/?q={email}")
        print(result.request.headers)
        print(result.request.body)
        rj = result.json()
        print(result.headers)
        print(result.json())

        if rj["count"]==1:
            coder_user = rj["users"][0]["username"]
            print(f"found coder user:{coder_user}")
            return coder_user
        else:
            print("no coder user found")
            return None

    def create_coder_user(email, username,password):
        r= requests.Session()
        r.headers.update({"Coder-Session-Token":coder_session_token})
        result = r.post(coder_api_url+f"/users",data =
                    json.dumps({'email': email,
                        'username': username,
                        'password': password,
                        'organization_id': coder_organization_id
                        }))
        print(result.request.headers)
        print(result.request.body)
        print("create user result")
        print(result.headers)
        print(result.json())
        if result.status_code==201:
            return result.json()
        else:
            return None

    def set_password(coder_user,random_pass):
        r= requests.Session()
        r.headers.update({"Coder-Session-Token":coder_session_token})

        print(f" set user={coder_user} pass={random_pass}")
        result = r.put(coder_api_url+f"/users/{coder_user}/password",data =
                        json.dumps({'password': random_pass}))
        print(result.request.headers)
        print(result.request.body)
        print("set password result")
        print(result.status_code)
        print(result.headers)

        if result.status_code==204:
            return True
        else:
            return None

