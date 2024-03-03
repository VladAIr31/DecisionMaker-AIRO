import pick
import data_builder

def seed_to_package(entry):
    return data_builder.create_package(entry)

def small_set():
    return pick.fetch_data_set(contest_id = 1915,size=25)

if __name__ == "__main__":
    data_set = small_set()
    print(data_set)
