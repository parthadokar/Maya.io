#include <iostream>
#include <fstream>

void getPing () {}

void getIpConfiguration () {}

void dnslookup() {}

void traceroute () {}

void speedtest () {}

void scanPort() {}

void saveFile() {}

int main () {
    std::cout << "Welcome to Network Diagnostic Tool\n";
    int choice;
    while (true) {
        std::cout << "\nSelect an option:\n";
        std::cout << "1. Ping Test\n";
        std::cout << "2. Get IP Configuration\n";
        std::cout << "3. DNS Lookup\n";
        std::cout << "4. Trace Route\n";
        std::cout << "5. Speed Test\n";
        std::cout << "6. Scan Port\n";
        std::cout << "7. Save The data to file\n";
        std::cout << "8. Exit\n";
        std::cout << "Enter your choice: ";

        std::cin >> choice;
        std::cin.ignore(); // optional, in case of mixing cin and getline later

        switch (choice) {
            case 1:
                getPing();
                break;
            case 2:
                getIpConfiguration();
                break;
            case 3:
                dnslookup();
                break;
            case 4:
                traceroute();
                break;
            case 5:
                speedtest();
                break;
            case 6:
                scanPort();
                break;
            case 7:
                saveFile();
                break;
            case 8:
                std::cout << "Exiting...\n";
                return 0;
            default:
                std::cout << "Invalid choice. Please try again.\n";
        }
    }
}
