# OneUCI APP

Created by the OneHack Hack UCI Team:
 Norman E.
 Varun S.
 Simon L.
 Shawn H.
 Johnathan C.

This file primarily describes the UCI_DATA_API; a simple API specifically designed to streamline the reading of data from UCI's food and course data. The OneUCI app utilizes this API heavily in order to generate a user-friendly interface for viewing and interacting with the large volume of data.

## Table of Contents

1. [Highlights](#highlights)
2. [Roadmap](#roadmap)
3. [TODOs](#todos)

1. [App Usage](#usage-app)
2. [API Usage](#usage-api)
3. [Parser Usage](#usage-parser)
4. [Examples]($eamples)
4. [Requirements](#requirements)
5. [Development](#develompent)

## Highlights
This project features a full API and working python-based application framework for either IOS or Android.

For more information, visit our github page: https://github.com/VarunS1997/OneUCI.

## ROADMAP
 Firstly, various visual improvements could and should be implemented. Particularly on the food tab.

 In the future, we plan on integrating a social walking service to track anteater walking patterns at UCI. Using the resulting data, we can create more efficient walking routes.

 We also plan on parsing food nutritional data more carefully, vs the current "sweeping" tactic for basic information. We will, of course, make this information easily accessible.

 Furthermore, we plan to integrate the events tab with UCI's EEE calander for pulling courses.

 Lastly, we plan on using a basic machine learning algorithm to provide users with UCI news that is considered potentially interesting to them based on events they attend, courses they take, and places they frequent.

 In terms of the API, we plan on increasing it's robustness and providing XML output by request. Additionally, optimizations to the searching algorithms for the ```HTMLReferenceTree``` class should be implemented.

## TODOs

1. Write a better self test for UCI_DATA_API
2. Something with events page? Ability to add events at least?
3. Prevent "over scrolling"

## Installation
Simply import the ```UCI_DATA_API.py``` module into the module you intend to use the API.

For lightweight, HTML parsing, implement the ```OneHack_HTML_Parser.py``` module.

## Usage (APP)
Simply run the ```main.py``` module.

## Usage (API)
To use the module, start by creating either a ```FoodDataManager``` or ```ClassDataManager``` class.

Each of these classes supports the same standard sequence of events:
 1. Construct an instance
 2. Designate an html source with ```UCI_DATA_API.set_html_target()```
 3. Activate data parsing with ```UCI_DATA_API.process_available_data()```
 4. Finalize answer into friendly data formats with ```UCI_DATA_API.process_result()```

From that point, the parsed result can be obtained as a JSON file through ```UCI_DATA_API.getJSON()```
or as a python dictionary though ```UCI_DATA_API.get_result()```.

Tests can also be preformed by running the UCI_DATA_API.py file.

## Usage (Parser)
 After construction, one of the following functions must be called and bound to the parser:
    - ```get_HTML_from_url()```
    - ```get_HTML_from_string()```
    - ```get_HTML_from_file()```
 Each specifies a different type of html source, and at least one must be selected before continuing.

 To initiate parsing, call ```HTMLReferenceTree.parse_data()```. The resulting parser state can then carry out find operations on the data.

 Tests can also be preformed by running the ```OneHack_HTML_Parser.py``` file.

## Examples
Some basic examples:
```
courseManager = ClassDataManager()
courseManager.set_html_target()
courseManager.process_available_data()
courseManager.process_result()
courseManager.getJSON()

foodManager = FoodDataManager()
foodManager.get_pippins_food()
foodManager.process_available_data()
foodManager.process_result()
```

In addition to these basic examples, running ```OneHack_HTML_Parser.py``` or ```UCI_DATA_API.py``` will start testing programs.

## Requirements

- Python 3.3 or greater


## Development
 Created as a part of the HACK UCI Hackathon

 While simple, the ```UCI_DATA_API``` provides all the potentially useful methods of locating and parsing both UCI meal and course data. It also prepares the result for JSON encoding or usage as a dictionary.

 The lightweight, HTML parser is built on python's basic html parser, yet provides additional functions and details for quickly locating and iterating through data. In particular, it provides an internal array of HTML id attributes, for rapid searching by ID. The search by attributes, however, expects more than one answer and thus, must do a thorough, linear search through all data nodes.

 Additionally, the ```HTMLReferenceTree``` class works primarily with HTMLNodes, a simple implementation of a node for quick access of children and parents. HTMLNodes are also equipped with basic comparision operators for sorting purposes.
