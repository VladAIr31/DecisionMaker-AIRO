import pick
import data_builder

def small_set():
    return pick.fetch_data_set(contest_id = 1915,size=25)

def medium_set():
    return pick.fetch_data_set(contest_id = 1915,size=100)

if __name__ == "__main__":
    data_set = small_set()
    print(data_set)
