from flask import Flask
import os

def create_app():
	app = Flask(__name__, instance_relative_config=True)
	sk = os.environ['SECRET_KEY']
	app.config.from_mapping(SECRET_KEY=sk)

	@app.route('/')
	def index():
		return "Server is up and running"

	import application.operations as operations
	app.register_blueprint(operations.bp)

	return app

application = create_app()