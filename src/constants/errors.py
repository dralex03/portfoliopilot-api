class ApiErrors:
    """
    This class contains all API Error messages and methods to generate often used error messages.

    Methods:
        field_wrong_type(field_name, type):
            - field_name (str): Field name from JSON body.
            - type (str): Required type for that field.
            - Returns: str
        field_is_empty(field_name):
            - field_name (str): Field name from JSON body.
            - Returns: str
        num_field_out_of_limit(field_name, limit, scope):
            - field_name (str): Field name from JSON body.
            - limit (str): Required limit for the number field.
            - scope (str): Whether field needs to be below or above this.
            - Returns: str
        delete_portfolio_by_id_error(data_type, data_id):
            - data_type (str): Type of data that failed to delete. 
            - data_id (str): ID of the data that failed to delete. 
            - Returns: str
        data_by_id_not_found(data_type, data_id):
            - data_type (str): Type of data that was not found. 
            - data_id (str): ID of the data that was not found. 
            - Returns: str
    """

    invalid_json = 'Error Parsing JSON body.'
    body_is_not_json = 'Request body needs to be JSON.'

    @staticmethod
    def field_wrong_type(field_name: str, type: str) -> str:
        return f'Field "{field_name}" needs to be a {type}.'
    
    @staticmethod
    def field_is_empty(field_name: str) -> str:
        return f'Field "{field_name}" can not be empty.'
    
    @staticmethod
    def num_field_out_of_limit(field_name: str, limit: str, scope: str) -> str:
        match scope:
            case '>':
                return f'Field "{field_name}" needs to be greater than {limit}.'
            case '>=':
                return f'Field "{field_name}" needs to be equal to or greater than {limit}.'
            case '<=':
                return f'Field "{field_name}" needs to be equal to or less than {limit}.'
            case '<':
                return f'Field "{field_name}" needs to be less than {limit}.'
            

    @staticmethod
    def delete_data_by_id_error(data_type: str, data_id: str) -> str:
        return f'Error deleting {data_type} with ID "{data_id}".'

    @staticmethod
    def data_by_id_not_found(data_type: str, data_id: str) -> str:
        return f'{data_type.capitalize()} with ID "{data_id}" not found.'


    class User:
        """
        This class contains all error messages for /user/...
        """

        # Query Errors
        get_user_by_email_error = 'Error finding user.'
        get_user_by_id_error = 'Error finding user.'
        add_new_user_error = 'Error creating user.'

        # Register
        register_invalid_email = 'Invalid Email address.'
        register_invalid_password = 'Password does not meet requirements.'
        register_already_exists = 'User already exists. Please log in.'

        # Login
        login_invalid_credentials = 'Invalid email or password.'

    class JwtAuth:
        user_id_not_exist = 'User ID does not exist.'
        missing_jwt_token = 'Missing JWT auth-token or invalid format.'
        jwt_token_expired = 'Signature expired. Please log in again.'
        jwt_token_invalid = 'Invalid token. Please log in.'


    class Portfolio:
        """
        This class contains all error messages for /user/portfolio/...
        """

        # Query Errors
        get_portfolios_by_user_id_error = 'Error fetching all portfolios.'
        get_portfolio_by_id_error = 'Error fetching portfolio.'
        add_portfolio_error = 'Error creating portfolio.'
        update_portfolio_name_error = 'Error updating portfolio.'
        add_portfolio_element_error = 'Error adding asset to portfolio.'
        get_portfolio_element_error = 'Error fetching portfolio element.'
        update_portfolio_element_error = 'Error updating portfolio element.'

        # Input Errors
        portfolio_already_exists = 'Portfolio with this name already exists.'
        update_p_element_all_values_none = 'Please enter at least one value to change.'

