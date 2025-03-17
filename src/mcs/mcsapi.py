import requests
import os
def request(location:str, params:dict,method:str="get",body = None):
    # Define the API URL and parameters
    response = None
    url = "http://verweij.site:23333" + location
    api_key = os.getenv("MCSMANAGER_APIKEY")
    # Set up headers
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }

    # Add the API key as a query parameter
    params["apikey"] = api_key
    try:
        # Send GET request
        if method == "get":
            response = requests.get(url, headers=headers, params=params,json=body)
        elif method == "post":
            response = requests.post(url, headers=headers, params=params,json=body)
        elif method == "delete":
            response = requests.delete(url, headers=headers, params=params,json=body)
        elif method == "put":
            response = requests.put(url, headers=headers, params=params,json=body)
        else:
            raise "method not valid"
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        # Print response
        #print("Response Status Code:", response.status_code)
        #print("Response Body:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error during the request:", e)
        print(F"result: {response.json()}")
    else:
        result = response.json()
        return result
    return response.json()

def get_daemon_data():
    data = request("/api/overview", {})
    return data

def get_users(page: int, pagesize: int, user_name: str = "", role: str = ""):
    data = request("/api/auth/search", {"userName":user_name, "page":page, "page_size":pagesize, "role":role})
    return data

def start_instance(uuid:str,daemon:str):
    return request("/api/protected_instance/open", {"uuid":uuid, "daemonId": daemon})

def stop_instance(uuid:str,daemon:str):
    return request("/api/protected_instance/stop", {"uuid":uuid, "daemonId": daemon})

def restart_instance(uuid:str,daemon:str):
    return request("/api/protected_instance/restart", {"uuid":uuid, "daemonId": daemon})

def kill_instance(uuid:str,daemon:str):
    return request("/api/protected_instance/kill", {"uuid":uuid,"daemonId":daemon})

def add_user(username:str,password:str,permission:int):
    return request("/api/auth",{},"post",{"username": username,"password": password,"permission": permission})

def delete_user(uuid:str):
    return request("/api/auth",{},"delete",[uuid])

def create_server(daemon:str,name:str,ports:list,servertype:str,memory:int,version:str):
    data = instance_config(name,ports,servertype,memory,version)
    return request("/api/instance",{"daemonId":daemon},"post",data)

def update_server(daemon:str,uuid:str,name:str,ports:list,servertype:str,memory:int,version:str):
    data = instance_config(name,ports,servertype,memory,version)
    return request("/api/instance",{"daemonId":daemon,"uuid":uuid},"put",data)

def update_server_data(daemon:str,uuid:str,data:dict):
    return request("/api/instance",{"daemonId":daemon,"uuid":uuid},"put",data)

def delete_server(daemon:str,uuid:str,delete_files:bool):
    return request("/api/instance",{"daemonId":daemon},"delete",{"deleteFile":delete_files,"uuids":[uuid]})

def send_command(daemon:str,uuid:str,command:str):
    return request("/api/protected_instance/command",{"uuid": uuid,"daemonId": daemon,"command": command})

def get_output(daemon:str,uuid:str,size:int):
    return request("/api/protected_instance/outputlog",{"uuid": uuid,"daemonId": daemon,"size": size})

def get_data(daemon:str,uuid:str):
    return request("/api/instance",{"daemonId": daemon,"uuid": uuid})