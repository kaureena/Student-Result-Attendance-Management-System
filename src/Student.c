#include <stdio.h>
#include <string.h>

struct Student {
    int id;
    char name[50];
    float attendance;
};

#Validate Student Id
int validateStudentID(int id) {
    if(id <= 0) {
        printf("Error: Invalid Student ID\n");
        return 0;
    }
    return 1;
}

void addStudent() {
    struct Student s;
    printf("Enter Student ID: ");
    scanf("%d", &s.id);

    if(!validateStudentID(s.id)) return;

    printf("Enter Name: ");
    scanf("%s", s.name);

    printf("Student Added Successfully!\n");
}

