"""
Database Routers for Digital Signage

Routes queries for external data sources to their respective databases.
"""


class DataConnectRouter:
    """
    Database router for the data_connect database.

    Routes all SalesBoardSummary queries to the 'data_connect' database.
    This database contains read-only data populated by external ETL processes.
    """

    # Models that should use the data_connect database
    route_app_labels = {'digital_signage'}
    route_model_names = {'salesboardsummary'}

    def db_for_read(self, model, **hints):
        """
        Route read operations for SalesBoardSummary to data_connect.
        """
        if model._meta.model_name in self.route_model_names:
            return 'data_connect'
        return None

    def db_for_write(self, model, **hints):
        """
        SalesBoardSummary is read-only, prevent writes.
        Other models use the default database.
        """
        if model._meta.model_name in self.route_model_names:
            # Return None to effectively block writes (table is read-only)
            # Could also raise an error here
            return None
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the same database.
        """
        # Don't allow relations between data_connect models and default models
        obj1_is_data_connect = obj1._meta.model_name in self.route_model_names
        obj2_is_data_connect = obj2._meta.model_name in self.route_model_names

        if obj1_is_data_connect or obj2_is_data_connect:
            return obj1_is_data_connect == obj2_is_data_connect
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Prevent migrations for SalesBoardSummary (managed=False anyway).
        """
        if model_name and model_name.lower() in self.route_model_names:
            # Never migrate these models - they're managed externally
            return False

        if db == 'data_connect':
            # Never run any migrations on data_connect database
            return False

        return None
