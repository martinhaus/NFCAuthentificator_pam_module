#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <stdbool.h>
#include <security/pam_modules.h>
#include <security/pam_ext.h>
#include <sys/stat.h>
#include <unistd.h>

#define  PYTHON_WRAPPER_COMMAND "python wrapper.py -a"

PAM_EXTERN int pam_sm_authenticate(pam_handle_t *handle, int flags, int argc,
				   const char **argv)
{
    int exitValue = 0;
    exitValue = WEXITSTATUS(system(PYTHON_WRAPPER_COMMAND));

    if (exitValue != 0) {
        printf("Auth failure\n");
        return PAM_PERM_DENIED;
    }

    return PAM_SUCCESS;
}

PAM_EXTERN int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags, int argc,
				const char **argv)
{

}

PAM_EXTERN int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc,
			      const char **argv)
{
	
}

PAM_EXTERN int pam_sm_open_session(pam_handle_t *pamh, int flags, int argc,
				   const char **argv)
{

}

PAM_EXTERN int pam_sm_close_session(pam_handle_t *pamh, int flags, int argc,
				    const char **argv)
{
	
}

PAM_EXTERN int pam_sm_chauthtok(pam_handle_t *pamh, int flags, int argc,
				const char **argv)
{

}

