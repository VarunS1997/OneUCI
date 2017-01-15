from UCI_DATA_API import *
from hackuci_gui import *

def main():
    gui = GUI()

    classData = ClassDataManager()
    food1 = FoodDataManager()
    food2 = FoodDataManager()
    food3= FoodDataManager()

    food1.get_pippins_food()
    food1.process_available_data()
    food1.process_result()
    pip = food1.get_result()

    food2.get_anteatery_food()
    food2.process_available_data()
    food2.process_result()
    ant = food2.get_result()

    food3.get_brandy_food()
    food3.process_available_data()
    food3.process_result()
    brand = food3.get_result()

    courseManager = ClassDataManager()
    courseManager.set_html_target()
    courseManager.process_available_data()
    courseManager.process_result()
    classData = classData.get_result()

    gui.retrieve_food(pip, brand, ant)
    gui.run()

if __name__ == '__main__':
    main()
