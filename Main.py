from UCI_DATA_API import *
from hackuci_gui import *



gui = GUI()
#classData = ClassDataManager()
food = FoodDataManager()



pippin = food.get_pippins_food()
food.process_available_data()
food.process_result()
pipFood = food.getJSON()
pipKeys = json.loads(pipFood).keys()
gui.retrieve_food(json.loads(pipFood))


    
    


print(json.loads(pipFood).keys())
ant = food.get_anteatery_food()
brandy = food.get_brandy_food()


    

