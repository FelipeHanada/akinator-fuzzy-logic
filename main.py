from infra.configs.connection import DBConnectionHandler

if __name__ == '__main__':
    db_handler = DBConnectionHandler()
    db_handler.create_tables()

    """
    fuzzy_system = FuzzySystem()
    fuzzy_system.create_input_variables()
    fuzzy_system.create_output_variables()
    fuzzy_system.create_rules()
    output_value = fuzzy_system.compute_output()
    print("Output value:", output_value)
    """
