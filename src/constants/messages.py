class ApiMessages:
    """
    This class contains all API messages (excluding errors) and methods to generate such messages.

    Methods:
        delete_data_by_id_success(data_type, data_id):
            - data_type (str): Type of data that was deleted. 
            - data_id (str): ID of the data that was deleted. 
            - Returns: str
    """

    @staticmethod
    def delete_data_by_id_success(data_type: str, data_id: str) -> str:
        return f'{data_type.capitalize()} with ID "{data_id}" deleted successfully.'


    class User:
        """
        This class contains all messages for /user/...
        """

        register_success = 'User created successfully.'
        login_success = 'Login successful.'
        session_refresh_success = 'Session refreshed successfully.'


    class Portfolio:
        """
        This class contains all messages for /user/... and methods to generate such messages.

        Methods:
            p_element_deleted_cause_count_zero(p_element_id):
                - p_element_id (str): ID of the element that was deleted.
                - Returns: str
        """

        @staticmethod
        def p_element_deleted_cause_count_zero(p_element_id: str) -> str:
            return f'Portfolio Element with ID "{p_element_id}" was deleted because count was zero or less.'

