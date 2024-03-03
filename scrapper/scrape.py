import pick
import data_builder

if __name__ == "__main__":
    data_set = pick.fetch_data_set(contest_id = 1915,size=10)
    
    for submission in data_set:
        data = data_builder.create_package(submission)
        break