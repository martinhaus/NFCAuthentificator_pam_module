#include <security/pam_appl.h>
#include <security/pam_misc.h>
#include <stdlib.h>
 
static struct pam_conv conv = {
    misc_conv, /* Conversation function defined in pam_misc.h */
    NULL /* We don't need additional data now*/
};
 
int main()
{
        pam_handle_t *handle = NULL;
        const char *service_name = "pam_nfc";
        int retval;
        char *username; /* This will be set by PAM with pam_get_item (see below) */
 
        retval = pam_start(service_name, NULL, &conv, &handle); /* Initializing PAM */
        if (retval != PAM_SUCCESS){
                fprintf(stderr, "Failure in pam initialization: %s", pam_strerror(handle, retval));
                return 1;
        }
 
        retval = pam_authenticate(handle, 0); /* Do authentication (user will be asked for username and password)*/
        if (retval != PAM_SUCCESS) {
                fprintf(stderr, "Failure in pam authentication: %s", pam_strerror(handle, retval));
                return 1;
        }

        printf("Successful authentication!\n");
    
        pam_end(handle, retval); /* ALWAYS terminate the pam transaction!! */
}