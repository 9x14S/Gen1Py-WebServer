#include <stdio.h>
#include <stdlib.h>

#define MAIN_START 0x2597
#define MAIN_END 0x3522
#define CHECKSUM 0x3523
#define MAIN_RANGE 0xF8B

#define BAD_SAVENAME -1
#define B_SERROR "Invalid save file name."

#define COULDNT_OPEN -2
#define C_COFERROR "Couldn't open save file."

#define COULDNT_CHECKS -3 
#define C_CERROR "Couldn't check previous checksum."

#define MAIN_UNREAD -4
#define M_RERROR "Couldn't read data from main bank."

#define COULDNT_CLOSE -5
#define C_CFERROR "Couldn't close save file."

FILE *open_file(char *savename)
{
    // Check everything's in order
    if (savename == NULL)
    {
        printf("%s 'open_file()' error.\n", B_SERROR);
        exit(BAD_SAVENAME);
    }

    FILE *save = fopen(savename, "rb+");
    if (save == NULL)
    {
        printf("%s 'open_file()' error.\n", C_COFERROR);
        fclose(save);
        exit(COULDNT_OPEN);
    }
    return save;
}

int close_file(FILE *save)
{
    if (save != NULL)
    {
        fclose(save);
        puts("(From C): Saved changes. \n");
        return 0;
    }
    else
    {
        printf("(From C):  %s\n", C_CFERROR);
        return COULDNT_CLOSE;
    }
}

int checksum(FILE *save)
{
    unsigned char prevcheck, compcheck, temp;

    // Move to and get the previous checksum
    fseek(save, CHECKSUM, SEEK_SET);
    
    if ((prevcheck = fgetc(save)) == EOF)
    {
        printf("%s 'checksum()' error.\n", C_CERROR);
        fclose(save);
        return COULDNT_CHECKS;
    }

    // Move back to the start of main bank
    fseek(save, MAIN_START, SEEK_SET);

    // Calculate the checksum 
    for (int i = MAIN_RANGE ; i != 0; i--)
    {
        temp = fgetc(save);
        if (temp == EOF)
        {
            printf("%s 'checksum()' error.\n", M_RERROR);
            fclose(save);
            return MAIN_UNREAD;
        }

        else compcheck += temp;
    }

    compcheck = ~compcheck - 1;
    printf("(From C): Previous checksum: %d, Computed checksum: %d.\n", prevcheck, compcheck);
    fclose(save);
    return compcheck;
}

int edit_offset(FILE *save, int offset, unsigned char value)
{

    fseek(save, offset, SEEK_SET);
    fputc(value, save);
    return 0;
}