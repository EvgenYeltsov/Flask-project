from app import fapp, db
from app.models import User, Post

if __name__ == '__main__':
	fapp.run(Debug=True)


@fapp.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, "Post": Post}
