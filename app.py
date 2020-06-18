import matplotlib
matplotlib.use('Agg')
from flaskfile import app

if __name__ == '__main__':
	app.run(debug=True)
