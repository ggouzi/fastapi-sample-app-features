
class Consts:

    ERROR_CODE_400 = 400
    ERROR_CODE_401 = 401
    ERROR_CODE_403 = 403
    ERROR_CODE_404 = 404
    ERROR_CODE_409 = 409
    ERROR_CODE_426 = 426
    ERROR_CODE_500 = 500

    MAX_TOKENS_PER_USER = 2
    MAX_RESULTS_PER_PAGE = 20
    ACCESS_TOKEN_EXPIRE_MINUTES = 120
    REFRESH_TOKEN_EXPIRE_DAYS = 200
    # Optional key concatenated with clear password given from user to set hash in database.
    # Hardcoded secret stored only on backend side allo to not compromise passwords if database is leaked
    # SECRET_KEY is used to generated hashed_password (based on password and salt) and to decrypt it
    SECRET_KEY = "mysecretbackendkey"
    TOKEN_LENGTH = 128
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'
    HEADER_VERSION = 'x-version'
    HEADER_AUTH = 'authorization'
    PERMISSION_ADMIN = 'Admin'
    PERMISSION_ADMIN_OR_USER_OWNER = 'User Owner'
    PERMISSION_ADMIN_OR_ITEM_OWNER = 'Item Owner'
    PERMISSION_USER = 'User'

    INVALID_CREDENTIALS = "Invalid credentials"
    INVALID_CREDENTIALS_OR_DISABLED = "Invalid credentials or inactive account"
    ITEM_ALREADY_EXISTS = "Item with the same name already exists"
    ITEM_NOT_FOUND = "Item not found"
    FAILED_TO_DELETE_ITEM = "Internal error: Failed to delete item"
    FAILED_TO_UPDATE_USER = "Internal error: Failed to update user"
    FAILED_TO_DISABLE_USER = "Internal error: Failed to disable user"
    ROLE_NOT_FOUND = "Role not found"
    USER_ALREADY_EXIST = "Username already taken"
    USER_NOT_FOUND = "User not found"
    CANNOT_EDIT_USER_NON_ADMIN = "Forbidden access: Cannot edit a different User without being an admin"
    CANNOT_EDIT_ADMIN_USER = "Forbidden access: Cannot edit an admin user"
    CANNOT_SET_SELF_ADMIN = "Forbidden access: Cannot elevate your own permissions to Admin"
    ERROR_CODE_ACTIVATE_AS_NON_ADMIN = "Forbidden access: Cannot enable/disable a user as a non-admin user"
    NOT_AUTHENTIFIED = "Not authentified"
    FORBIDDEN_ACCESS = "Forbidden access: User cannot access this resource"
    VERSION_NOT_SUPPORTED = "Version not supported anymore"
