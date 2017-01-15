from UCI_DATA_API import *
from hackuci_gui import *



gui = GUI()
#classData = ClassDataManager()
food1 = FoodDataManager()
food2 = FoodDataManager()
food3= FoodDataManager()



food1.get_pippins_food()
food1.process_available_data()
food1.process_result()
pip = json.loads(food1.getJSON())

food2.get_anteatery_food()
food2.process_available_data()
food2.process_result()
ant = json.loads(food2.getJSON())

food3.get_brandy_food()
food3.process_available_data()
food3.process_result()
brand = json.loads(food3.getJSON())

gui.retrieve_food(pip, brand, ant)


    
    







    

