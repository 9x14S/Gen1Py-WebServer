#include <stdio.h>
#include <stdlib.h>

#define NAME_SIZE 0xB

int main(int argc, char *argv[])
{
    // Check that argv is not empty and no extra strings were passed
    if (argc != 2)
    {
        printf("Usage: %s <save>\n", argv[0]);
        return 1;
    }

    // Load save file
    FILE *save = fopen(argv[1], "rb");
    if (save == NULL)
    {
        printf("Couldn't open save file. \n");
        fclose(save);
        return 2;
    }

    // Go to the player's name address
    fseek(save, 0x2597, SEEK_SET);

    // Get the player's name
    char name[NAME_SIZE];
    if (fgets(name, sizeof(name), save) == NULL)
    {
        printf("Couldn't read name. \n");
        fclose(save);
        return 3;
    }
        
    // Print player's name
    printf("Name: %s\n", name);
    fclose(save);
    return 0;
}