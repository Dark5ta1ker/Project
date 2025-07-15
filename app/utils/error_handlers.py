from flask import jsonify

def register_error_handlers(app):
    """
    Регистрирует обработчики ошибок для Flask-приложения.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        # Логирование неожиданных ошибок (можно добавить logging)
        return jsonify({"error": "An unexpected error occurred"}), 500