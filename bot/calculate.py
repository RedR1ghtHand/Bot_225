from db_manager import *

db = DB_Manager()
def calculate_cart(user_id):
    data = db.get_user_cart(user_id)[0].split('/')[1::]
    data_dict = {item: data.count(item) for item in data}

    result = [db.get_ingredients_by_dish_name(dish) * data_dict[dish] for dish in data_dict]
    result_ = []
    for item in result:
        for ingr in item:
            result_.append(ingr)

    result_dict = {item:result_.count(item) for item in result_}
    result_str = ''
    for item in result_dict:
        result_str += f'{item[0]} : {item[1] * result_dict[item]:.2f} \n'
    return result_str





if __name__ == '__main__':
    DB = DB_Manager()
    calculate_cart('1315483904')