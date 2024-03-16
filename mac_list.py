# Editer : Luca_yao
# E-mail : stelliva42@gmail.com
# Date : 2024/02/06

from ruamel.yaml import YAML
from datetime import datetime, timedelta
from mail_sender import send_mail

def load_User_info(file_path):
    with open(file_path, 'r') as file:
        yaml = YAML()

        comments = []
        data = []
        for line in file:
            if line.startswith("#"):
                comments.append(line)
            else:
                data.append(line)

        return comments, yaml.load("\n".join(data))

def save_User_info(file_path, comments, Users_info_list, expired_users):
    with open(file_path, 'w') as file:
        yaml = YAML()
      
        counter = 0
        for User_info in Users_info_list:
            order = ["USER", "WIFI", "WIRED", "START_TIME", "END_TIME"]
            ordered_user_info = {key: User_info[key] for key in order if key in User_info}
            if User_info.get("USER") in expired_users:
                file.write("#-")
                for key, value in ordered_user_info.items():
                    if key == "USER":
                        file.write(f" {key}: {value}\n")
                    else:
                        file.write(f"#  {key}: {value}\n")
            else:
                yaml.dump([ordered_user_info], file)
            counter += 1
            if counter == 1:
                file.write("\n")
                counter = 0

        for comment in comments:
            file.write(comment)
            if "END_TIME" in comment:
                file.write("\n")

def file_missing_dates(Users_info_list):
    if Users_info_list is None:
        return[]
    current_time = datetime.now()

    for User_info in Users_info_list:
        START_TIME = User_info.get("START_TIME")
        END_TIME = User_info.get("END_TIME")

        if START_TIME is None:
            User_info["START_TIME"] = current_time.strftime('%m-%d')

        if END_TIME is None:
            User_info["END_TIME"] = (current_time + timedelta(days=30)).strftime('%m-%d')

    return Users_info_list

def check_time_validity(START_TIME, END_TIME, current_time):
    return START_TIME <= current_time <= END_TIME

def main(file_path):
    combined_addresses = []
    expired_users = []
    current_time = datetime.now().strftime('%m-%d')
    comments, Users_info_list = load_User_info(file_path)
    Users_info_list = file_missing_dates(Users_info_list)

    for User_info in Users_info_list:
        USER = User_info.get("USER", '')
        WIFI = User_info.get("WIFI", '')
        WIRED = User_info.get("WIRED", '')
        START_TIME = User_info.get("START_TIME", '')
        END_TIME = User_info.get("END_TIME", '')

        if START_TIME and END_TIME:
            if check_time_validity(START_TIME, END_TIME, current_time):
                combined = f"{WIFI} {WIRED}"
                combined_addresses.append(combined)
        
        if END_TIME < current_time:
           send_mail(USER)
           expired_users.append(USER)
           print(expired_users)
           save_User_info(file_path, comments, Users_info_list, expired_users)

    result = ' '.join(combined_addresses)
    return result 

if __name__ == "__main__":
    pass
    