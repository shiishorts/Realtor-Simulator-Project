#include <iostream>
using namespace std;

// declare functions
void menu(string& UserInput, int& dataStruct);
void input(string& UserInput);

void menu(string& UserInput, int& dataStruct) {
  string option; 
  
  cout << "Select an option:" << endl;
  cout << "1) Search for housing" << endl;
  cout << "2) Data Algorithm 1: BFS" << endl;
  cout << "3) Data Algorithm 2: DFS" << endl;
  cout << "4) Exit" << endl;

  cin >> option;

  if (option == "1") {
    input(UserInput); // return string of university / city, state
  } else if (option == "2") {
    cout << "You selected Data Algorithm 1: BFS\n" << endl;
    dataStruct = 1;
    menu(UserInput, dataStruct);
  } else if (option == "3") {
    cout << "You selected Data Algorithm 2: DFS\n" << endl;
    dataStruct = 2;
    menu(UserInput, dataStruct);
  } else if (option == "4") {
    cout << "Exiting..." << endl;
    UserInput = "-1";
  } else {
    cout << "Invalid input. Please try again.\n" << endl;
    menu(UserInput, dataStruct);
  }
  return;
}

void input(string& UserInput) { //returns a string that contains the university, college or city, state
  string option;
  
  cout << "\nSelect an option:" << endl;
  cout << "1) Input University/College" << endl;
  cout << "2) Input city and state" << endl;

  cin >> option;
  
  if (option == "1") {
    cout << "\nPlease enter your University or College." << endl;
    cout << "[Ex.) University of Florida]" << endl;
    cin >> UserInput;               
  }
  else if (option == "2") {
    cout << "\nPlease enter your city with your state." << endl;
    cout << "[Ex.) Gainesville, FL]" << endl;
    cin >> UserInput;
  }
  else {
    cout << "\nInvalid input. Please try again." << endl;
    input(UserInput);
  }
  return;
}

int main() {
  string userInput;
  int dataStruct;
  
  cout << "----------------Welcome to the REALTOR SIMULATOR: Student Edition----------------";
  cout << "\n";
  
  menu(userInput, dataStruct);

  cout << "chosen items: " << userInput << " " << dataStruct << endl;

  if(userInput == "-1")
    return 0;
  
    }
